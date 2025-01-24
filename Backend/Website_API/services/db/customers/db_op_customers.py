def add_new_customer(data: dict):
    """"
    Adds a new customer to the database if no existing customer with the same email and group_id is found.

    This function accepts a dictionary containing customer details and creates a new
    customer record in the database using the provided information, but only if a customer
    with the same email and group_id does not already exist. It commits the changes to persist the 
    new customer if no conflict is found.

    Args:
        data (dict): A dictionary containing the following keys:
            - 'group_id' (int): The ID of the group the customer belongs to.
            - 'first_name' (str): The customer's first name.
            - 'last_name' (str): The customer's last name.
            - 'email' (str): The customer's email address.
            - 'country' (str, optional): The customer's country of residence. Default is None.
            - 'city' (str, optional): The customer's city of residence. Default is None.
            - 'birthday' (str, optional): The customer's birthday in the format 'YYYY-MM-DD'. Default is None.

    Returns:
         dict: A dictionary representation of the newly added customer or an error message if the customer already exists.
    """
    from models.customer_model import Customer, db
    
    # Check if a customer with the same email and group_id already exists
    existing_customer = Customer.query.filter_by(
        email=data['email'], group_id=data['group_id']
    ).first()

    if existing_customer:
        # Return an error message or handle as needed
        return {'message': 'Customer with the same email and group_id already exists.'}
    
    new_customer = Customer(
        group_id=data['group_id'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        country = data.get('country', None),
        city=data.get('city', None),
        birthday=data.get('birthday', None)
    )
    db.session.add(new_customer)
    db.session.commit()
    return new_customer.to_dict()


def add_new_customers(customers_list: list, group_id: int) -> dict:
    """
    Adds a list of new customers to the database for the given group_id.

    This function accepts a list of customer dictionaries and adds each customer
    to the database if no existing customer with the same email and group_id is found.
    It returns a dict with list, including added customers and any errors encountered.

    Args:
        customers_list (list): A list of dictionaries, each containing customer details:
            - 'first_name' (str): The customer's first name.
            - 'last_name' (str): The customer's last name.
            - 'email' (str): The customer's email address.
            - 'country' (str, optional): The customer's country of residence.
            - 'city' (str, optional): The customer's city of residence.
            - 'birthday' (str, optional): The customer's birthday in the format 'YYYY-MM-DD'.
        group_id (int): The ID of the group to which the customers belong.

    Returns:
        dict: A dict with list inside, each one representing the result for a customer. or error dict 
    """
    from models.customer_model import Customer, db

    results = []

    for customer_data in customers_list:
        # Check if a customer with the same email and group_id already exists
        existing_customer = Customer.query.filter_by(
            email=customer_data['email'], group_id=group_id
        ).first()

        if existing_customer:
            return {'message': f'Customer with email {customer_data['email']} already exists in the group.'}

        # Create and add the new customer
        new_customer = Customer(
            group_id=group_id,
            first_name=customer_data['first_name'],
            last_name=customer_data['last_name'],
            email=customer_data['email'],
            country=customer_data.get('country', None),
            city=customer_data.get('city', None),
            birthday=customer_data.get('birthday', None)
        )
        db.session.add(new_customer)

        # Append success result to results
        results.append(new_customer.to_dict())

    # Commit all changes at once
    db.session.commit()
    return {"customers": results}