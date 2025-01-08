# Decode bytes if necessary and handle null cases
def safe_decode(value):
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return value