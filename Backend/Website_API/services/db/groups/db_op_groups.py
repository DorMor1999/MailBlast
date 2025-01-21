from datetime import date, datetime

def add_new_group(group_admin_id: int, group_name: str, group_description: str) -> None:
    """
    Adds a new group to the database.

    Args:
        group_admin_id (int): The ID of the user who will be the administrator of the group.
        group_name (str): The name of the group.
        group_description (str): A brief description of the group.

    Returns:
        None: This function does not return a value but commits the new group to the database.
    
    Side Effects:
        - Adds a new group record to the database.
        - Commits the new group to the database session.
    """
    from models.group_model import Group, db
    new_group = Group(
        group_admin_id=group_admin_id,
        group_name=group_name,
        group_description=group_description,
        created_at=date.today(),
        created_at_time=datetime.now().time()
    )
    db.session.add(new_group)
    db.session.commit()