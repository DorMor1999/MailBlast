from flask_restful import Resource
from flask import request

class AllUsers(Resource):
    def get(self):
        """
        Retrieve list of all users or the amount of users based on the 'action' query parameter.
        Return 500 if an unexpected error occurs.
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
        with an empty list of users (or real data if available).
        
        Returns:
            dict: A JSON response containing the message and the list of users.
        """
        # Initialize an empty list of users for demonstration purposes
        arr = []

        # Return an empty list of users (or real data if you have any)
        return {"message": "Retrieve all users", "users": arr}, 200
    

    def handle_amount(self):
        """
        Retrieve the amount of users.
        
        This function handles the retrieval of the total number of users and returns a 
        JSON response with the count of users (or real data if available).
        
        Returns:
            dict: A JSON response containing the message and the amount of users.
        """
        # Initialize an empty list of users for demonstration purposes
        arr = []

        # Return the number of users in the list
        return {"message": "Retrieve amount of users", "amount": len(arr)}, 200
