#--------------------------------------------------  
# Compute the Luhn checksum of a number string. 
  # (str): A string containing only digits. 
  # int: The checksum modulo 10 (0 means valid Luhn).
#--------------------------------------------------

def luhn_checksum(number: str) -> int:
    total = 0
    # Reverse the digits because Luhn processes numbers from right to left
    digits = list(map(int, reversed(number)))
    
    for i, d in enumerate(digits):
        if i % 2 == 1:
            # Double every second digit from the right
            doubled = d * 2
            # If doubling gives a number > 9, subtract 9 (equivalent to summing its digits)
            total += doubled - 9 if doubled > 9 else doubled
        else:
            # Keep the other digits as-is
            total += d
    
    # Return modulo 10 of the total sum
    return total % 10

#--------------------------------------------------
# Check if a number passes the Luhn algorithm.
# Returns: bool: True if valid, False if invalid.
#--------------------------------------------------

def is_luhn_valid(number: str) -> bool:
    # A valid number will have a checksum modulo 10 equal to 0
    return luhn_checksum(number) == 0

#--------------------------------------------------
# Calculate the correct Luhn check digit for a given base number. 
# base_number (str): The number without the check digit. 
# Returns: str: The check digit as a string.
#--------------------------------------------------

def calculate_check_digit(base_number: str) -> str:
    # Append a '0' temporarily to calculate the checksum
    placeholder = base_number + '0'
    mod = luhn_checksum(placeholder)
    # The check digit is what makes the checksum divisible by 10
    return str((10 - mod) % 10)

#--------------------------------------------------
# Provide a step-by-step explanation of the Luhn calculation. 
# number (str): A string containing only digits.
#  Returns: dict: { 'steps': list of dictionaries for each digit, 'total': total sum, 'mod10': total modulo 10}
#--------------------------------------------------

def explain_calculation(number: str) -> dict:
    digits = list(map(int, number))  # Convert string to list of integers
    steps = []
    total = 0

    # Enumerate digits from right to left
    for pos_from_right, d in enumerate(reversed(digits)):
        # Calculate the position from the left for readability
        pos = len(digits) - 1 - pos_from_right
        entry = {'pos': pos, 'digit': d}

        if pos_from_right % 2 == 1:
            # Double every second digit from the right
            doubled = d * 2
            # Adjust if > 9
            adjusted = doubled - 9 if doubled > 9 else doubled
            entry.update({'doubled': doubled, 'adjusted': adjusted})
            total += adjusted
        else:
            # Digits not doubled stay the same
            entry.update({'doubled': None, 'adjusted': d})
            total += d

        # Append step info for later display
        steps.append(entry)

    # Reverse steps so they are in left-to-right order for readability
    steps = list(reversed(steps))

    return {'steps': steps, 'total': total, 'mod10': total % 10}
