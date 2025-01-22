from flask_restful import Resource
from flask import request
from services.db.groups.db_op_group_by_id import get_group_by_group_id
from services.token.token_op import check_token

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