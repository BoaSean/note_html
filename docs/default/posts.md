# 文章模块

## 获取文章列表

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/v1/posts` |

### 参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| page | int | 1 | 页码 |
| per_page | int | 10 | 每页数量 |
| status | string | published | `draft` / `published` |

### 响应

```json
{
  "code": 0,
  "data": {
    "items": [
      { "id": 1, "title": "Hello World", "status": "published", "created_at": "2025-06-01T08:00:00Z" }
    ],
    "total": 42
  }
}
```

---

## 获取文章详情

| 项目 | 内容 |
|------|------|
| **方法** | `GET` |
| **路径** | `/v1/posts/:id` |

### 响应

```json
{
  "code": 0,
  "data": {
    "id": 1,
    "title": "Hello World",
    "content": "Markdown 正文...",
    "author": { "id": 1, "username": "zhangsan" },
    "status": "published",
    "created_at": "2025-06-01T08:00:00Z"
  }
}
```

---

## 创建文章

| 项目 | 内容 |
|------|------|
| **方法** | `POST` |
| **路径** | `/v1/posts` |

### 请求体

```json
{
  "title": "新文章",
  "content": "Markdown 正文...",
  "status": "draft"
}
```

### 响应

```json
{ "code": 0, "data": { "id": 3, "status": "draft" } }
```

---

## 删除文章

| 项目 | 内容 |
|------|------|
| **方法** | `DELETE` |
| **路径** | `/v1/posts/:id` |

### 响应

```json
{ "code": 0, "data": null }
```
