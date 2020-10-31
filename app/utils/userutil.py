import phonenumbers

from .dbutil import db_user

def username_taken(username) -> bool:
    return True if db_user(username=username) else False

def email_taken(email) -> bool:
    return True if db_user(email=email) else False

def phone_invalid(phone) -> bool:
    if not '+' in phone[0]:
        return True
    try:
        phone = phonenumbers.parse(phone, None)
        return False if phonenumbers.is_possible_number(phone) and phonenumbers.is_valid_number(phone) else True
    except:
        return True

def phone_taken(phone) -> bool:
    return True if db_user(phone=phone) else False

def format_phone(phone) -> str:
    phone = phonenumbers.parse(phone, None)
    return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
