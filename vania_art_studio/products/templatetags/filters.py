from django.contrib.auth import get_user_model
from django.template import Library
from vania_art_studio.account.models import Profile
from vania_art_studio.account.common import get_picture_url

register = Library()
UserModel = get_user_model()


@register.filter('get_product_name')
def get_product_name(value: str):
    return value.__class__.__name__.lower()


@register.filter('get_commentator_profile_img')
def get_commentator_profile_img(commentator_id):
    return get_picture_url(Profile.objects.filter(pk=commentator_id).get(pk=commentator_id), 'profile')


@register.filter('get_commentator_username')
def get_commentator_username(commentator_id):
    return UserModel.objects.filter(pk=commentator_id).get(pk=commentator_id).username
