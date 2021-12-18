import datetime
from django.core.exceptions import ValidationError


def validate_year(value):
    if value > datetime.date.today().year:
        raise ValidationError(
            ('%(value)s год не должен быть больше нынешнего!'),
            params={'value': value},
        )
