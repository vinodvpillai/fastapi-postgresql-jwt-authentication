# FastAPI Authentication Service

## Overview

This is a microservice for user authentication built with FastAPI. It supports various endpoints for user registration, login, updating user details, and more. The service uses JWT for authentication and follows a modular design for better maintainability.

## Features

- User Registration
- User Login
- User Profile Update
- Token-based Authentication
- Middleware for Logging and CORS
- Token Blacklisting for Logout

## Project Structure

```
.
├── app
│   ├── __init__.py
│   ├── controller
│   │   ├── __init__.py
│   │   ├── auth_controller.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── middleware.py
│   │   ├── token_blacklist.py
│   ├── dto
│   │   ├── __init__.py
│   │   ├── auth_dto.py
│   ├── model
│   │   ├── __init__.py
│   │   ├── user.py
│   ├── repository
│   │   ├── __init__.py
│   │   ├── user_repository.py
│   ├── service
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   ├── main.py
├── run.py
├── .env
├── requirements.txt
└── README.md
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

### Setup

1. **Clone the repository:**
    ```sh
    git clone <repository_url>
    cd fastapi-authentication-service
    ```

2. **Create a virtual environment:**
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the environment variables:**
    Create a `.env` file in the project root and add the following variables:
    ```env
    DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
    SECRET_KEY=your_secret_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

5. **Run database migrations:**
    ```sh
    alembic upgrade head
    ```

## Running the Application

### Development Mode

To run the application in development mode with automatic reloading:

```sh
uvicorn app.main:app --reload
```

### Debugging with VS Code

Ensure you have the following in your `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload",
                "--host",
                "0.0.0.0",
                "--port",
                "8000"
            ],
            "envFile": "${workspaceFolder}/.env",
            "console": "integratedTerminal"
        }
    ]
}
```

## Endpoints

### /auth/register
**Method:** `POST`

**Description:** Registers a new user.

**Request Body:**
```json
{
    "username": "string",
    "email": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

### /auth/login
**Method:** `POST`

**Description:** Logs in a user and returns an access token.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

### /auth/logout
**Method:** `POST`

**Description:** Logs out a user by blacklisting the token.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
    "msg": "Successfully logged out"
}
```

### /auth/update
**Method:** `PUT`

**Description:** Updates user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
    "description": "string"
}
```

**Response:**
```json
{
    "access_token": "string",
    "token_type": "bearer"
}
```

### /auth/disable/{user_id}
**Method:** `POST`

**Description:** Disables a user account.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
    "msg": "User disabled successfully"
}
```

## Middleware

### CORS

The application includes CORS middleware to allow cross-origin requests.

### Logging

Custom middleware is included to log each request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

