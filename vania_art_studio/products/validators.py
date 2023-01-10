from django.core.exceptions import ValidationError


def description_validator(value: str):
    if len(value) < 10:
        raise ValidationError('Описанието на продукта трябва да е минимум 10 символа')
    elif len(value) > 200:
        raise ValidationError('Описанието на продукта не трябва да надвишава 200 символа')


def price_validator(value: float):
    if value == 0:
        raise ValidationError('Цената на продукта не може да бъде 0 лв.')
    elif value < 0:
        raise ValidationError('Цената на продукта не може да бъде отрицателно число')


def quantity_validator(value: int):
    if value > 99:
        raise ValidationError('Максималната наличност не може да надхвърля 99')
