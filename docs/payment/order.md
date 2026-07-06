# 支付 API

## 创建订单

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/v1/orders` |

### 请求体

```json
{
  "amount": 9900,
  "currency": "CNY",
  "description": "会员订阅",
  "notify_url": "https://example.com/callback"
}
```

### 响应

```json
{
  "code": 0,
  "data": {
    "order_id": "ORD20250624001",
    "amount": 9900,
    "status": "pending",
    "pay_url": "https://pay.example.com/ORD20250624001"
  }
}
```

---

## 查询订单

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/v1/orders/:id` |

### 响应

```json
{
  "code": 0,
  "data": {
    "order_id": "ORD20250624001",
    "amount": 9900,
    "status": "paid",
    "paid_at": "2025-06-24T15:30:00Z"
  }
}
```

---

## 退款

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/v1/orders/:id/refund` |

### 请求体

```json
{ "reason": "用户取消订单" }
```

### 响应

```json
{ "code": 0, "data": { "refund_id": "REF20250624001", "status": "processing" } }
```
