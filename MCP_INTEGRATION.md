# MCP 集成说明（MCP_INTEGRATION.md）

本文说明本项目实际使用的麦当劳 MCP Server、使用的 Tool、调用流程与业务价值。

## 一、使用的 MCP Server

| 项目 | 内容 |
|------|------|
| Server | 麦当劳中国官方 `mcd-mcp`（io.github.M-China-Official/mcd-mcp） |
| 接入地址 | `https://mcp.mcd.cn` |
| 传输协议 | Streamable HTTP |
| 鉴权方式 | 请求头 `Authorization: Bearer <MCP_TOKEN>`（Token 在 https://open.mcd.cn/mcp 申请） |
| 限流 | 600 次/分钟（超限返回 429） |
| 核验情况 | 2026-10-09 使用真实 Token 实连 `tools/list`，返回 **35 个工具**，与本文件工具清单一致 |

## 二、使用的 Tool（共 35 个，已实连核验）

**点餐链路**：`query-nearby-stores` · `query-meals` · `query-meal-detail` · `query-store-coupons` · `query-my-coupons` · `calculate-price` · `create-order` · `cancel-order` · `query-order` · `order-list`
**外送**：`delivery-query-addresses` · `delivery-create-address` · `delivery-query-stores`
**省钱/领券**：`available-coupons` · `auto-bind-coupons` · `query-my-coupons`
**营养**：`list-nutrition-foods`
**积分/商城**：`query-my-account` · `mall-points-products` · `mall-product-detail` · `mall-create-order` · `mall-order-list` · `mall-order-detail` · `query-lottery-info` · `draw-lottery` · `query-my-prizes`
**活动/派对**：`campaign-calendar` · `query-party-city` · `query-party-store` · `query-party-store-date` · `query-party-store-session` · `party-order-create`
**辅助/团餐**：`now-time-info` · `query-meal-assistance` · `query-promotions` · `query-survey-coupon`

## 三、调用流程（5 条工作流）

### ① 省钱模式
```
auto-bind-coupons（一键领麦麦省券）
  → query-my-coupons / query-store-coupons（看可用券）
  → query-nearby-stores（附近门店）
  → query-meals + query-meal-detail（选品）
  → calculate-price（用券前后比价）
  → create-order（确认后下单）
```

### ② 训练补给模式
```
list-nutrition-foods（筛高蛋白/适中热量）
  → query-meal-detail（看套餐可替换项）
  → auto-bind-coupons + calculate-price（压到最低价）
  → create-order
```

### ③ 就近点餐 / 外送
```
now-time-info（校准时间）
  → query-nearby-stores / delivery-query-stores
  → query-meals → calculate-price → create-order
```

### ④ 积分玩法
```
query-my-account（看可用/即将过期积分）
  → mall-points-products + mall-product-detail（选品）
  → mall-create-order（积分兑换）/ draw-lottery（积分抽奖）
```

### ⑤ 活动 / 派对
```
campaign-calendar（当月活动）+ available-coupons（领活动券）
  → query-party-city → query-party-store → query-party-store-date
  → query-party-store-session → party-order-create（派对预约下单）
```

## 四、业务价值

- 💰 **省钱**：每次点餐前默认先领券再用券比价，用户能直接看到「原价 / 用券价」差额，避免漏券多花钱。
- 🏃 **吃得明白**：用官方营养数据按「高蛋白、适中热量」为运动人群筛训练后补给，而不是凭感觉推荐。
- ⏱ **省时**：附近门店、外送地址、下单一条链路走完，不用在 App 里反复跳转。
- 🎟 **积分不浪费**：主动提醒即将过期积分并推荐兑换方案。
- 🤝 **安全**：涉及 `create-order` 前必须复述「门店+商品+就餐方式+应付」并等用户确认，券一经使用不可撤回。

## 五、本地验证方式

```bash
export MCD_MCP_TOKEN="你的Token"
python scripts/mcd_mcp_client.py list        # 列出全部 35 个工具
python scripts/mcd_mcp_client.py calendar    # 实测：拉取当月活动日历
```

> 注：本仓库所有配置仅使用环境变量占位符，不含任何真实 Token（符合《参赛声明》信息安全要求）。
