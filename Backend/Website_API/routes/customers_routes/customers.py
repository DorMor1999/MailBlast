from flask_restful import Resource
from flask import request
from services.token.token_op import check_token
from utils.errors.input.error_input_string import create_error_string
from services.db.groups.db_op_group_by_id import get_group_by_group_id
from services.db.customers.db_op_customers import add_new_customer, add_new_customers

class Customers(Resource):
    def post(self):
        """
        Handles HTTP POST requests to create customers.

        This method serves as the entry point for customer creation. It determines whether to process
        a single customer or a list of customers based on the `size` query parameter. The method validates
        the input data, checks the provided token, and delegates the processing to `handle_one` or `handle_list`
        methods.

        Query Parameters:
            size (str): Indicates the size of the request. Accepted values are:
                        - 'one': For creating a single customer.
                        - 'list': For creating multiple customers.

        Request Headers:
            Authorization (str): A token required for authentication and authorization.

        Request Body:
            For size='one': A dictionary containing a single customer's details:
                            - 'first_name' (str): The customer's first name.
                            - 'last_name' (str): The customer's last name.
                            - 'email' (str): The customer's email address.
                            - 'group_id' (int): The ID of the group the customer belongs to.
            For size='list': A dictionary with a `customers` key, containing a list of dictionaries
                            for multiple customers. Each customer dictionary should include:
                            - 'first_name' (str): The customer's first name.
                            - 'last_name' (str): The customer's last name.
                            - 'email' (str): The customer's email address.
                            - 'group_id' (int): The ID of the group the customer belongs to.

        Returns:
            dict: A response dictionary containing a success message and customer details,
                or an error message if validation or creation fails.
            int: The HTTP status code corresponding to the response.

        Raises:
            Exception: Catches and logs unexpected errors, returning a generic 500 error response.
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
        """
        Handles the creation of multiple customers.

        This method processes a list of customer data, validates it, and adds the customers to the database.
        It ensures that the input data is valid, the customers belong to the same group, and that there are
        no duplicate email addresses. If all checks pass, it adds the customers to the database.

        Args:
            data (dict): A dictionary containing a `customers` key, which is a list of customer dictionaries.
                        Each customer dictionary should include:
                        - 'first_name' (str): The customer's first name.
                        - 'last_name' (str): The customer's last name.
                        - 'email' (str): The customer's email address.
                        - 'group_id' (int): The ID of the group the customer belongs to.

        Returns:
            dict: A response dictionary containing a success message and the list of created customers,
                or an error message if validation or creation fails.
            int: The HTTP status code corresponding to the response.
        """
        #check for errors
        error = self.check_data_list_customers(data)
        if error:
            return error
        
        #adding customers to DB 
        customers = add_new_customers(data['customers'], data['customers'][0]["group_id"])
        if 'message' in customers.keys():
            return customers, 400
        
        return {"message": "All customers created", "customers": customers['customers']}, 201
        

            
    def check_data_list_customers(self, data):
        #check data
        if not data or not data['customers']:
            return {"message": "Invalid data. Data is required!"}, 400
        
        #check customers amount
        if len(data['customers']) < 2:
            return {"message": "At least two customers please!"}, 400

        #check every customer
        emails = []
        the_group_id = data['customers'][0]["group_id"]
        for customer in data['customers']:
            if customer['email'] in emails:
                return {"message": "In this list you have two customers with the same email."}, 400
            emails.append(customer['email'])
            inputs_error = self.handle_data(customer)
            #check fist_name, last_name, email
            if inputs_error:
                return {"message": inputs_error}, 400
            #check group_id
            if not customer["group_id"] or type(customer["group_id"]) is not int or the_group_id != customer["group_id"]:
                return {"message": "All customers need to be with the same group_id."}, 400
            group = get_group_by_group_id(customer["group_id"])
            if not group:
                return {"message": "Group with that id dosn't found."}, 404


    def handle_one(self, data):
        """
        Handles the creation of a single customer.

        This method processes a single customer's data, validates it, and adds the customer to the database.
        It ensures that the input data is valid, the group exists, and that no existing customer in the same group
        has the same email address. If all checks pass, it adds the customer to the database.

        Args:
            data (dict): A dictionary containing the customer's details:
                        - 'first_name' (str): The customer's first name.
                        - 'last_name' (str): The customer's last name.
                        - 'email' (str): The customer's email address.
                        - 'group_id' (int): The ID of the group the customer belongs to.

        Returns:
            dict: A response dictionary containing a success message and the created customer's details,
                or an error message if validation or creation fails.
            int: The HTTP status code corresponding to the response.
        """
        #check data
        inputs_error = self.handle_data(data)
        if inputs_error:
            return {"message": inputs_error}, 400
        
        #check group_id
        if not data.get("group_id") or type(data.get("group_id")) is not int:
            return {"message": "Group id is reqired."}, 400
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
        if not data:
            return {"message": "Invalid data. Data is required!"}, 400

        # check inputs
        fields = [
            {"input_type": "first_name", "input": data.get("first_name")},
            {"input_type": "last_name", "input": data.get("last_name")},
            {"input_type": "email", "input": data.get("email")}
        ]

        return self.validate_inputs(fields)
    

