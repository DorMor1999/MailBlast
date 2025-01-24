from datetime import date, datetime

def add_new_group(group_admin_id: int, group_name: str, group_description: str) -> dict:
    """
    Adds a new group to the database and returns its details as a dictionary.

    This function checks if a group with the same administrator ID, name, and 
    description already exists in the database. If such a group exists, it 
    does not create a new one and returns an error. Otherwise, it creates 
    a new group, saves it to the database, and returns the group's details.

    Args:
        group_admin_id (int): The ID of the user who will be the administrator of the group.
        group_name (str): The name of the group.
        group_description (str): A brief description of the group.

    Returns:
        dict: A dictionary representing the newly created group if successful.
              Returns an error message if the group already exists.

    Side Effects:
        - Queries the database to check for duplicate groups.
        - Adds a new group record to the database if no duplicate exists.
        - Commits the new group to the database session.
    """
    from models.group_model import Group, db

    # Check if a group with the same admin ID, name, and description already exists
    existing_group = Group.query.filter_by(
        group_admin_id=group_admin_id,
        group_name=group_name,
        group_description=group_description
    ).first()

    if existing_group:
        # Handle the case where the group already exists
        return {"message": "Group with the same admin_id, name, and description already exists."}

    new_group = Group(
        group_admin_id=group_admin_id,
        group_name=group_name,
        group_description=group_description,
        created_at=date.today(),
        created_at_time=datetime.now().time()
    )
    db.session.add(new_group)
    db.session.commit()
    return new_group.to_dict()