
# ADET REST API - V2 Documentation (API Key + AI Execution)

This document covers the API implemented in `server/service.php` and `server/connection.php`, including integration with the Python AI socket server (`ai.py`).

---

## Base URL

- Default local URL:  
  `http://localhost/adet-rest-api/server/service.php`

- All routes use query parametersssssssssssss:
```

?action=<route_name>

```

### Examples
- `POST /adet-rest-api/server/service.php?action=generate_api`
- `POST /adet-rest-api/server/service.php?action=execute_ai`

---

## Content Type

- Request body: JSON
- Response: JSON  
```

Content-Type: application/json; charset=UTF-8

````

---

## Response Format

All endpoints return:

```json
{
"status": "success | error",
"message": "Human-readable message",
"data": {}
}
````

### Notes

* `data` can be object, array, or `null`

---

## Database Behavior

### Database

* SQLite file: `api_keys.db`

### Table: `api_keys`

| Column     | Type    | Description                 |
| ---------- | ------- | --------------------------- |
| id         | INTEGER | Primary key, auto increment |
| api_key    | TEXT    | Unique API key              |
| created_at | TEXT    | Timestamp                   |

* Table is auto-created on server startup.

---

## AI Server Integration

* Host: `127.0.0.1`
* Port: `1234`
* Protocol: TCP socket (newline-delimited JSON)

### Supported Commands

| Command  | Description        |
| -------- | ------------------ |
| ping     | Health check       |
| run      | Execute AI logic   |
| shutdown | Shutdown AI server |

---

## Endpoints

---

## 1) Generate API Key

* Method: `POST`
* Action: `generate_api`

### URL

```
/adet-rest-api/server/service.php?action=generate_api
```

### Description

* Generates a unique 32-character API key
* Ensures no duplicates in database

### Success Response (201)

```json
{
  "status": "success",
  "message": "API key generated successfully",
  "data": {
    "api_key": "abcd1234..."
  }
}
```

### Errors

* `500` - API generation failed

---

## 2) Execute AI

* Method: `POST`
* Action: `execute_ai`

### URL

```
/adet-rest-api/server/service.php?action=execute_ai
```

### Request Body

```json
{
  "api_key": "your_api_key",
  "month": 5,
  "raw": true
}
```

### Parameters

| Field   | Type   | Required | Description            |
| ------- | ------ | -------- | ---------------------- |
| api_key | string | Yes      | Must exist in database |
| month   | int    | Yes      | Number of items        |
| raw     | bool   | Yes      | Output format toggle   |

### Behavior

1. Validates API key
2. Connects to AI server
3. Sends:

```json
{
  "cmd": "run",
  "month": <month>,
  "raw": <raw>
}
```

4. Returns AI-generated data

### Success Response (200)

```json
{
  "status": "success",
  "message": "AI Execution is successful!",
  "data": [1,2,3,4,5]
}
```

### Errors

* `400` - Missing parameters
* `404` - API key not found
* `503` - AI server unavailable
* `500` - Invalid AI response

---

## 3) Get All API Keys

* Method: `GET`
* Action: `api_keys`

### URL

```
/adet-rest-api/server/service.php?action=api_keys
```

### Success Response (200)

```json
{
  "status": "success",
  "message": "API keys retrieved successfully",
  "data": [
    {
      "id": 1,
      "api_key": "abcd1234...",
      "created_at": "2026-04-17"
    }
  ]
}
```

### Errors

* `500` - Query failed

---

## 4) Delete API Key

* Method: `DELETE`
* Action: `delete_api_key`

### URL

```
/adet-rest-api/server/service.php?action=delete_api_key&api_key=<key>
```

### Success Response (200)

```json
{
  "status": "success",
  "message": "API key deleted successfully",
  "data": null
}
```

### Errors

* `400` - API key required
* `404` - API key not found
* `500` - Delete failed

---

## 5) Fallback / Unknown Endpoint

### Response (404)

```json
{
  "status": "error",
  "message": "Endpoint not found",
  "data": null
}
```

---

## Python Client Mapping

### `api_key_gen.py`

| Function     | Endpoint                    |
| ------------ | --------------------------- |
| generate_api | POST `?action=generate_api` |
| execute_ai   | POST `?action=execute_ai`   |

---

### `api_mgt.py`

| Function         | Endpoint                                      |
| ---------------- | --------------------------------------------- |
| get_all_api_keys | GET `?action=api_keys`                        |
| delete_api_key   | DELETE `?action=delete_api_key&api_key=<key>` |

---

## cURL Examples

### Generate API Key

```bash
curl -X POST "http://localhost/adet-rest-api/server/service.php?action=generate_api"
```

### Execute AI

```bash
curl -X POST "http://localhost/adet-rest-api/server/service.php?action=execute_ai" \
  -H "Content-Type: application/json" \
  -d '{"api_key":"your_key","month":5,"raw":true}'
```

### Get API Keys

```bash
curl "http://localhost/adet-rest-api/server/service.php?action=api_keys"
```

### Delete API Key

```bash
curl -X DELETE "http://localhost/adet-rest-api/server/service.php?action=delete_api_key&api_key=your_key"
```

---

## Notes

* API keys are securely generated using `random_bytes`
* Socket communication uses newline-delimited JSON for reliability
* Clean separation:

  * PHP = API layer
  * Python = AI processing layer

---

## Future Improvements

* Rate limiting per API key
* API key expiration
* Usage logging
* AI response code passthrough

---

