def get_all_users() -> list:
    """
    Retrieves all users from the database.

    Returns:
        List: A list of all users in the database, or an empty list if no users exist.
    """
    from models.user_model import User
    users = User.query.all()  # Retrieve all users from the database
    return [user.to_dict() for user in users]


def get_amount_of_users() -> int:
    """
    Retrieve the total number of users in the database.

    This function queries the 'users' table and counts the number of entries 
    (i.e., the total number of users) using SQLAlchemy's session query 
    method. It returns an integer representing the total count.

    Returns:
        int: The total number of users in the database.
    """
    from models.user_model import User, db
    return db.session.query(User).count()