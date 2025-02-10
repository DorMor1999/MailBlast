# Customers API

This API provides endpoints for managing customers and customer groups.

## Endpoints

### 1. `GET /api/customers/<int:customer_id>`
Retrieves customer information based on the provided `customer_id`.

#### Workflow:
1. Validates the authorization token in the request header.
2. Attempts to fetch the customer details using `customer_id`.
3. Returns appropriate responses based on success, failure, or errors.

#### Responses:
- `200 OK`: Returns the customer details.
- `401 Unauthorized`: If the token is invalid or missing.
- `404 Not Found`: If the customer does not exist.
- `500 Internal Server Error`: On unexpected errors.

---

### 2. `PATCH /api/customers/<int:customer_id>`
Updates a customer's information.

#### Workflow:
1. Validates the authorization token in the request headers.
2. Parses the incoming JSON data from the request body.
3. Validates required fields.
4. Attempts to update the customer.
5. Returns an appropriate response based on the result.

#### Responses:
- `200 OK`: Returns the updated customer details.
- `400 Bad Request`: If the input data is invalid.
- `404 Not Found`: If the customer does not exist.
- `500 Internal Server Error`: On unexpected errors.

---

### 3. `DELETE /api/customers/<int:customer_id>`
Deletes a customer.

#### Workflow:
1. Validates the authorization token.
2. Calls the deletion function for the given `customer_id`.
3. Returns an appropriate response.

#### Responses:
- `200 OK`: If the customer was successfully deleted.
- `401 Unauthorized`: If the token is invalid or missing.
- `404 Not Found`: If the customer does not exist.
- `500 Internal Server Error`: On unexpected errors.

---

### 4. `GET /api/customers/group/<int:group_id>/`
Retrieves customers from a specific group, sorted according to query parameters.

#### Query Parameters:
- `sort` (optional): Field to sort by.
- `order` (optional): Sorting order (`asc` or `desc`).
- `age` (optional): Whether to include the `age` field.

#### Responses:
- `200 OK`: Returns a list of customers.
- `400 Bad Request`: If query parameters are invalid.
- `404 Not Found`: If the group does not exist.
- `500 Internal Server Error`: On unexpected errors.

---

### 5. `POST /api/customers/`
Creates one or multiple customers.

#### Query Parameters:
- `size=one`: Creates a single customer.
- `size=list`: Creates multiple customers.

#### Request Body:
- For `size=one`:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "group_id": 1
  }
  ```
- For `size=list`:
  ```json
  {
    "customers": [
      {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "group_id": 1
      },
      {
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "group_id": 2
      }
    ]
  }
  ```

#### Responses:
- `201 Created`: Returns the newly created customer(s).
- `400 Bad Request`: If validation fails.
- `401 Unauthorized`: If the token is invalid or missing.
- `500 Internal Server Error`: On unexpected errors.

---

## Authentication
All endpoints require an authorization token in the request headers.

## Error Handling
The API returns standardized error responses with appropriate status codes.

## Contact
For further inquiries, contact the API support team.

