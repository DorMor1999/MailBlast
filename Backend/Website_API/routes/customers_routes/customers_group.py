from flask_restful import Resource
from flask import request
from services.token.token_op import check_token
from services.db.groups.db_op_group_by_id import get_group_by_group_id
from services.db.customers.db_op_customers_group import get_customers_of_group_by_group_id_sorted


class CustomersGroup(Resource):
    def get(self, group_id: int):
        """
        Handles the GET request to retrieve customers from a specific group, 
        sorted according to query parameters, and optionally including the age field.

        Args:
            group_id (int): The ID of the group whose customers are to be retrieved.

        Returns:
            dict: A response containing a list of customers in the specified group, 
                sorted as requested, and optionally including an 'age' field.
            HTTP Status Code:
                - 200: Success, the customers are returned.
                - 400: If the query parameters (`sort`, `order`, `age`) are invalid.
                - 404: If the specified group does not exist.
                - 500: If an unexpected error occurs.

        Raises:
            Exception: If an unexpected error occurs, a generic 500 error response is returned.

        Behavior:
            - Verifies the validity of the authorization token using `check_token`.
            - Validates the `sort`, `order`, and `age` query parameters.
            - Retrieves customers from the specified group from the database, sorted as per the query.
            - Returns a list of customers, optionally including their age.
        """
        try:
            #check token
            token_check = check_token(request.headers.get("Authorization"))
            if token_check:
                return token_check
            
            # Retrieve 'sort' and 'order' from the query parameters
            sort = request.args.get("sort")
            order = request.args.get("order")
            age = request.args.get("age")
            
            #check Query Parameters
            error_query_parameters = self.check_query_parameters(sort, order, age)
            if error_query_parameters:
                return error_query_parameters
            
            # check if group exist
            from models.group_model import Group
            group: Group | None = get_group_by_group_id(group_id)
            if not group:
                return {"message": f"Group with group_id {group_id} does not exist."}, 404
            
            #get groups from db
            customers = get_customers_of_group_by_group_id_sorted(group_id, sort, order, age)
            
            # Return the response with the list of groups
            return {"message": "All the customers of the group", "customers": customers}, 200
        except Exception as e:
            # Return a generic 500 Internal Server Error response
            print(e)
            return {"message": "An unexpected error occurred. Please try again later."}, 500
        
    
    def check_query_parameters(self, sort: str, order: str, age: str):
        """
        Validates the query parameters 'sort', 'order', and 'age' to ensure they are allowed values.

        Args:
            sort (str): The field by which the records should be sorted.
                        Allowed values: 'first_name', 'last_name', 'email', 'country', 'city', 'birthday'.
            order (str): The sorting order of the results.
                        Allowed values: 'high_to_low', 'low_to_high'.
            age (str): Specifies whether to include age in the query.
                        Allowed values: 'include', 'uninclude'.

        Returns:
            tuple: A dictionary containing the error message and HTTP status code (400) if validation fails.
                Returns None if all parameters are valid.

        Behavior:
            - If 'sort' is invalid, returns an error message specifying valid options and HTTP status code 400.
            - If 'order' is invalid, returns an error message specifying valid options and HTTP status code 400.
            - If 'age' is invalid, returns an error message specifying valid options and HTTP status code 400.
            - If all parameters are valid, returns None.
        """
        # Validate 'sort'
        if sort not in ["first_name", "last_name", "email", "country", "city", "birthday"]:
            return {"message": "Invalid sort. Use 'first_name', 'last_name', 'email', 'country', 'city', or 'birthday'."}, 400
        
        # Validate 'order'
        if order not in ["high_to_low", "low_to_high"]:
            return {"message": "Invalid order. Use 'high_to_low' or 'low_to_high'."}, 400
       
        # Validate 'age'
        if age not in ["include", "uninclude"]:
            return {"message": "Invalid age. Use 'include' or 'uninclude'."}, 400