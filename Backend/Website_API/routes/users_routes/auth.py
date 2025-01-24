from flask_restful import Resource
from flask import request
from utils.errors.input.error_input_string import create_error_string
from services.db.users.db_op_auth import get_user_by_email, add_new_user
from bcrypt import hashpw, gensalt, checkpw
from services.token.token_op import get_new_token

class Auth(Resource):
    def post(self):
        """
        Handles user signup and login functionality based on the 'action' query parameter.
        
        The 'action' query parameter determines the operation:
        - 'signup': Registers a new user with the provided details in the request body.
        - 'login': Authenticates an existing user with the provided credentials.

        Request Body:
            - For 'signup':
                - first_name (str): The first name of the user (required).
                - last_name (str): The last name of the user (required).
                - email (str): The user's email address (required, must be unique).
                - password (str): The user's plain-text password (required).
            - For 'login':
                - email (str): The user's email address (required).
                - password (str): The user's plain-text password (required).

        Query Parameters:
            - action (str): Specifies the operation ('signup' or 'login').

        Returns:
            - 201 Created:
                - If 'signup' is successful, returns a success message with the user's email.
            - 200 OK:
                - If 'login' is successful, returns a success message with the user's data.
            - 400 Bad Request:
                - If the 'action' query parameter is missing or invalid.
                - If required input fields are missing or invalid.
            - 401 Unauthorized:
                - If the email or password provided during 'login' is incorrect.
            - 409 Conflict:
                - If the email provided during 'signup' already exists in the system.
            - 500 Internal Server Error:
                - If an unexpected error occurs during processing.

        Side Effects:
            - Adds a new user to the database (if 'signup' is successful).
            - Validates user credentials against stored data (if 'login' is attempted).

        Exceptions:
            - Handles all unexpected exceptions gracefully and returns a generic error message.
        """
        
        try:
            # Retrieve and validate the 'action' query parameter
            action = request.args.get("action")
            if not action:
                return {"message": "Missing 'action' query parameter."}, 400

            # Parse JSON data from the body
            data = request.get_json()

            # Handle the appropriate action
            if action == "signup":
                return self.handle_signup(data)
            elif action == "login":
                return self.handle_login(data)
            else:
                return {"message": "Invalid action. Use 'signup' or 'login'."}, 400

        except Exception as e:
            # Return a generic 500 Internal Server Error response
            print(e)
            return {"message": "An unexpected error occurred. Please try again later."}, 500


    def validate_inputs(self, fields):
        """Helper method to validate user inputs."""
        return create_error_string(fields)


    def handle_signup(self, data):
        """Handle user signup logic."""
        # validate data
        if not data or not data.get("first_name") or not data.get("last_name") or not data.get("email") or not data.get("password"):
            return {"message": "Invalid data. Data is required!"}, 400

        # check inputs
        fields = [
            {"input_type": "first_name", "input": data.get("first_name")},
            {"input_type": "last_name", "input": data.get("last_name")},
            {"input_type": "email", "input": data.get("email")},
            {"input_type": "password", "input": data.get("password")}
        ]
        inputs_error = self.validate_inputs(fields)
        if inputs_error:
            return {"message": inputs_error}, 400
        
        # check if user alredy exist
        if get_user_by_email(data["email"]):
            return {"message": "A user with that email already exists. Please try another email."}, 409
        
        # Hash the password
        hashed_password = hashpw(data["password"].encode('utf-8'), gensalt()).decode('utf-8')

        # adding new user to DB
        add_new_user(data["first_name"], data["last_name"], data["email"], hashed_password) 
       
        return {"message": "User signed up", "user": {"email": data["email"]}}, 201


    def handle_login(self, data):
        """Handle user login logic."""
        # validate data
        if not data or not data.get("email") or not data.get("password"):
            return {"message": "Invalid data. Data is required!"}, 400

        # check inputs
        fields = [
            {"input_type": "email", "input": data.get("email")},
            {"input_type": "password", "input": data.get("password")}
        ]
        inputs_error = self.validate_inputs(fields)
        if inputs_error:
            return {"message": inputs_error}, 400

        # check if user alredy exist
        from models.user_model import User
        user: User | None = get_user_by_email(data["email"])
        if not user:
            return {"message": "User not found. Please check your credentials."}, 401
        
        # check if wrong password
        if not checkpw(data["password"].encode('utf-8'), user.password.encode('utf-8')):
            return {"message": "Invalid credentials. Please check your password and try again."}, 401
        
        # get new token for 3 hours
        token = get_new_token(user.email, user.user_id)

        return {"message": "User logged in", "user": user.to_dict(), "token": token}, 200
