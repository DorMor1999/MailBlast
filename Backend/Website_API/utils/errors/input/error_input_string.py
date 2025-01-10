from .input_validation import validate_input
from .input_error_messages import input_error_messages



def create_error_string(input_list: list) -> str:
    """
    Iterates over a list of dictionaries, where each dictionary contains an 'input' string and an 'input_type' string.
    Validates each input based on its type and builds an error string if validation fails.
    
    The function checks if the 'input' and 'input_type' keys exist in each dictionary and calls the appropriate
    validation function based on the 'input_type'. If validation fails, an error message specific to that input type
    is added to the error string. If either 'input' or 'input_type' is missing from the dictionary, an error message
    is added indicating the missing key(s).
    
    If all validations pass, the function returns an empty string, indicating no errors.

    Args:
        input_list (list): A list of dictionaries, each containing an 'input' string and an 'input_type' string.

    Returns:
        str: A string containing all the error messages for failed validations or missing keys.
             Returns an empty string if all inputs are valid.
    """
    error: str = ''
    for item in input_list:
        # Ensure both 'input' and 'input_type' keys exist in the dictionary
        if "input" in item and "input_type" in item:
            input_value = item["input"]
            input_type = item["input_type"]
        
            # Validate the input based on the type and append error message if validation fails
            if not validate_input(input_value, input_type):
                error += f"{input_error_messages[input_type]}\n"
        else:
            error += "Missing 'input' or 'input_type' in the dictionary\n"
    
    return error

