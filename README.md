# k6-mastery

**Author: 7DGroup**

> 《k6 性能测试从入门到精通》专栏（[CSDN](https://blog.csdn.net/zuozewei/category_13216606.html) / 微信公众号）配套示例仓库。
> 范围：k6 示例脚本、本地被测服务、测试案例与实跑证据——面向本机短时低压力跟练的最小可运行资产。

![k6](https://img.shields.io/badge/k6-v2.x-orange)
![Python](https://img.shields.io/badge/Python-3.x%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)

<p align="center">
  <a href="https://blog.csdn.net/zuozewei/category_13216606.html">
    <img src="images/column-poster-k6-mastery.png" alt="《k6 性能测试从入门到精通》专栏海报" width="320">
  </a>
</p>

## 📌 专栏信息

| 项目 | 说明 |
|------|------|
| 专栏系列 | [《k6 性能测试从入门到精通》](https://blog.csdn.net/zuozewei/category_13216606.html)：24 篇（第 00—23 篇），k6 v2.x 基线（CSDN） |
| 仓库用途 | 存放正文引用的示例脚本、本地被测服务、测试案例与实跑证据，按篇目组织 |
| 技术栈 | k6（自带 JS 运行时）· Python 3.x 标准库（两个本地被测服务） |
| 第三方依赖 | 无：不需要 npm / pip 安装任何包，仓库内没有 `package.json` |
| 运行方式 | 本机回环（`127.0.0.1:8899` / `8898`），短时低压力跟练 |
| 实跑基线 | Windows amd64 · k6 v2.2.0 · Python 3.13.2 · curl 8.15.0（2026-10-13 记录） |

> **关于示例读数**：全部示例只打本机回环地址、短时低压力运行，用于验证安装、请求流程与判定口径；读数不作为容量、稳定性或工具性能排名的结论依据。

## 🖼️ 仓库总览

一条链路串起跟练全过程：正文讲解 → 跟练脚本 → 本地被测服务 → k6 运行 → 可复查证据。

```
专栏正文（讲解）→ examples/NN/ 示例脚本 → 本地被测服务（回显 / 模拟工单）→ k6 run → 原始终端输出（run-*.txt）
```

- **两个本地被测服务**：回显服务把请求要素原样回显成 JSON，便于核对脚本实际发出的内容；模拟工单服务提供「登录发令牌 → 带令牌查工单 → 校验建单 → SSE 事件流」的最小业务闭环。
- **第 01 篇脚本覆盖的能力点**：`options` 负载配置与命令行覆盖、阈值（thresholds）、检查（check）、JSON 提取与 Bearer 鉴权、业务流编排、SSE 流式响应断言。
- **证据可复查**：每份实跑输出、服务日志与异常输入处置记录都带版本与日期，可先看证据再动手复跑。

## ✅ 配套资产总览

| 资产 | 说明 | 相关篇目 |
|------|------|----------|
| [examples/README.md](examples/README.md) | 示例资产总说明：两个服务的启动、自测与端点明细 | 全局 |
| `examples/echo_server.py` | 本地回显服务（8899）：回显请求头/参数/Body，演示 Basic Auth 与 Cookie | 第 01、03 篇 |
| `examples/ticket_service.py` | 模拟工单服务（8898）：登录令牌、工单列表/详情/创建、SSE 事件流 | 第 01 篇；第 23 篇规划复用 |
| `examples/01/first.js` | 最小 k6 脚本：`vus`/`duration`、阈值与检查 | 第 01 篇 |
| `examples/01/ticket_flow.js` | 工单业务流：登录 → 列表 → 详情 → 创建，5 处业务断言 | 第 01 篇 |
| `examples/01/sse_demo.js` | SSE 事件流：登录后收流并按 `data:` 计数断言 | 第 01 篇 |
| [examples/01/测试案例-工单模拟服务.md](examples/01/测试案例-工单模拟服务.md) | API-01～14 与 RUN-01～03 用例及通过记录 | 第 01 篇 |
| [examples/01/本地实跑记录-2026-10-13.md](examples/01/本地实跑记录-2026-10-13.md) | first.js 两轮命令行对照与环境口径说明 | 第 01 篇 |
| `examples/01/run-*.txt` 等 | 7 份 k6 原始终端输出、服务日志、SSE 原始流、异常输入处置证据 | 第 01 篇 |

## 📂 仓库结构

```
k6-mastery/
├── README.md                          # 本文件
├── images/
│   ├── column-poster-k6-mastery.png   # 专栏海报
│   └── wechat-7dgroup-qr.jpg          # 7DGroup 公众号二维码
└── examples/
    ├── README.md                      # 示例资产总说明：端点明细与各篇使用
    ├── echo_server.py                 # 本地回显服务：127.0.0.1:8899，把请求要素回显成 JSON
    ├── ticket_service.py              # 模拟工单服务：127.0.0.1:8898，登录发令牌、工单增查、SSE 事件流
    └── 01/                            # 第 01 篇配套（脚本 + 测试案例 + 实跑证据）
        ├── first.js                   # 最小 k6 脚本：1 VU / 5s，阈值 + 检查
        ├── ticket_flow.js             # 工单业务流：登录 → 列表 → 详情 → 创建
        ├── sse_demo.js                # SSE 事件流：登录后收流并按 data: 计数断言
        ├── 测试案例-工单模拟服务.md      # API-01～14 与 RUN-01～03 用例及通过记录
        ├── 本地实跑记录-2026-10-13.md   # first.js 两轮命令行对照与环境口径说明
        ├── run-*.txt                  # 7 份 k6 原始终端输出（含 THRESHOLDS / TOTAL RESULTS）
        └── *.log / sse-stream.txt 等  # 服务访问日志、SSE 原始流、异常输入 400 处置证据
```

## 🚀 快速开始

```bash
# 1) 启动本地被测服务（按篇所需任选，各占一个终端；前置条件：对应端口空闲）
cd examples
python echo_server.py       # 回显服务，监听 127.0.0.1:8899
python ticket_service.py    # 模拟工单服务，监听 127.0.0.1:8898

# 自测：curl http://127.0.0.1:8899/ 与 curl http://127.0.0.1:8898/
# 应分别返回带 "k6-echo" / "k6-ticket-demo" 的 JSON 首页

# 2) 运行第 01 篇脚本（另开终端）
cd 01
k6 run first.js                            # 最小脚本，默认 1 VU / 5s
k6 run --vus 2 --duration 5s first.js      # 命令行覆盖负载，观察迭代数变化
k6 run ticket_flow.js                      # 工单业务流（需先启动 8898 工单服务）
k6 run sse_demo.js                         # SSE 事件流断言（需先启动 8898 工单服务）

# 3) 不改脚本切换被测目标：脚本统一从环境变量读取 BASE_URL
k6 run -e BASE_URL=http://127.0.0.1:8899 first.js
```

每条命令的完整原始输出（含 THRESHOLDS 与 TOTAL RESULTS 各节）保存在 `examples/01/run-*.txt`，可先看证据再动手复跑。环境准备（k6 安装等）见下方「实跑口径与版本基线」及 [k6 官方安装文档](https://grafana.com/docs/k6/latest/install/)。

## 📚 专栏篇目与配套状态

| 篇号 | 标题 | 层级 | 本仓库配套 |
|---|---|---|---|
| 00 | 为什么是 k6：AI 时代的性能测试工具选型 | 入门 | 无本地脚本（跟练用公开示例端点） |
| 01 | 十分钟跑通 k6：安装、命令行与第一个脚本 | 入门 | ✅ `examples/01/`（3 个脚本 + 测试案例 + 实跑记录） |
| 02 | 脚本结构与生命周期：init、setup、default 与 teardown | 入门 | 待更新 |
| 03 | HTTP 请求、标签与参数化 | 入门 | 规划：默认目标为 `examples/echo_server.py` |
| 04 | 检查与阈值：把性能门禁写进脚本 | 入门 | 待更新 |
| 05 | 内置指标与结果摘要怎么看 | 入门 | 待更新 |
| 06 | VU、迭代、负载模型与 6 类测试类型 | 入门 | 待更新 |
| 07 | 六种执行器与多场景组合 | 进阶 | 待更新 |
| 08 | 事务分组与 URL 粒度分析 | 进阶 | 待更新 |
| 09 | 自定义指标与标签体系 | 进阶 | 待更新 |
| 10 | 结果输出与报告体系 | 进阶 | 待更新 |
| 11 | InfluxDB 与 Grafana 实时监控栈 | 进阶 | 待更新 |
| 12 | 脚本录制与转换：HAR、Postman 与 OpenAPI | 进阶 | 待更新 |
| 13 | WebSocket 与 gRPC 协议测试 | 进阶 | 待更新 |
| 14 | 脚本工程化：模块化与配置管理 | 进阶 | 待更新 |
| 15 | xk6 扩展：Kafka、MySQL 与 Redis | 精通 | 待更新 |
| 16 | 分布式压测：负载分割与多机协同 | 精通 | 待更新 |
| 17 | k6 Operator：Kubernetes 上的分布式压测 | 精通 | 待更新 |
| 18 | k6 Cloud：云端压测与团队协作 | 精通 | 待更新 |
| 19 | 浏览器测试与 Web Vitals 采集 | 精通 | 待更新 |
| 20 | k6 v2 迁移与版本基线 | 精通 | 待更新 |
| 21 | CI/CD 集成与性能回归门禁 | 精通 | 待更新 |
| 22 | AI 时代的 k6：脚本生成与智能分析 | 综合实战 | 待更新 |
| 23 | 综合实战：工单系统的 k6 全链路压测 | 综合实战 | 规划：复用 `examples/ticket_service.py` 工单案例 |

配套状态随专栏正文发布逐步补充，以各篇正文引用的路径为准；尚未发布的篇目不提前放置半成品脚本。

## 🗂️ 目录与命名约定

- **按篇组织**：第 NN 篇的配套资产统一放在 `examples/NN/`（两位篇号，如 `examples/01/`）。
- **脚本命名**：小写 snake_case（`first.js`、`ticket_flow.js`），可直接 `k6 run` 执行。
- **原始输出**：`run-<脚本>-<并发>-<时长>-output.txt` 保存 k6 完整终端输出，未经删改。
- **日期证据**：文件名带 `-YYYYMMDD`（如 `api-error-inputs-20261013.txt`）、说明文档带 `-YYYY-MM-DD`，每个证据可定位到具体日期与环境。
- **中文说明文档**：`本地实跑记录-*`（环境、命令与读数口径）、`测试案例-*`（用例清单与通过状态）。

## 🧪 实跑口径与版本基线

- 专栏与仓库均以 **k6 v2.x** 为基线；k6 v1 专属能力不在示例范围内，v1→v2 迁移话题见专栏第 20 篇。
- 已验证实跑环境：Windows amd64、k6 v2.2.0、Python 3.13.2、curl 8.15.0，记录日期 2026-10-13，明细见 [examples/01/本地实跑记录-2026-10-13.md](examples/01/本地实跑记录-2026-10-13.md)。
- 示例读数只用于验证安装、请求流程与判定口径，不作为容量、稳定性或工具性能排名的结论依据；更换被测目标用 `-e BASE_URL=...`，不改脚本。
- 各篇正文发布前会在写作时的现行 k6 版本上重跑示例；如你本地版本更新导致输出有差异，以官方文档口径为准。

## ⚠️ 注意事项

1. **端口占用**：启动服务前确认 `8899`、`8898` 端口空闲；被占用时先停掉占用进程再启动。
2. **服务状态**：模拟工单服务的数据在内存中（预置 5 张工单），重启即还原；SSE 事件流推送的是当前内存中的全部工单，跟练中新建过工单则事件数会多于 5。
3. **切换被测目标**：脚本统一从环境变量读取 `BASE_URL`，用 `k6 run -e BASE_URL=...` 覆盖默认值，不要直接改脚本。
4. **证据文件**：`run-*.txt` 等证据是特定日期、特定环境的原始记录，仅供对照学习；复跑以你本机输出为准。
5. **无环境地址与凭据**：仓库不含任何真实环境地址、账号或密钥；对外部目标压测请自行获得授权。
6. **正文与代码分工**：专栏讲解正文（含每个示例的完整说明）请在 [CSDN 专栏](https://blog.csdn.net/zuozewei/category_13216606.html)阅读；本仓库只提供代码与证据资产。

## 📄 相关链接

- [k6 官方文档](https://grafana.com/docs/k6/latest/)
- [grafana/k6 GitHub 仓库](https://github.com/grafana/k6)
- 专栏《k6 性能测试从入门到精通》：[CSDN 专栏地址](https://blog.csdn.net/zuozewei/category_13216606.html)，讲解正文与完整目录

## 📮 关注公众号

微信公众号 **7DGroup**：性能工程实战内容，专栏更新与配套资料动态。

<p align="center">
  <img src="images/wechat-7dgroup-qr.jpg" width="180" alt="7DGroup 微信公众号二维码">
</p>

- 📣 微信公众号：**7DGroup**
- 🏢 主组织：[github.com/7dgroup-ai](https://github.com/7dgroup-ai)
