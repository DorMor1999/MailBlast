from flask_restful import Resource
from flask import request
from services.token.token_op import check_token
from utils.errors.input.error_input_string import create_error_string
from services.db.groups.db_op_group_by_id import get_group_by_group_id
from services.db.customers.db_op_customers import add_new_customer

class Customers(Resource):
    def post(self):
        """
        
        """
        try:
            #check token
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check
            
            # Retrieve 'size' from the query parameters
            size = request.args.get("size")

            # Parse JSON data from the body
            data = request.get_json()

            if size == 'list':
                return self.handle_list(data)
            elif size == 'one':
                return self.handle_one(data)
            else:
                return {"message": "Invalid size. Use 'one', or 'list'."}, 400
        except Exception as e:
            # Return a generic 500 Internal Server Error response
            print(e)
            return {"message": "An unexpected error occurred. Please try again later."}, 500
        
    
    def handle_list(self, data):
        pass

    def handle_one(self, data):
        #check data
        inputs_error = self.handle_data(data)
        if inputs_error:
            return {"message": inputs_error}, 400
        
        #check group_id
        group = get_group_by_group_id(data.get("group_id"))
        if not group:
            return {"message": "Group with that id dosn't found."}, 404  
        
        #adding customer to DB
        customer = add_new_customer(data)
        if 'message' in customer.keys():
            return customer, 400

        return {"message": "Customer created", "customer": customer}, 201
  

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
        if not data or not data.get("group_id") or not data.get("first_name") or not data.get("last_name") or not data.get("email"):
            return {"message": "Invalid data. Data is required!"}, 400

        # check inputs
        fields = [
            {"input_type": "first_name", "input": data.get("first_name")},
            {"input_type": "last_name", "input": data.get("last_name")},
            {"input_type": "email", "input": data.get("email")}
        ]

        return self.validate_inputs(fields)
