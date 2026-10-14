"""k6 专栏模拟工单服务。

仅用 Python 标准库，监听 127.0.0.1:8898，模拟一个最小业务系统的
登录鉴权与工单增查接口，供《k6 性能测试从入门到精通》第 01 篇
「模拟测试」环节使用：被测对象有业务形态，脚本才有业务可断。

启动：python ticket_service.py
自测：curl http://127.0.0.1:8898/
仅限本机短时低压力跟练，读数不用于任何容量结论。
"""

import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 8898

# 模拟业务处理耗时（秒）：让每个请求的响应时间有真实服务的形态。
HANDLING_SECONDS = 0.02

# 演示账号与令牌，仅用于本地模拟服务教学，不是真实凭据。
DEMO_USER = "demo"
DEMO_PASS = "demo123"
DEMO_TOKEN = "demo-token-0001"

# 预置内存数据，重启即还原；创建操作只改本进程内存。
TICKETS = [
    {"id": 1, "title": "登录页验证码不刷新", "status": "open"},
    {"id": 2, "title": "导出报表超时", "status": "processing"},
    {"id": 3, "title": "工单列表分页错乱", "status": "open"},
    {"id": 4, "title": "消息通知重复推送", "status": "closed"},
    {"id": 5, "title": "附件上传失败", "status": "processing"},
]


class TicketHandler(BaseHTTPRequestHandler):
    server_version = "K6TicketDemo/1.0"

    def _send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            return json.loads(raw.decode("utf-8")) if raw else {}
        except (ValueError, UnicodeDecodeError):
            return None

    def _authorized(self):
        return self.headers.get("Authorization") == f"Bearer {DEMO_TOKEN}"

    def _require_auth(self):
        if self._authorized():
            return True
        self._send_json({"error": "missing or invalid token"}, status=401)
        return False

    def do_GET(self):
        time.sleep(HANDLING_SECONDS)
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_json({
                "service": "k6-ticket-demo",
                "message": "模拟工单服务已就绪",
                "endpoints": ["POST /login", "GET /tickets",
                              "GET /tickets/{id}", "POST /tickets",
                              "GET /events"],
            })
            return
        if parsed.path == "/events":
            if self._require_auth():
                self._sse_events()
            return
        if parsed.path == "/tickets":
            if self._require_auth():
                self._send_json({"tickets": TICKETS, "total": len(TICKETS)})
            return
        if parsed.path.startswith("/tickets/"):
            if not self._require_auth():
                return
            try:
                ticket_id = int(parsed.path.rsplit("/", 1)[1])
            except ValueError:
                self._send_json({"error": "invalid ticket id"}, status=400)
                return
            ticket = next((t for t in TICKETS if t["id"] == ticket_id), None)
            if ticket:
                self._send_json(ticket)
            else:
                self._send_json({"error": "ticket not found"}, status=404)
            return
        self._send_json({"error": "unknown endpoint"}, status=404)

    def do_POST(self):
        time.sleep(HANDLING_SECONDS)
        parsed = urlparse(self.path)
        if parsed.path == "/login":
            body = self._read_json()
            if not isinstance(body, dict):
                self._send_json({"error": "request body must be a JSON object"},
                                status=400)
                return
            if body.get("username") == DEMO_USER and \
                    body.get("password") == DEMO_PASS:
                self._send_json({"token": DEMO_TOKEN, "user": DEMO_USER})
            else:
                self._send_json({"error": "invalid credentials"}, status=401)
            return
        if parsed.path == "/tickets":
            if not self._require_auth():
                return
            body = self._read_json()
            if body is None:
                self._send_json({"error": "request body must be JSON"},
                                status=400)
                return
            if not isinstance(body, dict):
                self._send_json({"error": "request body must be a JSON object"},
                                status=400)
                return
            title = body.get("title")
            if not isinstance(title, str) or not title.strip():
                self._send_json({"error": "title is required"}, status=400)
                return
            ticket = {
                "id": max(t["id"] for t in TICKETS) + 1,
                "title": title,
                "status": "open",
            }
            TICKETS.append(ticket)
            self._send_json(ticket, status=201)
            return
        self._send_json({"error": "unknown endpoint"}, status=404)

    def _sse_events(self):
        # 推送当前全部工单事件后主动收尾（刚启动时 5 条）：标准 HTTP
        # 客户端也能完整读取的 SSE 形态（text/event-stream，每条事件
        # 以 data: 开头、空行收尾）。
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        for ticket in TICKETS:
            payload = json.dumps({"event": "status", "ticket": ticket},
                                 ensure_ascii=False)
            self.wfile.write(f"data: {payload}\n\n".encode("utf-8"))
            self.wfile.flush()
            time.sleep(0.2)

    def log_message(self, fmt, *args):
        # 保留默认访问日志，便于与 k6 侧请求数对账。
        super().log_message(fmt, *args)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), TicketHandler)
    print(f"模拟工单服务：http://{HOST}:{PORT}（Ctrl+C 停止）")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
