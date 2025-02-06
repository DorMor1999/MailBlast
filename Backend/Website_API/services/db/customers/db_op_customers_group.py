def get_customers_of_group_by_group_id_sorted(group_id: int, sort: str, order: str, age: str) -> [dict]:
    """
    Retrieves customers of a specific group, sorted based on the specified field and order, 
    and optionally includes the 'age' field.

    Args:
        group_id (int): The ID of the group whose customers are to be retrieved.
        sort (str): The field by which the results should be sorted.
                    Allowed values: 'first_name', 'last_name', 'email', 'country', 'city', 'birthday'.
        order (str): The sorting order of the results.
                    Allowed values: 'high_to_low' (descending) or 'low_to_high' (ascending).
        age (str): Whether to include the 'age' field in the results.
                    Allowed values: 'include' (includes age), 'uninclude' (excludes age).

    Returns:
        list[dict]: A list of dictionaries representing the customers in the specified group,
                    sorted by the specified field and order, and optionally including the 'age' field.

    Raises:
        ValueError: If the provided sort field, order, or age option is invalid.

    Behavior:
        - If 'age' is 'include', the function includes the 'age' field in the customer dictionary.
        - If 'age' is 'uninclude', the function omits the 'age' field from the customer dictionary.
        - If 'sort' or 'order' is invalid, a ValueError is raised.
    """
    from models.customer_model import Customer, db
    from sqlalchemy import desc, asc

    # Validate sort field to prevent SQL injection
    valid_sort_fields = ["first_name", "last_name", "email", "country", "city", "birthday"]
    if sort not in valid_sort_fields:
        raise ValueError(f"Invalid sort field: '{sort}'. Must be one of {valid_sort_fields}.")
    
    # Validate order
    valid_orders = ['high_to_low', 'low_to_high']
    if order not in valid_orders:
        raise ValueError(f"Invalid order: '{order}'. Must be one of {valid_orders}.")
    
    # Validate age field
    valid_age = ["include", "uninclude"]
    if age not in valid_age:
        raise ValueError(f"Invalid age: '{age}'. Must be one of {valid_age}.")

    # Determine the sorting order
    sort_order = desc if order == 'high_to_low' else asc

    customers = (
            db.session.query(Customer)
            .filter(Customer.group_id == group_id)
            .order_by(sort_order(getattr(Customer, sort)))
            .all()
        )
   
    # Convert customers to a list of dictionaries, including or excluding age as requested
    if age == "include":
        return [customer.to_dict_with_age() for customer in customers]
    else:
        return [customer.to_dict() for customer in customers]
