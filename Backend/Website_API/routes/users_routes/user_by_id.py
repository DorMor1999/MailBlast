from flask_restful import Resource
from flask import request
from services.db.users.db_op_user_by_id import get_user_by_user_id, change_user_col
from utils.errors.input.error_input_string import create_error_string
from bcrypt import hashpw, gensalt
from services.token.token_op import check_token


class UserById(Resource):
    def get(self, user_id: int):
        """
        Retrieve a specific user by their ID (requires token).

        This function simulates the retrieval of a user by their unique identifier (`user_id`).
        If the user does not exist, an appropriate error message is returned with a 404 status code.
        In case of an unexpected error during the process, a 500 status code is returned.

        Args:
            user_id (int): The unique identifier of the user to be retrieved.

        Returns:
            dict: A dictionary containing the response message and user data.
            int: HTTP status code indicating the result of the operation.
        """
        try:
            #check token
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check

            # check if user exist
            from models.user_model import User
            user: User | None = get_user_by_user_id(user_id)
            if not user:
                return {"message": f"User with user_id {user_id} does not exist."}, 404


            return {"message": f"Retrieve user.", "user": user.to_dict()}, 200

        except Exception as e:
            return {"message": "An unexpected error occurred."}, 500


    def patch(self, user_id: int):
        """
         Update a specific user's information by user ID (requires token).
        
        This method checks if the user exists in the database, validates 
        the provided data, and updates the specified fields. 
        Returns appropriate responses for success, invalid input, or errors.
        
        Args:
            user_id (int): The unique identifier of the user to update.
            
        Returns:
            dict, int: A JSON response with a message and HTTP status code.
        """
        try:
            #check token
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check

            # Import the User model and retrieve the user
            from models.user_model import User
            user: User | None = get_user_by_user_id(user_id)
            if not user:
                return {"message": f"User with user_id {user_id} does not exist."}, 404

            # Parse and validate request data
            data = request.get_json()
            check = self.check_data_patch(data)
            if check:
                return check

            # if i change password i hash her before
            if data["input_type"] == 'password':
                # Hash the password
                data["input"] = hashpw(data["input"].encode('utf-8'), gensalt()).decode('utf-8')
            
            # Update the user in the database
            change_user_col(user_id,  data["input"], data["input_type"])

            # return success
            return {"message": f"User {user_id} updated successfully", "updated_field": data["input_type"]}, 200

        except Exception as e:
            # Catch unexpected errors and return a generic error message
            return {"message": "An error occurred while updating the user.", "error": str(e)}, 500
    

    def validate_inputs(self, fields):
        """Helper method to validate user inputs."""
        return create_error_string(fields)


    def check_data_patch(self, data):
        """Helper method to check data."""
        # check data
        fields = []
        if data and data.get("input_type") == 'first_name':
            fields = [{"input_type": "first_name", "input": data.get("input")}]
        elif data and data.get("input_type") == 'last_name':
            fields = [{"input_type": "last_name", "input": data.get("input")}]
        elif data and data.get("input_type") == 'email':
            fields = [{"input_type": "email", "input": data.get("input")}]
        elif data and data.get("input_type") == 'password':
            fields = [{"input_type": "password", "input": data.get("input")}]
        else:
            #data wrong
            return {
                "message": (
                    "Invalid data. Data is required!\n"
                    "data example:\n"
                    "{'input_type': 'first_name', 'input': 'valid first name'}\n"
                    "{'input_type': 'last_name', 'input': 'valid last name'}\n"
                    "{'input_type': 'eamil', 'input': 'valid eamil adress'}\n"
                    "{'input_type': 'password', 'input': 'valid password'}"
                )
            }, 400
       
        #validate inputs problem here
        inputs_error = self.validate_inputs(fields)
        if inputs_error:
            return {"message": inputs_error}, 400
