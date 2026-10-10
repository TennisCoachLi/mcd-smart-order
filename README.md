# 麦麦智能点餐 · 省钱补给助手（mcd-smart-order）

> 2026 麦当劳程序员创意开发大赛 · 参赛作品
> 基于 **麦当劳中国官方 MCP（mcd-mcp）** 能力，用 WorkBuddy 开发的创意 Skill。

一个给「想省钱、想就近、想吃得明白」的用户打造的 AI 点餐助手。它把麦当劳 MCP 的 35 个工具编排成 6 条可落地工作流：**省钱领券 → 比价 → 就近点餐 → 积分兑换 → 查活动**，还能从运动补给视角（高蛋白、训练后 30 分钟补给）帮网球教练 / 运动人群点餐。

---

## 🎯 项目介绍

| 维度 | 内容 |
|------|------|
| 参赛赛道 | 基于麦当劳 MCP 开发创意 Skill（点餐助手 / 省钱助手 / 活动推荐助手） |
| 开发工具 | **WorkBuddy**（本 Skill 即由 WorkBuddy 编写、调试、自测） |
| 依赖 MCP | 麦当劳中国 `mcd-mcp`（远程托管，Streamable HTTP） |
| 适用人群 | 想省钱的普通消费者、运动人群（训练补给）、企业团餐 |
| 核心卖点 | 一键领券 + 用券比价 + 就近门店 + 积分不浪费 |

**5 条工作流**
1. 💰 **省钱模式**：`auto-bind-coupons` 一键领券 → `query-my-coupons` / `query-store-coupons` 看券 → `calculate-price` 对比用券前后价 → `create-order`。
2. 🏃 **训练补给模式**：`list-nutrition-foods` 筛高蛋白餐 → `query-meal-detail` 看可替换项 → 算价下单。
3. 📍 **就近点餐 / 外送**：`query-nearby-stores` / `delivery-query-stores` → 选品 → 下单。
4. 🎟 **积分玩法**：`query-my-account` 看即将过期积分 → `mall-points-products` 兑换 → `draw-lottery` 抽奖。
5. 📅 **活动 / 派对**：`campaign-calendar` 看当月活动 → `query-party-*` 预约派对。
6. 🍗 **个性化点餐 / 口味偏好**：先问「今天吃哪种肉、烤还是炸」，按偏好筛菜单；点名经典单品时主动给解腻均衡建议。

## 👥 目标用户

- 💸 **想省钱的普通消费者**：每次点餐前自动领券、用券比价，不漏一张可用券。
- 🎾 **运动人群 / 教练**（如网球教练训练后补给）：按官方营养数据筛高蛋白餐，训练后 30 分钟内快速补给。
- 🧑‍💼 **忙碌上班族**：就近门店 / 外送一条链路走完，不用在 App 里反复跳转。
- 🎁 **积分持有者**：即将过期积分主动提醒并推荐兑换方案，积分不浪费。
- 👪 **家庭 / 团建组织者**：麦麦派对、团餐活动查询与预约。

---

## 💡 设计理念：为什么做这个 Skill

这个 Skill 不是凭空想的——它源于作者对麦当劳官方点餐 App / 小程序的几点真实不满：**优惠券散、领了要等下周才能用又容易忘、结算页强制顺手加购很烦、营养信息不透明、积分活动看不懂**。

解法是用官方 MCP 把同一套能力重新组合，做一个**更克制、更尊重用户、更省心**的助手：

| 官方 App 的别扭 | 本 Skill 的做法 |
|---|---|
| 券散在各处、漏券 | 点餐前一键聚合所有券 + 比价，不漏一张 |
| 领了下周才能用、又忘了（还被催开提醒） | 按「现在能用 / 下周才能用」分组，只推现在能用的，其余给一次性安静摘要，绝不推送骚扰 |
| 结算页强制「顺手加个什么」 | 没有加购环节，你说要什么就只给什么，下单前只复述方案 |
| 营养要点好几层 | 一句话问出热量 / 蛋白质 |
| 积分活动看不懂 | 主动提示「积分怎么花最值」+ 当月活动一并说清 |

完整设计动机与解法对照见 [DESIGN.md](./DESIGN.md)。

---

## 🚀 安装方法（MCP 接入与本地安装）

### 1. 申请麦当劳 MCP Token
1. 打开 https://open.mcd.cn/mcp ，右上角【登录】→ 手机号验证登录。
2. 点右上角【控制台】→【激活】申请 MCP Token → 一键复制。
3. 协议：每个 Token 限流 **600 次/分钟**（超了返回 429）。

### 2. 在 WorkBuddy 接入 mcd-mcp
把下面 JSON 粘贴到 WorkBuddy 的「连接器 / MCP」配置中，替换 `YOUR_MCP_TOKEN`：

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

### 3. 安装本 Skill（可选，用于本地直接调用）
把本仓库的 `SKILL.md` 复制到 WorkBuddy 用户级 skills 目录：

```bash
mkdir -p ~/.workbuddy/skills/mcd-smart-order
cp SKILL.md ~/.workbuddy/skills/mcd-smart-order/
```

### 4. 安装本 Skill 后的使用示例

接入后直接对 WorkBuddy 说：

- 「帮我看看附近麦当劳，领券后点一份训练后吃的，要高蛋白」
- 「我积分快过期了，有什么能换的」
- 「麦当劳这个月有啥活动」
- 「不想出门，把餐送到公司」

完整示例对话见 [examples/dialog.md](./examples/dialog.md)。

### 5. 命令行直接调用（scripts/mcd_mcp_client.py）
零依赖，仅用 Python 标准库：

```bash
export MCD_MCP_TOKEN="你的Token"
python scripts/mcd_mcp_client.py list        # 列出全部 35 个工具
python scripts/mcd_mcp_client.py nutrition   # 示例：查餐品营养
python scripts/mcd_mcp_client.py coupons     # 示例：一键领麦麦省券
python scripts/mcd_mcp_client.py account     # 示例：查我的积分
python scripts/mcd_mcp_client.py calendar    # 示例：查当月活动
python scripts/mcd_mcp_client.py call list-nutrition-foods '{}'  # 任意工具调用
```

---

## 📂 目录结构

```
mcd-smart-order/
├── SKILL.md                      # 核心 Skill 定义（WorkBuddy 加载）
├── README.md                     # 本文件（项目介绍/安装方法/使用示例/目标用户）
├── DESIGN.md                     # 原创设计理念（痛点 → 解法对照）
├── MCP_INTEGRATION.md            # 麦当劳 MCP Server/Tool/调用流程/业务价值
├── CONTEST_DECLARATION.md        # 参赛声明（官方原文，未改动）
├── workbuddy.md                  # 使用 WorkBuddy 开发的对话上下文
├── ISSUE_TEMPLATE.md             # 报名 Issue 格式速查
├── scripts/
│   └── mcd_mcp_client.py        # 零依赖 MCP 命令行客户端
└── examples/
    └── dialog.md                # 示例对话（省钱 / 补给 / 积分）
```

---

## 📜 参赛声明

完整参赛声明见 [CONTEST_DECLARATION.md](./CONTEST_DECLARATION.md)（官方原文，内容未作任何改动）。要点：

1. 本作品为 **2026 麦当劳程序员创意开发大赛** 个人参赛项目，由作者使用 **WorkBuddy** 独立完成开发，仅用于非商业的参赛演示与个人学习。
2. 使用麦当劳 MCP 服务已遵守《麦当劳 MCP 服务规则》及《使用条款》，未对服务做任何逆向、破解或绕过限制的行为。
3. 仓库所有配置仅使用环境变量占位符，不含任何真实 Token、密钥或账号凭证。
4. 仓库内容按「现状」提供，不构成任何形式的保证；麦当劳及其关联方的商标权归其所有。

---

© 2026 参赛作者 · 基于麦当劳中国 mcd-mcp 构建
