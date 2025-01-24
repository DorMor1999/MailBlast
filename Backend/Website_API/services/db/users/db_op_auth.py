def get_user_by_email(email: str):
    """
    Retrieves a user from the database by their email address.

    Args:
        email (str): The email address of the user to be retrieved.

    Returns:
        User | None: The user object if found, otherwise None.
    """
    from models.user_model import User
    return User.query.filter_by(email=email).first()


def add_new_user(first_name: str, last_name: str, email: str, password: str) -> dict:
    """
    Adds a new user to the database and return a dict of him.

    Args:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        password (str): The password for the user's account.

    Returns:
        dict: dict that describe the user.
    
    Side Effects:
        - Adds a new user record to the database.
        - Commits the new user to the database session.

    Raises:
        IntegrityError: If there is a conflict, such as the email already existing in the database.
    """
    from models.user_model import User, db
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user.to_dict()
    