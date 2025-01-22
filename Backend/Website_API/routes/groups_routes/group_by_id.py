from flask_restful import Resource
from flask import request
from services.db.groups.db_op_group_by_id import get_group_by_group_id, change_group_by_group_id
from services.token.token_op import check_token
from utils.errors.input.error_input_string import create_error_string

class GroupById(Resource):
    def get(self, group_id: int):
        """
        Handles a GET request to retrieve group information based on the provided group_id.

        Workflow:
        1. Validates the authorization token in the request header.
        2. Attempts to fetch the group details using the provided group_id.
        3. Returns appropriate responses based on success, failure, or errors.

        Parameters:
            group_id (int): The unique identifier of the group to retrieve.

        Returns:
            tuple: A JSON response (dict) and an HTTP status code (int).
        """
        try:
            #check token
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check
            
            #get group from db
            group = get_group_by_group_id(group_id)
            if not group:
                return {"error": "Group not found for the given group_id."}, 404
            
            # Return the response with the group
            return {"message": "The group", "group": group}, 200
        except Exception as e:
            # Return a generic 500 Internal Server Error response
            print(e)
            return {"message": "An unexpected error occurred. Please try again later."}, 500
        
    
    def patch(self, group_id: int):
        """
        Handles PATCH requests to update a group's information.

        This method performs the following tasks:
        1. Validates the authorization token provided in the request headers.
        2. Parses the incoming JSON data from the request body.
        3. Validates the required fields (`group_name` and `group_description`).
        4. Attempts to update the group by calling `change_group_by_group_id`.
        5. Returns an appropriate response based on the result of the update process.

        Steps:
        - If the token is invalid or missing, returns an error response.
        - If the input data is invalid (missing required fields), returns a `400 Bad Request` error with a detailed message.
        - If the group is found and updated successfully, returns a `200 OK` response with the updated group.
        - If the group doesn't exist or an error occurs during the update process, returns an error message with the corresponding HTTP status code.

        Args:
            group_id (int): The ID of the group to be updated.

        Returns:
            dict: A response dictionary containing a message and, if successful, the updated group data.
            tuple: A tuple containing an error message and an HTTP status code if an error occurs (e.g., `400` for bad request, `404` for group not found).
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
            group = change_group_by_group_id(group_id, data.get("group_name"), data.get("group_description"))
            if isinstance(group, tuple) and "error" in group[0]:
                return group
            
            # Return the response with the updated group
            return {"message": "The updated group", "group": group}, 200
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
        1. Ensures all required fields (`group_name`, and `group_description`) are present.
        2. Uses `validate_inputs` to check the validity of specific fields.

        Args:
            data (dict): The JSON payload from the request.

        Returns:
            str | None: An error message string if validation fails, otherwise None.
        """
        # validate data
        if not data or not data.get("group_name") or not data.get("group_description"):
            return {"message": "Invalid data. Data is required!"}, 400

        # check inputs
        fields = [
            {"input_type": "group_name", "input": data.get("group_name")},
            {"input_type": "group_description", "input": data.get("group_description")},
        ]

        return self.validate_inputs(fields)