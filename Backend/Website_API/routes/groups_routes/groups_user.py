from flask_restful import Resource
from flask import request
from services.db.users.db_op_user_by_id import get_user_by_user_id
from services.token.token_op import check_token
from services.db.groups.db_op_groups_user import get_groups_of_user_by_user_id_sorted

class GroupsUser(Resource):
    def get(self, user_id: int):
        """
        Handles GET requests to retrieve groups of a user by their user ID.

        Args:
            user_id (int): The ID of the user whose groups are to be retrieved.

        Query Parameters:
            sort (str): The field by which the groups should be sorted. 
                        Allowed values: 'group_name', 'group_description', 'created_at'.
            order (str): The sorting order of the results. 
                        Allowed values: 'high_to_low', 'low_to_high'.

        Returns:
            dict: A JSON response with a message and a list of groups or an error message.
            HTTP Status Code:
                - 200: Successfully retrieved and sorted the groups.
                - 400: Invalid 'sort' or 'order' parameter provided.
                - 404: The user with the given user_id does not exist.
                - 500: An unexpected error occurred during the request.
        """
        try:
            #check token
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check
            
            # Retrieve 'sort' and 'order' from the query parameters
            sort = request.args.get("sort")
            order = request.args.get("order")
            
            #check Query Parameters
            error_query_parameters = self.check_query_parameters(sort, order)
            if error_query_parameters:
                return error_query_parameters
            
            # check if user exist
            from models.user_model import User
            user: User | None = get_user_by_user_id(user_id)
            if not user:
                return {"message": f"User with user_id {user_id} does not exist."}, 404
            
            #get groups from db
            groups = get_groups_of_user_by_user_id_sorted(user_id, sort, order)
            
            # Return the response with the list of groups
            return {"message": "All the groups of the user", "groups": groups}, 200
        except Exception as e:
            # Return a generic 500 Internal Server Error response
            print(e)
            return {"message": "An unexpected error occurred. Please try again later."}, 500
        
    def check_query_parameters(self, sort: str, order: str):
        """
        Validates the query parameters 'sort' and 'order' to ensure they are allowed values.

        Args:
            sort (str): The field by which the groups should be sorted. 
                        Allowed values: 'group_name', 'group_description', 'created_at'.
            order (str): The sorting order of the results.
                        Allowed values: 'high_to_low', 'low_to_high'.

        Returns:
            tuple: A dictionary containing the error message and the HTTP status code (400) if validation fails.
                Returns None if both 'sort' and 'order' are valid.

        Behavior:
            - If 'sort' is invalid, returns a message specifying valid options and HTTP status code 400.
            - If 'order' is invalid, returns a message specifying valid options and HTTP status code 400.
            - If both parameters are valid, the function returns None.
        """
        # Validate 'sort'
        if sort not in ["group_name", "group_description", "created_at"]:
            return {"message": "Invalid sort. Use 'group_name', 'group_description', or 'created_at'."}, 400
        
        # Validate 'order'
        if order not in ["high_to_low", "low_to_high"]:
            return {"message": "Invalid order. Use 'high_to_low' or 'low_to_high'."}, 400
