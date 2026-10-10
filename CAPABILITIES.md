# 麦当劳 MCP 能力清单（mcd-mcp，共 35 个工具）

> 本文件由真实 Token 实连 `tools/list` 核验（2026-10-10），列出本 Skill 可用的全部麦当劳 MCP 工具及「能做什么」。
> 用途：方便作者 / 评审快速了解能力边界，也便于基于此设计更多「有趣组合」。

## 一、点餐链路（菜单 / 详情 / 算价 / 下单）
- `query-meals`：查在售餐品列表（到店/外送），含价格与团餐搭配区间。
- `query-meal-detail`：查套餐构成、可替换项、是否可特调。
- `query-store-coupons`：查某门店当前可用的券（下单校验口径）。
- `query-my-coupons`：查用户卡包里的券（展示/管理口径）。
- `calculate-price`：算价（含优惠），支持到店/外送。
- `create-order`：下单，返回支付/取餐凭证。
- `cancel-order`：取消订单。
- `query-order`：订单详情。
- `order-list`：历史订单。

## 二、门店 / 外送
- `query-nearby-stores`：附近门店（到店/得来速）。
- `delivery-query-addresses`：我的外卖地址。
- `delivery-create-address`：新建外卖地址。
- `delivery-query-stores`：某地址可配送门店。

## 三、优惠券 / 省钱
- `available-coupons`：麦麦省可领券列表。
- `auto-bind-coupons`：一键领当前所有可领券。
- `query-survey-coupon`：按订单号查满意度答卷 + 关联奖券（标题/核销状态/适用方式）。

## 四、营养
- `list-nutrition-foods`：餐品营养/热量/蛋白质。

## 五、积分 / 商城 / 抽奖
- `query-my-account`：积分账户（可用/即将过期）。
- `mall-points-products`：积分商城可兑换商品。
- `mall-product-detail`：商品详情（SKU 规格）。
- `mall-create-order`：积分兑换下单（得券码）。
- `mall-order-list`：商城订单列表。
- `mall-order-detail`：商城订单详情。
- `query-lottery-info`：抽奖活动信息。
- `draw-lottery`：抽奖。
- `query-my-prizes`：我的抽奖奖品。

## 六、活动 / 派对
- `campaign-calendar`：当月营销活动日历。
- `query-party-city`：支持派对的城市。
- `query-party-store`：城市下可办派对门店。
- `query-party-store-date`：门店可预约日期。
- `query-party-store-session`：日期下可预约时段。
- `party-order-create`：创建派对订单。

## 七、辅助 / 团餐
- `now-time-info`：当前时间（用于「今天/本周/即将过期」校准）。
- `query-meal-assistance`：团餐助餐。
- `query-promotions`：企业团餐满减/满折促销规则。

## 八、有趣组合种子（抛砖引玉）
- **省钱 × 营养**：领券 → 按营养目标筛餐 → 用券比价 → 出「最划算的健康方案」。
- **肉种偏好 × 菜单**：先问鸡肉/牛肉/鱼肉 + 烤/炸 → 用 `query-meals`/`query-meal-detail` 过滤 → 解腻搭配建议。
- **积分 × 活动 × 抽奖**：看积分 → 看当月活动 → 抽奖得券 → 券再用于下单。
- **满意度奖券闭环**：`query-survey-coupon` 查订单关联奖券核销状态 → 未核销的券回到下单链路。
- **团餐最优搭**：`query-promotions` 满减规则 + `query-meal-assistance` → 团餐省钱组合。
