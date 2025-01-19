# User Management API

## Overview
This API provides endpoints for user management, including authentication and retrieval of user data. The following routes are available:

## Routes

### 1. **GET /api/users/**
Retrieves either a list of all users or the total count of users based on the `action` query parameter.

#### Query Parameters:
- `action` (string): The action to perform. 
  - `list`: Returns a list of all users with their details.
  - `amount`: Returns the total number of users.

#### Responses:
- **200 OK**:
  - If `action=list`, returns a list of all users.
  - If `action=amount`, returns the total number of users.
- **400 Bad Request**: If `action` is missing, invalid, or contains a value other than `list` or `amount`.
- **500 Internal Server Error**: If an unexpected error occurs during processing.

---

### 2. **POST /api/users/auth/**
Handles user signup and login based on the `action` query parameter.

#### Query Parameters:
- `action` (string): The operation to perform.
  - `signup`: Registers a new user.
  - `login`: Authenticates an existing user.

#### Request Body:
- **For `signup`**:
  - `first_name` (string): The user's first name (required).
  - `last_name` (string): The user's last name (required).
  - `email` (string): The user's email address (required, unique).
  - `password` (string): The user's password (required).
- **For `login`**:
  - `email` (string): The user's email address (required).
  - `password` (string): The user's password (required).

#### Responses:
- **201 Created** (for `signup`): If successful, returns a success message with the user's email.
- **200 OK** (for `login`): If successful, returns a success message with the user's data and token.
- **400 Bad Request**: If the `action` parameter is missing or invalid. If required fields are missing or invalid.
- **401 Unauthorized**: If the email or password provided during `login` is incorrect.
- **409 Conflict**: If the email provided during `signup` already exists.
- **500 Internal Server Error**: If an unexpected error occurs.

---

### 3. **GET /api/users/<int:user_id>**
Retrieves a specific user by their unique `user_id` (requires authentication).

#### URL Parameters:
- `user_id` (integer): The unique identifier of the user to retrieve.

#### Headers:
- `Authorization`: Bearer <your_token_here>.

#### Responses:
- **200 OK**: If the user exists, returns the user data.
- **401 Unauthorized**: Token error.
- **404 Not Found**: If the user does not exist.
- **500 Internal Server Error**: If an unexpected error occurs.

---

### 4. **PATCH /api/users/<int:user_id>**
Updates a specific user's information by their `user_id` (requires token).

#### URL Parameters:
- `user_id` (integer): The unique identifier of the user to update.

#### Headers:
- `Authorization`: Bearer <your_token_here>.

#### Request Body:
- `input_type` (string): The type of information to update. It can be one of the following:
  - `first_name`: The updated first name of the user (optional).
  - `last_name`: The updated last name of the user (optional).
  - `email`: The updated email address of the user (optional).
  - `password`: The updated password of the user (optional). The password will be hashed before saving.
- `input` (string): The new value for the specified `input_type`.

#### Responses:
- **200 OK**: If the update is successful, returns the updated user data.
- **400 Bad Request**: If the request body contains invalid data or required fields are missing.
- **401 Unauthorized**: Token error.
- **404 Not Found**: If the user does not exist.
- **500 Internal Server Error**: If an unexpected error occurs.

---

## Example Requests

- **GET /api/users/?action=list**
    ```bash
    GET /api/users/?action=list
    ```

- **GET /api/users/?action=amount**
    ```bash
    GET /api/users/?action=amount
    ```

- **POST /api/users/auth/?action=signup**
    ```bash
    POST /api/users/auth/?action=signup
    Content-Type: application/json

    {
      "first_name": "John",
      "last_name": "Doe",
      "email": "johndoe@example.com",
      "password": "password123"
    }
    ```

- **POST /api/users/auth/?action=login**
    ```bash
    POST /api/users/auth/?action=login
    Content-Type: application/json

    {
      "email": "johndoe@example.com",
      "password": "password123"
    }
    ```

- **GET /api/users/<int:user_id>**
    ```bash
    GET /api/users/1
    Authorization: Bearer <your_token_here>
    ```

- **PATCH /api/users/<int:user_id>**
    ```bash
    PATCH /api/users/1
    Authorization: Bearer <your_token_here>
    Content-Type: application/json

    {
      "input_type": "first_name",
      "input": "John"
    }
    ```

    ```bash
    PATCH /api/users/1
    Authorization: Bearer <your_token_here>
    Content-Type: application/json

    {
      "input_type": "last_name",
      "input": "Doe"
    }
    ```

    ```bash
    PATCH /api/users/1
    Authorization: Bearer <your_token_here>
    Content-Type: application/json

    {
      "input_type": "email",
      "input": "john.doe@updated.com"
    }
    ```

    ```bash
    PATCH /api/users/1
    Authorization: Bearer <your_token_here>
    Content-Type: application/json

    {
      "input_type": "password",
      "input": "newPassword123"
    }
    ```



