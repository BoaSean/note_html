# 快速开始

欢迎使用本 API 手册。

## Base URL

```
https://api.example.com/v1
```

## 请求格式

所有请求使用 JSON，需设置 `Content-Type: application/json`：

```
POST /v1/users
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "张三",
  "email": "zhangsan@example.com"
}
```

## 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码，0 表示成功 |
| message | string | 状态描述 |
| data | object/array | 返回数据 |
