from django.core.exceptions import ValidationError
import re
def validate_grade(value):
    if not value.isdigit():
        raise ValidationError(
            '%(value)s is not a valid grade. It must contain only numbers.',
            params={'value': value},
        )
    if len(value) > 5:
        raise ValidationError(
            '%(value)s is too long. It must be 5 characters or less.',
            params={'value': value},
        )






def validate_phone_number(value):
    # Regular expression to match +998 followed by exactly 9 digits
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError(
            'telefon raqam +998 dan boshlanishi va undan tashqari 9 ta sondan tashkil topishi kerak.'
        )




