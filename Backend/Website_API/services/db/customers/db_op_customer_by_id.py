def get_customer_by_customer_id(customer_id: int):
    """
    Retrieves a customer from the database by its customer_id.

    Args:
        customer_id (int): The ID of the customer to be retrieved.

    Returns:
        Customer | None: The group object if found, otherwise None.
    """
    from models.customer_model import Customer
    customer = Customer.query.get(customer_id)
    return customer


def change_customer_by_customer_id(customer_id: int, first_name: str, last_name: str, email: str, country: str = None, city: str = None, birthday: str = None):
    """
    Updates the details of a customer identified by their customer_id.

    Parameters:
        customer_id (int): The unique identifier of the customer to update.
        first_name (str): The new first name of the customer.
        last_name (str): The new last name of the customer.
        email (str): The new email of the customer.
        country (str, optional): The new country of the customer.
        city (str, optional): The new city of the customer.
        birthday (str, optional): The new birthday of the customer in YYYY-MM-DD format.

    Returns:
        dict: A dictionary representation of the updated customer if successful.
        tuple: An error message and HTTP status code (404) if the customer is not found.
    """
    
    from models.customer_model import Customer, db
    # Step 1: Query the customer from the database by customer_id
    customer = Customer.query.filter_by(customer_id=customer_id).first()
    
    # Step 2: Check if the customer exists
    if not customer:
        return {"message": "Customer not found for the given customer_id."}, 404

    # Step 3: Check if another customer with the same email and group_id exists
    existing_customer = Customer.query.filter_by(email=email, group_id=customer.group_id).first()
    if existing_customer and existing_customer.customer_id != customer_id:
        return {"message": "A customer with this email and group ID already exists."}, 400

    # Step 4: Update the customer's details
    customer.first_name = first_name
    customer.last_name = last_name
    customer.email = email
    customer.country = country
    customer.city = city

    # Step 5: Commit the changes to the database
    db.session.commit()
    return customer.to_dict()


def delete_customer_by_customer_id(customer_id: int):
    """
    Deletes a customer from the database by their `customer_id`.

    This function performs the following tasks:
    1. Queries the `Customer` table in the database for a customer with the provided `customer_id`.
    2. If the customer exists, it deletes the customer from the database.
    3. Commits the transaction to apply the deletion.
    4. Returns a success message if the deletion is successful.
    5. If the customer does not exist, returns an error message.

    Args:
        customer_id (int): The ID of the customer to be deleted.

    Returns:
        dict: A response dictionary with a success message if the deletion is successful.
        tuple: A tuple containing an error message and an HTTP status code if the customer is not found.
    """
    from models.customer_model import Customer, db
    
    # Step 1: Query the customer from the database by customer_id
    customer = Customer.query.filter_by(customer_id=customer_id).first()

    # Step 2: Check if the customer exists
    if not customer:
        return {"message": "Customer not found for the given customer_id."}, 404

    # Step 3: Delete the customer from the database
    db.session.delete(customer)

    # Step 4: Commit the transaction to apply the deletion
    db.session.commit()

    # Step 5: Return a success message
    return {"message": "Customer successfully deleted."}, 200
