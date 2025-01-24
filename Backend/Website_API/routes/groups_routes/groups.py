from flask_restful import Resource
from flask import request
from services.token.token_op import check_token
from utils.errors.input.error_input_string import create_error_string
from services.db.users.db_op_user_by_id import get_user_by_user_id
from services.db.groups.db_op_groups import add_new_group

class Groups(Resource):
    def post(self):
        """
        Handles POST requests to create a new group.

        Steps:
        1. Validates the token from the `Authorization` header to ensure the user is authenticated.
        2. Parses and validates the JSON payload in the request body.
        3. Checks if the group admin (user) exists in the database using the provided `group_admin_id`.
        4. Adds the group to the database if all validations pass and group with the same administrator ID, name, and 
        description not exist.
        5. Returns a success message with the group details or an error message with the appropriate status code.

        Returns:
            dict: A JSON response with a message and group data.
            int: HTTP status code indicating the result of the operation.
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
            
            # check if user exist
            from models.user_model import User
            user: User | None = get_user_by_user_id(data.get("group_admin_id"))
            if not user:
                return {"message": f"User with user_id {data.get("group_admin_id")} does not exist."}, 404
            
            #add group to db and get this group
            group = add_new_group(data.get("group_admin_id"),  data.get("group_name"), data.get("group_description"))
            if 'message' in group:
                return group, 400
            
            return {"message": "Group created", "group": group}, 201
        except Exception as e:
            # Return a generic 500 Internal Server Error response
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
        if not data or not data.get("group_admin_id") or not data.get("group_name") or not data.get("group_description"):
            return {"message": "Invalid data. Data is required!"}, 400

        # check inputs
        fields = [
            {"input_type": "group_name", "input": data.get("group_name")},
            {"input_type": "group_description", "input": data.get("group_description")},
        ]

        return self.validate_inputs(fields)
