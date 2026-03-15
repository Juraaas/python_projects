import re

PLATE_PATTERN = re.compile(r'^[A-Z]{2,3}[A-Z0-9]{4,5}$')

def is_valid_plate(text):
    if text is None:
        return False
    
    text = text.replace(" ", "").upper()

    return bool(PLATE_PATTERN.match(text))