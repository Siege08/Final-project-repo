# Django User Authentication API

This project provides a basic user authentication system using Django REST Framework and JWT.

## 🚀 API Endpoints

### 1. Register a New User
- **Method:** POST  
- **URL:** `/api/register/`
- **Body:**
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "yourpassword"
}
