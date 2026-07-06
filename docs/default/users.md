# 用户模块

## 获取用户列表

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/v1/users` |

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| per_page | int | 20 | 每页数量 |

### 响应

```json
{
  "code": 0,
  "data": {
    "items": [
      { "id": 1, "username": "zhangsan", "email": "zhangsan@example.com", "status": "active" }
    ],
    "total": 150
  }
}
```

---

## 获取用户详情

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/v1/users/:id` |

### 响应

```json
{
  "code": 0,
  "data": {
    "id": 1,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "phone": "13800138000",
    "bio": "全栈开发者",
    "status": "active"
  }
}
```

---

## 创建用户

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/v1/users` |

### 请求体

```json
{
  "username": "lisi",
  "email": "lisi@example.com",
  "password": "P@ssw0rd!"
}
```

### 响应

```json
{
  "code": 0,
  "data": { "id": 2, "username": "lisi", "status": "active" }
}
```

---

## 更新用户

| 项目 | 内容 |
|------|------|
| **方法** | `PUT` |
| **路径** | `/v1/users/:id` |

### 请求体

所有字段可选，只传需更新的。

```json
{
  "bio": "DevOps 工程师"
}
```

### 响应

```json
{
  "code": 0,
  "data": { "id": 1, "bio": "DevOps 工程师" }
}
```

---

## 删除用户

| 项目 | 内容 |
|------|------|
| **方法** | `DELETE` |
| **路径** | `/v1/users/:id` |

### 响应

```json
{
  "code": 0,
  "data": null
}
```
