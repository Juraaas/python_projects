import re

PLATE_PATTERN = re.compile(r'^[A-Z0-9]{5,8}$')

def is_valid_plate(text):
    if text is None:
        return False
    text = text.replace(" ", "").upper()

    return bool(PLATE_PATTERN.match(text))