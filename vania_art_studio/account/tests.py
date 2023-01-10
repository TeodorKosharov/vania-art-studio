from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model
from vania_art_studio.account.forms import RegisterForm
from vania_art_studio.account.models import Profile
from vania_art_studio.account.validators import username_validator, first_name_validator, last_name_validator, \
    city_validator

UserModel = get_user_model()


# utils:
def get_model_field_validation_message(field_name, max_chars, actual_chars):
    return f"{{'{field_name}': ['Ensure this value has at most {max_chars} characters (it has {actual_chars}).']}}"


def get_encoded_str_from_given_value(value):
    return f"['{value}']".encode(encoding='utf-8')


def get_encoded_str_from_raised_err(value):
    return value.encode(encoding='utf-8')


# Testing models:
class AppUserModelTests(TestCase):
    def test_creating_appuser(self):
        user = UserModel(username='Teodor', password='12345678pass', email='teo@abv.bg')
        user.full_clean()  # Call this for validation
        user.save()
        self.assertIsNotNone(user.pk)

    def test_appuser_username_invalid_length(self):
        user = UserModel(username='T' * 21, password='12345678pass', email='teo@abv.bg')
        with self.assertRaises(Exception) as error:
            user.full_clean()
        self.assertEqual(get_model_field_validation_message('username', 20, 21), str(error.exception))


class ProfileModelTests(TestCase):
    def test_creating_profile(self):
        user = UserModel(username='Teodor', password='12345678pass', email='teo@abv.bg')
        user.save()
        profile = Profile(first_name='Teodor', last_name='Plamenov', age=21, city='Sofia', user=user)
        profile.full_clean()
        profile.save()
        self.assertIsNotNone(profile.pk)

    def test_profile_first_name_invalid_length(self):
        user = UserModel(username='Teodor', password='12345678pass', email='teo@abv.bg')
        user.save()
        profile = Profile(first_name='T' * 21, last_name='Plamenov', age=21, city='Sofia', user=user)
        with self.assertRaises(Exception) as error:
            profile.full_clean()
        self.assertEqual(get_model_field_validation_message('first_name', 20, 21), str(error.exception))

    def test_profile_last_name_invalid_length(self):
        user = UserModel(username='Teodor', password='12345678pass', email='teo@abv.bg')
        user.save()
        profile = Profile(first_name='Teodor', last_name='P' * 21, age=21, city='Sofia', user=user)
        with self.assertRaises(Exception) as error:
            profile.full_clean()
        self.assertEqual(get_model_field_validation_message('last_name', 20, 21), str(error.exception))

    def test_profile_city_invalid_length(self):
        user = UserModel(username='Teodor', password='12345678pass', email='teo@abv.bg')
        user.save()
        profile = Profile(first_name='Teodor', last_name='Plamenov', age=21, city='S' * 31, user=user)
        with self.assertRaises(Exception) as error:
            profile.full_clean()
        self.assertEqual(get_model_field_validation_message('city', 30, 31), str(error.exception))


# Testing Forms:

class RegisterFormTests(TestCase):
    def test_creating_profile_upon_registration(self):
        data = {
            'username': 'Teodor',
            'email': 'teo@abv.bg',
            'password1': '12345678pass',
            'password2': '12345678pass'
        }
        form = RegisterForm(data)
        form.save()
        created_profile = Profile.objects.get(pk=1)
        self.assertTrue(form.is_valid())
        self.assertIsNotNone(created_profile)

    def test_valid_data(self):
        data = {
            'username': 'Teodor',
            'email': 'teo@abv.bg',
            'password1': '12345678pass',
            'password2': '12345678pass'
        }
        form = RegisterForm(data)
        self.assertTrue(form.is_valid())

    def test_invalid_data(self):
        data = {
            'username': 'Teodor',
            'email': 'teo@abv.bg',
            'password1': '12345678pass',
            'password2': '12345678p'
        }
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())


# Testing validators:

class UsernameValidatorTest(TestCase):
    def test_username_containing_only_numbers(self):
        username = '12345'
        with self.assertRaises(ValidationError) as error:
            username_validator(username)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Потребителското име не може да бъде число')
        self.assertEqual(expected, actual)

    def test_username_containing_chars_other_than_numbers_and_letters(self):
        username = 'test123#'
        with self.assertRaises(ValidationError) as error:
            username_validator(username)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Потребителското име може да съдържа само букви и цифри')
        self.assertEqual(expected, actual)

    def test_username_invalid_length(self):
        username = 'ab'
        with self.assertRaises(ValidationError) as error:
            username_validator(username)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Потребителското име трябва да е минимум 3 символа')
        self.assertEqual(expected, actual)


class FirstNameValidatorTest(TestCase):
    def test_first_name_containing_only_numbers(self):
        first_name = '12345'
        with self.assertRaises(ValidationError) as error:
            first_name_validator(first_name)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Името не може да съдържа цифри')
        self.assertEqual(expected, actual)

    def test_first_name_invalid_length(self):
        first_name = 'a'
        with self.assertRaises(ValidationError) as error:
            first_name_validator(first_name)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Името трябва да съдържа минимум 2 букви')
        self.assertEqual(expected, actual)


class LastNameValidatorTest(TestCase):
    def test_last_name_containing_only_numbers(self):
        last_name = '12345'
        with self.assertRaises(ValidationError) as error:
            last_name_validator(last_name)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Фамилията не може да съдържа цифри')
        self.assertEqual(expected, actual)

    def test_last_name_invalid_length(self):
        first_name = 'a'
        with self.assertRaises(ValidationError) as error:
            last_name_validator(first_name)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Фамилията трябва да съдържа минимум 2 букви')
        self.assertEqual(expected, actual)


class CityValidatorTest(TestCase):
    def test_city_containing_only_numbers(self):
        city = '123'
        with self.assertRaises(ValidationError) as error:
            city_validator(city)
        actual = get_encoded_str_from_raised_err(str(error.exception))
        expected = get_encoded_str_from_given_value('Името на града не може да съдържа цифри')
        self.assertEqual(expected, actual)
