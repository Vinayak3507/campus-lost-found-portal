# Backend Documentation (Version 0.1)

## Project Architecture

```
Client (React)
      │
      │ HTTP Request
      ▼
FastAPI Router
      │
      ▼
Service Layer
      │
      ▼
Repository Layer
      │
      ▼
MySQL Database
```

Each layer has only one responsibility.


## Folder Explanation

### `app/config`

**Purpose:** Application configuration.

**Contains:** `settings.py`

**Responsible for:**
- Reading `.env`
- Database credentials
- Secret keys
- Future JWT settings

**Example:**
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

> No business logic belongs here.

---

### `app/db`

**Purpose:** Everything related to MySQL.

**Contains:**
- `session.py`
- `base.py`

**Responsibilities:**
- Connect to MySQL
- Create database
- Create tables
- Return database connection

**Current functions:**
- `create_database()`
- `create_tables()`
- `get_connection()`
- `initialize_database()`

Every repository uses:
```python
connection = get_connection()
```
instead of creating connections itself.

---

### `app/schema`

**Purpose:** Validate incoming request data.

**Current file:** `auth_schema.py`

**Contains:** `UserRegisterRequest`

**Responsibilities — validate:**
- ✔ Student Name
- ✔ Student ID
- ✔ Email
- ✔ Password
- ✔ Confirm Password
- ✔ Branch
- ✔ Academic Session
- ✔ Phone

**Example flow:**
```
Incoming JSON
      ↓
Pydantic checks it
      ↓
If valid → Passes to Service
Else     → Returns 422 Validation Error
```

---

### `app/models`

**Purpose:** Project enums and database models.

**Currently:** `enums.py`

**Contains:** `BranchEnum`

**Later it will also contain:**
- `RoleEnum`
- `ReportType`
- `ClaimStatus`
- `Importance`
- `Visibility`
- etc.

---

### `app/repositories`

**Purpose:** Talk to MySQL.

**Current:** `auth_repository.py`

**Responsibilities:** Only SQL queries — `INSERT`, `UPDATE`, `DELETE`, `SELECT`.

**Rules:**
- Repository **never** validates data.
- Repository **never** hashes passwords.
- Repository **never** creates JWT.
- Repository only talks to the database.

**Example:**
```
Register User
      ↓
INSERT INTO users(...)
```

---

### `app/services`

**Purpose:** Business logic.

**Current:** `auth_service.py`

**Responsibilities — Registration flow:**
```
Receive validated user
      ↓
Check email exists
      ↓
Check student ID exists
      ↓
Hash password
      ↓
Generate UUID
      ↓
Call repository
      ↓
Return success
```

> No SQL here. Only business decisions.

---

### `app/api`

**Purpose:** FastAPI endpoints.

**Current:** `auth.py`

**Responsibilities:**
```
Receive HTTP request
      ↓
Call service
      ↓
Return response
```

**Example:** `POST /auth/register`

Nothing more.

---

### `main.py`

**Purpose:** Start FastAPI.

**Current responsibilities:**
- Initialize database
- Register routers
- Run server

**Startup flow:**
```
main.py
   ↓
initialize_database()
   ↓
Database Ready
   ↓
Routes Loaded
   ↓
Server Running
```

## Registration Flow

```
POST /auth/register
      ↓
FastAPI
      ↓
UserRegisterRequest
      ↓
Validation
      ↓
AuthService.register_user()
      ↓
AuthRepository.create_user()
      ↓
MySQL
      ↓
Success Response
```

## Current Database

**Tables:**
- `users`
- `reports`
- `categories`
- `claims`
- `notifications`

**Relationships:**
```
User
  ↓
Many Reports
  ↓
Many Claims
  ↓
Many Notifications
```

## What Happens During Registration

User sends:
```json
{
  "student_name": "Vinayak",
  "student_id": "220105",
  ...
}
```

```
Schema validates
      ↓
Password checked
      ↓
Email checked
      ↓
Student ID checked
      ↓
Password hashed
      ↓
UUID generated
      ↓
INSERT Query
      ↓
User saved
      ↓
Response
```

Response:
```json
{
  "message": "User registered successfully",
  "user_id": "..."
}
```

## Request Lifecycle

```
Internet
   ↓
POST Request
   ↓
FastAPI Router
   ↓
Schema
   ↓
Service
   ↓
Repository
   ↓
MySQL
   ↓
Repository
   ↓
Service
   ↓
API
   ↓
Response
```

## Why Multiple Layers?

Suppose tomorrow you replace MySQL with MongoDB.
> Only the **Repository** changes. Everything else remains the same.

Suppose tomorrow the password policy changes.
> Only the **Service** changes.

Suppose the request body changes.
> Only the **Schema** changes.

This is why production projects are modular.

## Current Project Progress

- [x] Project Structure
- [x] MySQL Connection
- [x] Database Initialization
- [x] Tables Creation
- [x] Configuration
- [x] User Registration Schema
- [x] Password Validation
- [x] Repository Layer
- [x] Service Layer
- [x] API Layer
- [x] Register Endpoint
- [x] User Registration Working