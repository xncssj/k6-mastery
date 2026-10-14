"""k6 专栏本地回显服务。

仅用 Python 标准库，监听 127.0.0.1:8899，供《k6 性能测试从入门到精通》
第 01 篇（跑通安装与第一个脚本）与第 03 篇（请求、标签与参数化）跟练使用。

启动：python echo_server.py
自测：curl http://127.0.0.1:8899/
仅限本机短时低压力跟练，不用于任何容量结论。
"""

import base64
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

HOST = "127.0.0.1"
PORT = 8899

# 演示用固定账号，仅用于本地被测服务的 Basic Auth 教学，不是真实凭据。
BASIC_USER = "user"
BASIC_PASS = "pass"


class EchoHandler(BaseHTTPRequestHandler):
    """把请求要素回显成 JSON，方便核对 k6 脚本到底发出去的是什么。"""

    server_version = "K6Echo/1.0"

    def _send_json(self, payload, status=200, extra_headers=None):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        # 响应头只能走 latin-1（一种单字节编码），Cookie 等头值出现中文会直接掐断连接。
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        for key, value in (extra_headers or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(body)

    def _echo(self, body_obj=None):
        parsed = urlparse(self.path)
        return {
            "method": self.command,
            "path": parsed.path,
            "args": {k: v[0] for k, v in parse_qs(parsed.query).items()},
            "headers": {k: v for k, v in self.headers.items()},
            "body": body_obj,
        }

    def _read_body(self):
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        content_type = self.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                return {"json": json.loads(raw.decode("utf-8"))}
            except (ValueError, UnicodeDecodeError):
                return {"raw": raw.decode("utf-8", errors="replace")}
        if "application/x-www-form-urlencoded" in content_type:
            # 非 UTF-8 字节（如 GBK 控制台直发）按替换字符容错，不让 handler 崩溃。
            form = parse_qs(raw.decode("utf-8", errors="replace"))
            return {"form": {k: v[0] for k, v in form.items()}}
        if "multipart/form-data" in content_type:
            boundary = content_type.split("boundary=")[-1].strip().strip('"')
            return self._parse_multipart(raw, boundary)
        return {"raw": raw.decode("utf-8", errors="replace")} if raw else None

    @staticmethod
    def _parse_multipart(raw, boundary):
        # 教学级 multipart 解析：按边界分段，提取普通字段与文件字段并回显。
        fields, files = {}, {}
        for part in raw.split(("--" + boundary).encode()):
            if part in (b"", b"--", b"--\r\n"):
                continue
            if part.startswith(b"\r\n"):
                part = part[2:]
            if part.endswith(b"--"):
                part = part[:-2]
            if part.endswith(b"\r\n"):
                part = part[:-2]
            head, _, content = part.partition(b"\r\n\r\n")
            headers = head.decode("latin-1")
            if 'name="' not in headers:
                continue
            name = headers.split('name="', 1)[1].split('"', 1)[0]
            if 'filename="' in headers:
                filename = headers.split('filename="', 1)[1].split('"', 1)[0]
                files[name] = {"filename": filename,
                               "content": content.decode("utf-8", errors="replace")}
            else:
                fields[name] = content.decode("utf-8", errors="replace")
        return {"form": fields, "files": files}

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send_json({
                "service": "k6-echo",
                "message": "本地回显服务已就绪",
                "endpoints": ["/get", "/post", "/basic-auth/user/pass",
                              "/cookies/set", "/cookies"],
            })
        elif parsed.path == "/get":
            self._send_json(self._echo())
        elif parsed.path == "/basic-auth/user/pass":
            self._basic_auth()
        elif parsed.path == "/cookies/set":
            self._send_json(self._echo(), extra_headers={
                "Set-Cookie": "k6demo=abc123; Path=/",
            })
        elif parsed.path == "/cookies":
            self._send_json({"cookies": self.headers.get("Cookie", "")})
        else:
            self._send_json({"error": "unknown endpoint"}, status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/post":
            self._send_json(self._echo(body_obj=self._read_body()))
        else:
            self._send_json({"error": "unknown endpoint"}, status=404)

    def _basic_auth(self):
        header = self.headers.get("Authorization", "")
        expected = "Basic " + base64.b64encode(
            f"{BASIC_USER}:{BASIC_PASS}".encode()).decode()
        if header == expected:
            self._send_json({"authenticated": True, "user": BASIC_USER})
        else:
            self._send_json({"error": "authentication required"}, status=401,
                            extra_headers={
                                "WWW-Authenticate": 'Basic realm="k6-echo"'})

    def log_message(self, fmt, *args):
        # 保留默认访问日志，方便跟练时对照 k6 侧请求数。
        super().log_message(fmt, *args)


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), EchoHandler)
    print(f"k6 本地回显服务：http://{HOST}:{PORT}（Ctrl+C 停止）")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n回显服务已停止")
