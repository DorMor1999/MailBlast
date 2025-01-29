from datetime import datetime

def convert_str_to_date(date_str: str) -> datetime.date:
    """
    Converts a date string in 'YYYY-MM-DD' format to a datetime.date object for database storage.

    Args:
        date_str (str): The date string to convert.

    Returns:
        datetime.date: The converted date object.
    """
    try:
        # Convert the string to a datetime.date object
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        # If the string format is incorrect, return None or handle the error as needed
        print("Invalid date format:", date_str)
        return None