def get_group_by_group_id(group_id: int):
    """
    Retrieves a group from the database by its group_id.

    Args:
        group_id (int): The ID of the group to be retrieved.

    Returns:
        Group | None: The group object if found, otherwise None.
    """
    from models.group_model import Group
    return Group.query.get(group_id).to_dict()


def change_group_by_group_id(group_id: int, group_name: str, group_description: str):
    """
    Updates the name and description of a group identified by its group_id.

    Parameters:
        group_id (int): The unique identifier of the group to update.
        group_name (str): The new name to assign to the group.
        group_description (str): The new description to assign to the group.

    Returns:
        dict: A dictionary representation of the updated group if successful.
        tuple: An error message and HTTP status code (404) if the group is not found.

    Raises:
        SQLAlchemyError: If there is an issue with the database operation.

    This function retrieves a group from the database by its ID, checks for its existence, 
    updates the group's name and description, commits the changes, and returns the updated group as a dictionary. 
    If the group is not found, it returns an error message and a 404 status code.
    """
    
    from models.group_model import Group, db
    # Step 1: Query the group from the database by group_id
    group = Group.query.filter_by(group_id=group_id).first()

    # Step 2: Check if the group exists
    if not group:
        return {"error": "Group not found for the given group_id."}, 404
    
    # Step 3: Update the group's name and description
    group.group_name = group_name
    group.group_description = group_description

    # Step 4: Commit the changes to the database
    db.session.commit()
    return group.to_dict()
