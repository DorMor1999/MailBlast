def get_user_by_user_id(user_id: int):
    """
    Retrieves a user from the database by their user_id address.

    Args:
        user_id (int): The user_id of the user to be retrieved.

    Returns:
        User | None: The user object if found, otherwise None.
    """
    from models.user_model import User
    return User.query.get(user_id)


def change_user_col(user_id: int, new_input: str, input_type: str):
    """
    Changes a specific column for a user in the database.

    Args:
        user_id (int): The ID of the user whose data is to be updated.
        new_input (str): The new value to be assigned to the column.
        input_type (str): The name of the column to be updated.

    Returns:
        User | None: The updated user object if successful, otherwise None.
    """
    from models.user_model import User, db
    
    user = User.query.get(user_id)
    if user and hasattr(user, input_type):
        setattr(user, input_type, new_input)
        db.session.commit()
        return user
    return None

def delete_user_by_user_id(user_id: int):
    """
    This function deletes a user from the database by their user_id.
    It checks if the user exists and then deletes them, committing the changes to the database.
    If the user is not found, it returns a 404 error message.
    """
    from models.user_model import User, db
    # Find the user by user_id
    user_to_delete = User.query.get(user_id)

    if user_to_delete:
        # Delete the user
        db.session.delete(user_to_delete)
        db.session.commit()
        return {"message": "User successfully deleted"}, 200
    else:
        return {"message": "User not found"}, 404