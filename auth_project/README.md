# Auth Project API

## Authentication
All endpoints require JWT authentication. Obtain a token via `/api/login/` and include it in the `Authorization` header as `Bearer <your_token>`.

## Endpoints

### User Registration
- **POST** `/api/register/`
  - **Body:**
    - `username`: string (required)
    - `email`: string (required)
    - `password`: string (required)
    - `photo`: image file (optional, JPEG/PNG/WebP, max 2MB, auto-cropped to 1:1)
  - **Headers:** `Content-Type: multipart/form-data`
  - **Sample Request (form-data):**
    - username: user
    - email: user@email.com
    - password: pass
    - photo: (attach file)
  - **Sample Response:**
    ```json
    {
      "username": "user",
      "email": "user@email.com",
      "photo": "/media/user_photos/yourphoto.jpg"
    }
    ```

### Login (JWT Token)
- **POST** `/api/login/`
  - **Body:** `{ "username": "user", "password": "pass" }`
  - **Response:** `{ "refresh": "...", "access": "..." }`

### Token Refresh
- **POST** `/api/token/refresh/`
  - **Body:** `{ "refresh": "..." }`
  - **Response:** `{ "access": "..." }`

### Protected Example
- **GET** `/api/protected/`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Response:** `{ "message": "Authenticated access granted" }`

---

## Post CRUD
- **List Posts:**
  - **GET** `/api/posts/`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Response:** `[ { "id": 1, "user": "user", "title": "...", "content": "...", ... } ]`
- **Create Post:**
  - **POST** `/api/posts/`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Body:** `{ "title": "...", "content": "..." }`
  - **Response:** `{ "id": 1, "user": "user", "title": "...", "content": "...", ... }`
- **Retrieve Post:**
  - **GET** `/api/posts/{id}/`
  - **Headers:** `Authorization: Bearer <access_token>`
- **Update Post:**
  - **PUT/PATCH** `/api/posts/{id}/`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Body:** `{ "title": "new", "content": "new" }`
- **Delete Post:**
  - **DELETE** `/api/posts/{id}/`
  - **Headers:** `Authorization: Bearer <access_token>`

## Comment CRUD
- **List Comments:**
  - **GET** `/api/comments/`
  - **Headers:** `Authorization: Bearer <access_token>`
- **Create Comment:**
  - **POST** `/api/comments/`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Body:** `{ "post": 1, "text": "..." }`
- **Retrieve Comment:**
  - **GET** `/api/comments/{id}/`
  - **Headers:** `Authorization: Bearer <access_token>`
- **Update Comment:**
  - **PUT/PATCH** `/api/comments/{id}/`
  - **Headers:** `Authorization: Bearer <access_token>`
  - **Body:** `{ "text": "new" }`
- **Delete Comment:**
  - **DELETE** `/api/comments/{id}/`
  - **Headers:** `Authorization: Bearer <access_token>`

---

## Rate Limiting
All endpoints are rate-limited to 5 requests per minute per user (if authenticated) or per IP (if unauthenticated). If you exceed this limit, you will receive a 429 Too Many Requests error.

- **429 Too Many Requests:**
  - **Response:** `{ "detail": "Too many requests. Please try again later." }`

---

## Error Handling
- **401 Unauthorized:** Returned if token is missing or invalid.
- **403 Forbidden:** Returned if you try to modify/delete another user's post or comment.
- **400 Bad Request:** For invalid data.
- **429 Too Many Requests:** Returned if you exceed the allowed number of requests per minute.
  - **Sample Response:** `{ "detail": "Too many requests. Please try again later." }`

---

## Github Repository
- _Add your Github repository link here._ 