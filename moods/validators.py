from datetime import date

from django.core.exceptions import ValidationError


def date_validator(value):
    if value > date.today():
        raise ValidationError('Date can not be in the future.')