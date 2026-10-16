# k6 专栏示例资产

本目录存放《k6 性能测试从入门到精通》正文引用的示例脚本与本地被测服务，全部面向本机短时低压力跟练，读数不用于任何容量、稳定性或工具性能结论。

## 本地回显服务：echo_server.py

仅用 Python 标准库实现，监听 `127.0.0.1:8899`，把请求要素回显成 JSON，便于核对脚本实际发出的内容。

```bash
# 启动（前置条件：Python 3.x，端口 8899 空闲）
python echo_server.py

# 自测预期：返回带 "k6-echo" 的 JSON 首页
curl http://127.0.0.1:8899/
```

| 端点 | 方法 | 行为 |
|---|---|---|
| `/` | GET | 首页，返回服务信息 JSON |
| `/get` | GET | 回显查询参数、请求头 |
| `/post` | POST | 回显 JSON／表单／上传字节数 |
| `/basic-auth/user/pass` | GET | 演示账号 `user:pass`，凭据错误返回 401 |
| `/cookies/set` | GET | 种下演示 Cookie `k6demo=abc123` |
| `/cookies` | GET | 回显请求携带的 Cookie 头 |

## 模拟工单服务：ticket_service.py

仅用 Python 标准库实现，监听 `127.0.0.1:8898`，模拟最小业务系统：登录发令牌、带令牌查工单、校验标题建工单。预置 5 张内存工单，每个请求固定加 20 毫秒模拟业务处理耗时，重启即还原。

```bash
# 启动（前置条件：Python 3.x，端口 8898 空闲）
python ticket_service.py

# 自测预期：返回带 "k6-ticket-demo" 的 JSON 首页
curl http://127.0.0.1:8898/
```

| 端点 | 方法 | 行为 |
|---|---|---|
| `/` | GET | 首页，返回服务信息 JSON |
| `/login` | POST | 演示账号 `demo/demo123`，正确返回令牌，错误 401 |
| `/tickets` | GET | 需 `Authorization: Bearer <令牌>`，返回工单列表 |
| `/tickets/{id}` | GET | 需令牌，返回单张工单，不存在 404 |
| `/tickets` | POST | 需令牌，JSON 对象且 `title` 为非空字符串则 201 创建，否则 400 |
| `/events` | GET | 需令牌，SSE 事件流：推送当前内存全部工单事件（刚启动时为 5 条，间隔 200 毫秒）后主动收尾 |

## 各篇使用

- 第 01 篇：`01/first.js` 最小脚本打回显服务 `/`，配两轮命令行对照实跑记录（`01/本地实跑记录-2026-10-13.md`）；`01/ticket_flow.js` 业务流脚本打模拟工单服务（登录 → 列表 → 详情 → 创建），`01/sse_demo.js` 收 SSE 事件流并按 `data:` 计数断言，测试案例与各轮实跑输出见 `01/测试案例-工单模拟服务.md`。
- 第 02 篇：`02/` 下 5 个生命周期脚本（`lifecycle.js`、`setup_isolation.js`、`setup_failure.js`、`init_forbidden.js`、`summary_hook.js`）打模拟工单服务，逐轮实跑输出与 `summary.json` 生成物同目录，实跑记录与测试案例见 `02/本地实跑记录-2026-10-14.md`、`02/测试案例-生命周期脚本.md`，生命周期边界探针（init 求值计数、迭代内异常、主动中止）归档于 `02/探针记录-生命周期边界-2026-10-16.md`。
- 第 03 篇：请求方法、鉴权、Cookie、参数化示例的默认目标（回显服务，`BASE_URL` 默认 `http://127.0.0.1:8899`）。
