from django.db import models
from vania_art_studio.products.common import Product


class Card(Product):
    pass


class Album(Product):
    pass


class Frame(Product):
    pass


class ChristeningSet(Product):
    pass


class ShoppingCart(models.Model):
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)


class Comments(models.Model):
    product = models.ForeignKey(Product, unique=False, on_delete=models.CASCADE)
    commentator_id = models.PositiveIntegerField(null=False, blank=False)
    comment = models.CharField(max_length=150, null=False, blank=False)
