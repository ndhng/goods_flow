from random import choices, randint

# Number of new dates
def next_date(true_weight:float, max_days: int) -> int:
    """
    returns the number of days to move forward based on the true_weight and max_days allowed
    :param true_weight: the frequency that a new date will happen
    :param max_days: the maximum number of days to move forward
    :return: the number of days to move forward (or 0 if no new date)
    """
    if_new_date = choices([True,False], [true_weight, 1-true_weight])[0]
    if if_new_date:
        return randint(1,max_days)
    else:
        return 0

# Code generation
def generate_code(header: str, zeros_length: int, code_number: int) -> (str, int):
    """
    Generates a formatted code string by appending the given header
    followed by the code_number zero-padded to a specified length.
    It also increments and returns the updated code_number.

    :param header: A string representing the header or prefix for the
        generated code.
    :param zeros_length: An integer representing the total length of
        the zero-padded number part in the generated code.
    :param code_number: An integer representing the number to be
        formatted and appended to the header.

    :return: A tuple where the first element is the generated code as
        a string, and the second element is the updated code_number
        as an integer.
    """
    code = header + str(code_number).zfill(zeros_length)
    code_number += 1
    return code, code_number

def generate_code_item(header: str,
                       zeros_length: int,
                       code_number: int,
                       code_item_number: int,
                       combined_freq: float) -> (str, str, int, int):
    """
    Generates a unique code item based on the provided header, a sequence number,
    and a probabilistic decision. The code item is returned along with the updated
    code, sequence number, and item number. If a new code is generated, the code
    item number resets to 1; otherwise, it increments by 1.

    :param header: A string prefix included in the generated code.
    :param zeros_length: Number of zeros to pad the numeric portion of the code.
    :param code_number: Current sequence number used in generating the code.
    :param code_item_number: Current sequence number for the specific code item.
    :param combined_freq: Float representing the probability of creating a new
        code. Must be a value between 0.0 and 1.0, where higher values increase
        the likelihood of new code generation.

    :return: A tuple containing:
        - code_item (str): The full generated code item including its sequence
          number.
        - code (str): The generated code based on the header and sequence number.
        - code_number (int): The updated sequence number used for generating the
          code.
        - code_item_number (int): The updated sequence number for the code item.
    """
    if_new_code = choices([True,False], [combined_freq, 1-combined_freq])[0]

    if if_new_code:
        code, code_number = generate_code(header, zeros_length, code_number)
    else:
        code = header + str(code_number).zfill(zeros_length)

    code_item = code + '-' + str(code_item_number).zfill(2)

    if if_new_code:
        code_item_number = 1
    else:
        code_item_number += 1

    return code_item, code, code_number, code_item_number