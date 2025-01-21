def get_group_by_group_id(group_id: int):
    """
    Retrieves a group from the database by its group_id.

    Args:
        group_id (int): The ID of the group to be retrieved.

    Returns:
        Group | None: The group object if found, otherwise None.
    """
    from models.group_model import Group
    return Group.query.get(group_id)
