# workbuddy.md —— 使用 WorkBuddy 开发本项目的过程记录

> 本文件用于核验「使用 WorkBuddy 开发」的联动活动奖励条件。
> 本项目由作者于 2026-10-09 在 WorkBuddy（Mac 端）中，通过 AI 对话方式完成构思、开发、调试与自测。
> 出于信息安全要求（见 CONTEST_DECLARATION.md），本文不包含任何真实 MCP Token。

## 一、开发过程（对话上下文摘要）

### 第 1 轮：了解赛事
- 用户提供了麦当劳 × WorkBuddy 程序员创意开发大赛的公众号文章链接，要求查看比赛内容。
- WorkBuddy 抓取文章确认：赛事时间 2026-10-09 至 10-25，要求基于麦当劳 MCP 开发创意 Skill、开源到 GitHub 并按 Issue 报名；使用 WorkBuddy 开发可获积分专项奖励。
- 用户明确目标：参赛获得 WorkBuddy 3000 积分专项奖励。

### 第 2 轮：调研麦当劳 MCP 能力
- WorkBuddy 检索并抓取官方仓库 M-China/mcd-mcp-server 的 README，确认：
  - 接入地址 `https://mcp.mcd.cn`，Streamable HTTP，Bearer Token 鉴权；
  - Token 在 open.mcd.cn/mcp 用手机号申请，限流 600 次/分钟；
  - 工具覆盖点餐、外送、领券、营养、积分商城、抽奖、活动派对等场景。

### 第 3 轮：开发 Skill（WorkBuddy 生成全部代码与文档）
- 编写 `SKILL.md`：编排 mcd-mcp 工具为 5 条工作流（省钱 / 训练补给 / 就近点餐 / 积分玩法 / 活动派对）。
- 编写 `scripts/mcd_mcp_client.py`：零依赖（仅 Python 标准库）的 MCP Streamable HTTP 客户端，支持 initialize / tools/list / tools/call。
- 编写 README、报名 Issue 模板与示例对话。
- 全部文件由 WorkBuddy 直接写入本地项目目录，并完成 git 初始化与提交。

### 第 4 轮：自测与问题排查（真实产品验证）
- 语法验证：`python -m py_compile` 通过。
- 连通性验证：无 Token 请求返回 403（未提供鉴权）、假 Token 返回 401（鉴权码无效），证明握手请求格式正确。
- 排查过程中发现边缘节点对个别请求特征偶发 403，通过改用标准 `urlopen` 并增加 UA 头解决；同时在错误提示上区分「未配置 Token（403）」与「Token 失效（401）」。

### 第 5 轮：真实 Token 端到端验证
- 用户提供真实 MCP Token（仅以环境变量方式临时传入，未写入任何文件或 git 记录）。
- 实连 `tools/list` 返回 **35 个工具**，据此修正文档：工具数 37 → 35；修正派对工具实际名称（`query-party-store-date` / `query-party-store-session`）；补充此前遗漏的 `query-promotions`、`query-survey-coupon`。
- 实跑 `tools/call` 调用 `campaign-calendar`，成功返回 2026 年 10 月真实活动日历，证明 initialize → tools/list → tools/call 全链路可用。

### 第 6 轮：按官方赛事要求重构仓库
- WorkBuddy 抓取官方活动仓库 M-China/mcd-developer-innovation-challenge 的 README 与规则，确认参赛项目必须包含：README.md（项目介绍/安装方法/使用示例/目标用户）、MCP_INTEGRATION.md、CONTEST_DECLARATION.md（官方原文不可改动）、源代码，以及用于 WorkBuddy 专项奖励的 workbuddy.md。
- 下载官方 CONTEST_DECLARATION.md（未改动原文），新增 MCP_INTEGRATION.md 与本文件，补全 README 的「目标用户 / 安装方法 / 使用示例」章节，并将报名 Issue 模板改为官方标准格式（不超过 1000 字、无图片）。

## 二、WorkBuddy 在本项目中的实际作用

- 📄 生成全部核心文件：SKILL.md、mcd_mcp_client.py、README、MCP_INTEGRATION.md、示例对话。
- 🧪 执行自测：语法编译、无 Token / 假 Token / 真 Token 三态连通性验证、真实工具调用。
- 🔍 事实核查：实连核验工具清单，纠正了官方 README 中工具数量与实际下发数量不一致的问题（37 → 35）。
- 📦 版本管理：git 初始化与两次提交（初版 + 工具清单校正）。
