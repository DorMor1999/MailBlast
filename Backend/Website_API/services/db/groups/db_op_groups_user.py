def get_groups_of_user_by_user_id_sorted(user_id: int, sort: str, order: str) -> [dict]:
    """
    Retrieves groups of a user by user_id and sorts them based on the specified field and order.

    Args:
        user_id (int): The ID of the user whose groups are to be retrieved.
        sort (str): The field by which the results should be sorted ('group_name', 'group_description', 'created_at').
        order (str): The sorting order ('high_to_low' or 'low_to_high').

    Returns:
        list[dict]: A list of dictionaries representing the groups, sorted as requested.

    Raises:
        ValueError: If the provided sort field or order is invalid.
    """
    from models.group_model import Group, db
    from sqlalchemy import desc, asc

    # Validate sort field to prevent SQL injection
    valid_sort_fields = ['group_name', 'created_at', 'group_description']
    if sort not in valid_sort_fields:
        raise ValueError(f"Invalid sort field: '{sort}'. Must be one of {valid_sort_fields}.")
    
    # Validate order
    valid_orders = ['high_to_low', 'low_to_high']
    if order not in valid_orders:
        raise ValueError(f"Invalid order: '{order}'. Must be one of {valid_orders}.")

    # Determine the sorting order
    sort_order = desc if order == 'high_to_low' else asc

    # Sorting logic
    if sort == 'created_at':
        # Sort by both date and time
        groups = (
            db.session.query(Group)
            .filter(Group.group_admin_id == user_id)
            .order_by(sort_order(Group.created_at), sort_order(Group.created_at_time))
            .all()
        )
    else:
        # Sort by the specified field
        groups = (
            db.session.query(Group)
            .filter(Group.group_admin_id == user_id)
            .order_by(sort_order(getattr(Group, sort)))
            .all()
        )

    # Convert groups to a list of dictionaries using to_dict
    return [group.to_dict() for group in groups]
    