import re
from datetime import datetime
from .countries_and_cities.countries import countries
from .countries_and_cities.cities import cities

def not_empty_input(input: str) -> bool:
    """
    Checks if the input string is not empty.
    Returns True if the string has a length greater than 0, otherwise False.
    """
    return len(input) > 0

def email_input(input: str) -> bool:
    """
    Validates if the input string is a valid email format.
    Uses regular expression to check if the email matches the pattern.
    Returns True if the email format is valid, otherwise False.
    """
    # Define a regular expression pattern for a valid email
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    
    # Use re.match to check if the email matches the pattern
    return bool(re.match(pattern, input))

def password_input(input: str) -> bool:
    """
    Validates if the input string has a minimum length of 6 characters (basic password validation).
    Returns True if the password length is 6 or more characters, otherwise False.
    """
    return len(input) >= 6

def check_country(input: str) -> bool:
    """
    Checks if the given input exists in the predefined `countries` set.
    
    Args:
        input (str): The country name to check.

    Returns:
        bool: True if the input is in `countries`, False otherwise.
    """
    return input in countries
    
def check_city(input: str) -> bool:
    """
    Checks if the given input exists in the predefined `cities` set.
    
    Args:
        input (str): The city name to check.

    Returns:
        bool: True if the input is in `cities`, False otherwise.
    """
    return input in cities

def check_date_format(date_str: str) -> bool:
    """
    Checks if the given input is a valid date in the format YYYY-MM-DD, 
    which is required for storing in a SQLAlchemy db.Date column.

    Args:
        date_str (str): The date string to check.

    Returns:
        bool: True if the input is a valid date in YYYY-MM-DD format, False otherwise.
    """
    try:
        # Attempt to parse the string into a datetime object
        datetime.strptime(date_str, "%Y-%m-%d").date()
        return True
    except (ValueError, TypeError):
        return False 

def check_birthday(date_str: str) -> bool:
    """
    Checks if the given input is a valid date in the format YYYY-MM-DD and that the date is not in the future.
    
    Args:
        date_str (str): The date string to check.

    Returns:
        bool: True if the input is a valid date in YYYY-MM-DD format and not in the future, False otherwise.
    """
    try:
        # Attempt to parse the string into a datetime object
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()

        # Check if the parsed date is in the future
        if parsed_date > datetime.today().date():
            return False  # Date is in the future
        
        return True
    except (ValueError, TypeError):
        return False  # Invalid format or type

def validate_input(input: str, check_type: str) -> bool:
    """
    Validates the input based on the specified check_type.
    - "first_name": Calls not_empty_input to check if the input is not empty.
    - "last_name": Calls not_empty_input to check if the input is not empty.
    - "group_name": Calls not_empty_input to check if the input is not empty.
    - "group_description": Calls not_empty_input to check if the input is not empty.
    - "email": Calls email_input to check if the input is a valid email.
    - "password": Calls password_input to check if the input is a valid password (min 6 characters).
    
    Returns True if the input passes the specified validation, otherwise False.
    If an invalid check_type is provided, returns False.
    """
    if check_type == "first_name" or check_type == "last_name" or check_type == "group_name" or check_type == "group_description":
        return input is not None and type(input) is str and not_empty_input(input)
    elif check_type == "email":
        return input is not None and type(input) is str and email_input(input)
    elif check_type == "password":
        return input is not None and type(input) is str and password_input(input)
    elif check_type == "country":
        return input is None or (input is not None and type(input) is str and check_country(input))
    elif check_type == "city":
        return input is None or (input is not None and type(input) is str and check_city(input))
    elif check_type == "birthday":
        return input is None or (input is not None and type(input) is str and check_birthday(input))
    
    # Returns False if the check_type doesn't match any of the expected types
    return False