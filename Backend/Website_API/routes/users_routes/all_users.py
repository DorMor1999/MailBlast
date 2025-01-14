from flask_restful import Resource
from flask import request
from services.db.users.db_op_all_users import get_all_users, get_amount_of_users

class AllUsers(Resource):
    def get(self):
        """
        Retrieves either a list of all users or the total count of users based on the 'action' query parameter.

        Supported actions:
        - 'list': Returns a list of all users and their details.
        - 'amount': Returns the total number of users.

        Query Parameters:
        - action (str): Specifies the action to be performed ('list' or 'amount').

        Returns:
        - 200 OK: 
            - If 'list', returns a list of all users.
            - If 'amount', returns the total number of users.
        - 400 Bad Request: 
            - If the 'action' query parameter is missing, invalid, or contains a value other than 'list' or 'amount'.
        - 500 Internal Server Error: 
            - If an unexpected error occurs during processing.

        Side Effects:
            - Executes the appropriate action (retrieving a list of all users or counting the total number of users) based on the 'action' query parameter.

        Exceptions:
            - Catches any unexpected exceptions and returns a generic error message.
        """
        try:
            # Retrieve 'action' from the query parameters
            action = request.args.get("action")
            

            if action == "list":
                return self.handle_list()
            elif action == "amount":
                return self.handle_amount()
            else:
                # If 'action' is invalid, return an error message
                return {"message": "Invalid action. Use 'list' or 'amount'."}, 400
        except Exception as e:
            # Return a 500 Internal Server Error response
            return {"message": "An unexpected error occurred. Please try again later."}, 500
    

    def handle_list(self):
        """
        Retrieve a list of all users.
        
        This function handles the retrieval of all users and returns a JSON response 
        with a list of users.
        
        Returns:
            dict: A JSON response containing the message and the list of users.
        """
        return {"message": "Retrieve all users", "users": get_all_users()}, 200
    

    def handle_amount(self):
        """
        Retrieve the amount of users.
        
        This function handles the retrieval of the total number of users and returns a 
        JSON response with the count of users.
        
        Returns:
            dict: A JSON response containing the message and the amount of users.
        """    
        return {"message": "Retrieve amount of users", "amount": get_amount_of_users()}, 200
