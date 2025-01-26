import re

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
    
    # Returns False if the check_type doesn't match any of the expected types
    return False