from flask_restful import Resource
from flask import request
from services.token.token_op import check_token
from utils.errors.input.error_input_string import create_error_string
from services.db.customers.db_op_customer_by_id import get_customer_by_customer_id, change_customer_by_customer_id, delete_customer_by_customer_id
from utils.converters.convert_str_to_date import convert_str_to_date


class CustomerById(Resource):
    def get(self, customer_id: int):
        """
        Handles a GET request to retrieve customer information based on the provided customer_id.

        Workflow:
        1. Validates the authorization token in the request header.
        2. Attempts to fetch the customer details using the provided customer_id.
        3. Returns appropriate responses based on success, failure, or errors.

        Parameters:
            customer_id (int): The unique identifier of the group to retrieve.

        Returns:
            tuple: A JSON response (dict) and an HTTP status code (int).
        """
        try:
            #check token
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check
            
            #get customer from db
            from models.customer_model import Customer
            customer: Customer | None = get_customer_by_customer_id(customer_id)
            if not customer:
                return {"error": "customer not found for the given customer_id."}, 404
            
            # Return the response with the group
            return {"message": "The customer", "customer": customer.to_dict_with_age()}, 200
        except Exception as e:
            # Return a generic 500 Internal Server Error response
            print(e)
            return {"message": "An unexpected error occurred. Please try again later."}, 500
        
    
    def patch(self, customer_id: int):
        """
        Handles PATCH requests to update a customers's information.

        This method performs the following tasks:
        1. Validates the authorization token provided in the request headers.
        2. Parses the incoming JSON data from the request body.
        3. Validates the required fields.
        4. Attempts to update the customer by calling `change_customer_by_customer_id`.
        5. Returns an appropriate response based on the result of the update process.

        Steps:
        - If the token is invalid or missing, returns an error response.
        - If the input data is invalid (missing required fields), returns a `400 Bad Request` error with a detailed message.
        - If the customer is found and updated successfully, returns a `200 OK` response with the updated customer.
        - If the customer doesn't exist or an error occurs during the update process, returns an error message with the corresponding HTTP status code.

        Args:
            customer_id (int): The ID of the customer to be updated.

        Returns:
            dict: A response dictionary containing a message and, if successful, the updated customer data.
            tuple: A tuple containing an error message and an HTTP status code if an error occurs (e.g., `400` for bad request, `404` for customer not found).
        """
        try:
            #check token
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check
            
            # Parse JSON data from the body
            data = request.get_json()

            #check data
            inputs_error = self.handle_data(data)
            if inputs_error:
                return {"message": inputs_error}, 400
            
            #check if not exist get in else change in db and move foward
            data["birthday"] = None if data["birthday"] is None else convert_str_to_date(data["birthday"])
            customer = change_customer_by_customer_id(customer_id, data['first_name'], data['last_name'], data['email'], data['country'], data['city'], data['birthday'])
            if isinstance(customer, tuple) and "message" in customer[0]:
                return customer
            
            # Return the response with the updated customer
            return {"message": "The updated customer", "customer": customer}, 200
        except Exception as e:
            # Return a generic 500 Internal Server Error response
            print(e)
            return {"message": "An unexpected error occurred. Please try again later."}, 500
    

    def delete(self, customer_id: int):
        """
        Handles the HTTP DELETE request to delete a customer by its `customer_id`.

        This function performs the following steps:
        1. Checks the authorization token in the request header.
        2. If the token is invalid or not provided, an error response is returned.
        3. Calls the `delete_customer_by_customer_id` function to delete the customer with the given `customer_id`.
        4. If successful, the customer is deleted and an appropriate message is returned.
        5. In case of any errors during the process, a generic error response is returned.

        Args:
            customer_id (int): The ID of the customer to be deleted.

        Returns:
            dict: A response dictionary with a success message or an error message.
        """
        try:
            # Step 1: Check token for authorization
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check
            
            # Step 2: Call the delete function to remove the customer from the database
            return delete_customer_by_customer_id(customer_id)
        except Exception as e:
            # Step 3: Handle any exceptions by logging and returning a generic error response
            print(e)
            return {"message": "An unexpected error occurred. Please try again later."}, 500
        
    

    def validate_inputs(self, fields):
        """
        Validates the group input fields by calling a utility function.

        Args:
            fields (list): A list of dictionaries containing input fields to validate.

        Returns:
            str | None: An error message string if validation fails, otherwise None.
        """
        return create_error_string(fields)
    

    def handle_data(self, data):
        """
        Validates and processes the request payload.

        Steps:
        1. Ensures all required fields (`group_admin_id`, `group_name`, and `group_description`) are present.
        2. Uses `validate_inputs` to check the validity of specific fields.

        Args:
            data (dict): The JSON payload from the request.

        Returns:
            str | None: An error message string if validation fails, otherwise None.
        """
        # validate data
        if not data:
            return {"message": "Invalid data. Data is required!"}, 400

        # check inputs
        fields = [
            {"input_type": "first_name", "input": data.get("first_name")},
            {"input_type": "last_name", "input": data.get("last_name")},
            {"input_type": "email", "input": data.get("email")},
            {"input_type": "country", "input": data.get("country")},
            {"input_type": "city", "input": data.get("city")},
            {"input_type": "birthday", "input": data.get("birthday")}
        ]

        return self.validate_inputs(fields)