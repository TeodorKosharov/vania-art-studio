from enum import Enum
from django.contrib.auth import get_user_model
from django.db import models
from cloudinary.models import CloudinaryField
from django.urls import reverse_lazy
from vania_art_studio.products.validators import description_validator, price_validator, quantity_validator

UserModel = get_user_model()


class ProductTypeChoices(Enum):
    male = 'Мъжки продукт'
    female = 'Женски продукт'

    @classmethod
    def choices(cls):
        return [(x.name, x.value) for x in cls]


class Product(models.Model):
    description = models.TextField(null=False, blank=False, validators=(description_validator,))
    product_image = CloudinaryField('image')
    price = models.FloatField(null=False, blank=False, validators=(price_validator,))
    quantity = models.PositiveIntegerField(null=False, blank=False, validators=(quantity_validator,))
    type = models.CharField(max_length=6, null=False, blank=False, choices=ProductTypeChoices.choices())
    owner_id = models.IntegerField(null=True, blank=True)
    cart_quantity = models.PositiveIntegerField(null=True, blank=True, default=0)


# The following functions are used in views.py:

def get_template(template: str, prefix: str):
    if prefix == 'account':
        return f'account/{template}-page.html'
    elif prefix == 'products':
        return f'products/{template}.html'
    elif prefix == 'products-add':
        return f'products/add-{template}.html'


def get_permissions(product: str):
    return f'products.add_{product}', \
           f'products.change_{product}', \
           f'products.delete_{product}', \
           f'products.view_{product}'


def is_user_authorized(required_perms, user, product_owner):
    if user.is_superuser:
        return True
    if not all([user.has_perm(perm) for perm in required_perms]) or user.pk != product_owner:
        return False
    return True


def set_product_owner_and_redirect(ProductClass, user_id: int, redirect_url_name: str):
    product = ProductClass.objects.last()
    product.owner_id = user_id
    product.save()
    return reverse_lazy(redirect_url_name)
