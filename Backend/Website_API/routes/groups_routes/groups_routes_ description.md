# Groups API Documentation

## Overview
This API allows users to manage groups within a system. It provides endpoints to:

- Retrieve groups associated with a user.
- Create new groups.
- Retrieve, update, or delete individual groups.

All interactions are secured through token-based authentication, and the API supports a variety of query parameters to filter and sort the data.

## Authentication
Each request to the API must include an `Authorization` header with a valid token.

Example:
```bash
Authorization: Bearer <your_token>
```

## Endpoints

### 1. Get Groups by User ID
`GET /api/groups/user/<user_id>/`

Retrieves all the groups associated with a specific user by their user ID.

#### Query Parameters:
- `sort`: The field by which the groups should be sorted. Allowed values: 'group_name', 'group_description', 'created_at'.
- `order`: The sorting order of the results. Allowed values: 'high_to_low', 'low_to_high'.

#### Responses:
- `200`: Successfully retrieved and sorted the groups.
- `400`: Invalid 'sort' or 'order' parameter.
- `404`: User does not exist.
- `500`: Unexpected error.

### 2. Create a New Group
`POST /api/groups/`

Creates a new group with specified details.

#### Request Body:
- `group_name`: The name of the group.
- `group_description`: A brief description of the group.
- `group_admin_id`: The user ID of the group admin.

#### Responses:
- `201`: Group created successfully.
- `400`: Invalid request data.
- `404`: User does not exist.
- `500`: Unexpected error.

### 3. Get Group by ID
`GET /api/groups/<group_id>/`

Retrieves information about a specific group by its ID.

#### Responses:
- `200`: Successfully retrieved the group.
- `404`: Group not found.
- `500`: Unexpected error.

### 4. Update Group by ID
`PATCH /api/groups/<group_id>/`

Updates the details of a group (e.g., name and description).

#### Request Body:
- `group_name`: The new name of the group.
- `group_description`: The new description of the group.

#### Responses:
- `200`: Group updated successfully.
- `400`: Invalid input.
- `404`: Group not found.
- `500`: Unexpected error.

### 5. Delete Group by ID
`DELETE /api/groups/<group_id>/`

Deletes a group by its ID.

#### Responses:
- `200`: Group deleted successfully.
- `404`: Group not found.
- `500`: Unexpected error.

## Error Handling
The API provides meaningful error messages for different failure cases, such as missing parameters, invalid authentication tokens, or non-existent users and groups.

Example:
```json
{
  "message": "Invalid 'sort' parameter provided."
}
```