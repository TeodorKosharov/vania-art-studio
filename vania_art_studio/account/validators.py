from django.core.exceptions import ValidationError


def username_validator(value: str):
    if value.isnumeric():
        raise ValidationError('Потребителското име не може да бъде число')
    if not value.isalnum():
        raise ValidationError('Потребителското име може да съдържа само букви и цифри')
    if len(value) < 3:
        raise ValidationError('Потребителското име трябва да е минимум 3 символа')


def first_name_validator(value: str):
    if value:
        if not value.isalpha():
            raise ValidationError('Името не може да съдържа цифри')
        if len(value) == 1:
            raise ValidationError('Името трябва да съдържа минимум 2 букви')


def last_name_validator(value: str):
    if value:
        if not value.isalpha():
            raise ValidationError('Фамилията не може да съдържа цифри')
        if len(value) == 1:
            raise ValidationError('Фамилията трябва да съдържа минимум 2 букви')


def city_validator(value: str):
    if not value.isalpha():
        raise ValidationError('Името на града не може да съдържа цифри')
