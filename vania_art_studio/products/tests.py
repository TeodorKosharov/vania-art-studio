from django.core.exceptions import ValidationError
from django.test import TestCase
from vania_art_studio.products.common import Product
from vania_art_studio.products.validators import description_validator, price_validator, quantity_validator
from vania_art_studio.account.tests import get_encoded_str_from_given_value, get_encoded_str_from_raised_err


# Testing models:

class ProductModelTests(TestCase):
    def test_creating_product(self):
        product = Product(description='this is a test product', price=100, quantity=2, type='male', owner_id=1)
        product.full_clean()
        product.save()
        self.assertIsNotNone(product.pk)


# Testing validators:

class DescriptionValidatorTest(TestCase):
    def test_description_length_under_10_chars(self):
        description = 'abc'
        with self.assertRaises(ValidationError) as error:
            description_validator(description)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Описанието на продукта трябва да е минимум 10 символа')
        self.assertEqual(expected, actual)

    def test_description_length_more_than_200_chars(self):
        description = 'a' * 201
        with self.assertRaises(ValidationError) as error:
            description_validator(description)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Описанието на продукта не трябва да надвишава 200 символа')
        self.assertEqual(expected, actual)


class PriceValidatorTest(TestCase):
    def test_price_equals_zero(self):
        price = 0
        with self.assertRaises(ValidationError) as error:
            price_validator(price)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Цената на продукта не може да бъде 0 лв.')
        self.assertEqual(expected, actual)

    def test_negative_price(self):
        price = -100
        with self.assertRaises(ValidationError) as error:
            price_validator(price)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Цената на продукта не може да бъде отрицателно число')
        self.assertEqual(expected, actual)


class QuantityValidator(TestCase):
    def test_quantitiy_more_than_99(self):
        quantity = 100
        with self.assertRaises(ValidationError) as error:
            quantity_validator(quantity)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Максималната наличност не може да надхвърля 99')
        self.assertEqual(expected, actual)
