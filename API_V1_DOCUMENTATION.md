# ADET REST API - V1 Documentation

This document covers **only V1** of the API implemented in `server/service.php` and its database setup in `server/connection.php`.

## Base URL

- Default local URL: `http://localhost/adet-rest-api/server/service.php`
- All routes are selected via query parameter: `?action=<route_name>`

Examples:
- `POST /adet-rest-api/server/service.php?action=register`
- `GET /adet-rest-api/server/service.php?action=users`

## Content Type

- Request body (when required): JSON
- Response: JSON (`Content-Type: application/json; charset=UTF-8`)

## Response Format

All endpoints return the same envelope:

```json
{
  "status": "success | error",
  "message": "Human-readable message",
  "data": {}
}
```

Notes:
- `data` can be an object, an array, or `null`.
- Error responses still use the same JSON structure.

## Database Behavior (V1)

On startup, the API auto-provisions:
- Database: `user_api`
- Table: `users`

`users` table columns:
- `id` (INT, auto increment, primary key)
- `username` (VARCHAR(100), required)
- `email` (VARCHAR(150), required, unique)
- `password` (VARCHAR(255), required, hashed)
- `created_at` (TIMESTAMP, default current timestamp)

## Validation Rules (V1)

### Username
- Required for registration and update
- Length must be 3 to 50 characters
- Allowed characters: letters, numbers, underscore (`_`), dash (`-`)

### Email
- Required for registration, login, update
- Must be valid email format
- Must be unique for registration

### Password
- Required for registration and login
- Minimum length: 8 characters
- Stored using PHP `password_hash`
- Verified using PHP `password_verify`

## Endpoints

## 1) Register User

- Method: `POST`
- Action: `register`
- URL: `/adet-rest-api/server/service.php?action=register`

Request body:

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "supersecret123"
}
```

Success:
- Status code: `201`

Example response:

```json
{
  "status": "success",
  "message": "User registered successfully",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

Common errors:
- `400`: missing required fields
- `400`: invalid username
- `400`: invalid email
- `400`: password too short
- `409`: email already exists
- `500`: registration failed

## 2) Login

- Method: `POST`
- Action: `login`
- URL: `/adet-rest-api/server/service.php?action=login`

Request body:

```json
{
  "email": "john@example.com",
  "password": "supersecret123"
}
```

Success:
- Status code: `200`

Example response:

```json
{
  "status": "success",
  "message": "Login successful",
  "data": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

Common errors:
- `400`: email/password missing
- `401`: invalid email or password

## 3) Get All Users

- Method: `GET`
- Action: `users`
- URL: `/adet-rest-api/server/service.php?action=users`

Success:
- Status code: `200`

Example response:

```json
{
  "status": "success",
  "message": "Users retrieved successfully",
  "data": [
    {
      "id": 1,
      "username": "john_doe",
      "email": "john@example.com",
      "created_at": "2026-04-17 10:00:00"
    }
  ]
}
```

## 4) Get User by ID

- Method: `GET`
- Action: `user`
- URL: `/adet-rest-api/server/service.php?action=user&id=<id>`

Example:
- `/adet-rest-api/server/service.php?action=user&id=1`

Success:
- Status code: `200`

Common errors:
- `404`: user not found

## 5) Update User

- Method: `PUT`
- Action: `update_user`
- URL: `/adet-rest-api/server/service.php?action=update_user&id=<id>`

Request body:

```json
{
  "username": "john_updated",
  "email": "john_updated@example.com"
}
```

Success:
- Status code: `200`

Common errors:
- `400`: invalid user id
- `400`: missing username/email
- `400`: invalid username/email format
- `404`: user not found
- `500`: update failed

## 6) Delete User

- Method: `DELETE`
- Action: `delete_user`
- URL: `/adet-rest-api/server/service.php?action=delete_user&id=<id>`

Success:
- Status code: `200`

Common errors:
- `400`: invalid user id
- `404`: user not found
- `500`: delete failed

## 7) Fallback / Unknown Endpoint

If no method/action pair matches:
- Status code: `404`
- Message: `Endpoint not found`

## Quick cURL Examples

Register:

```bash
curl -X POST "http://localhost/adet-rest-api/server/service.php?action=register" \
  -H "Content-Type: application/json" \
  -d '{"username":"john_doe","email":"john@example.com","password":"supersecret123"}'
```

Login:

```bash
curl -X POST "http://localhost/adet-rest-api/server/service.php?action=login" \
  -H "Content-Type: application/json" \
  -d '{"email":"john@example.com","password":"supersecret123"}'
```

Get users:

```bash
curl "http://localhost/adet-rest-api/server/service.php?action=users"
```

Get user by id:

```bash
curl "http://localhost/adet-rest-api/server/service.php?action=user&id=1"
```

Update user:

```bash
curl -X PUT "http://localhost/adet-rest-api/server/service.php?action=update_user&id=1" \
  -H "Content-Type: application/json" \
  -d '{"username":"john_updated","email":"john_updated@example.com"}'
```

Delete user:

```bash
curl -X DELETE "http://localhost/adet-rest-api/server/service.php?action=delete_user&id=1"
```

## Python Client Mapping (V1)

- `client/client_auth.py`
  - `register` -> `POST ?action=register`
  - `login` -> `POST ?action=login`
- `client/client_users.py`
  - `get_all_users` -> `GET ?action=users`
  - `get_user_by_id` -> `GET ?action=user&id=<id>`
  - `update_user` -> `PUT ?action=update_user&id=<id>`
  - `delete_user` -> `DELETE ?action=delete_user&id=<id>`

## Scope Note

This document is intentionally limited to **V1** and excludes all files in `V2/`.
