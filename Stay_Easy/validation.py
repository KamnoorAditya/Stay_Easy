def validate_name(name):
    if name=="":
        return False
    else:
        return True
def validate_mobile(mobile):
    if len(mobile)!=10:
        return False
    if not mobile.isdigit():
        return False
    if mobile[0] not in "6789":
        return False
    return True
def validate_email(email):
    if "@" not in email:
        return False
    if "." not in email:
        return False
    return True