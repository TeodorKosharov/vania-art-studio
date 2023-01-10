import re


def get_picture_url(record, model):
    if model == 'profile':
        try:
            profile_picture_url = re.findall(r'(?<=\<img src=").+(?="\/>)', record.profile_picture.image())[0]
        except IndexError:
            profile_picture_url = None
        return profile_picture_url
    elif model == 'product':
        try:
            product_image_url = re.findall(r'(?<=\<img src=").+(?="\/>)', record.product_image.image())[0]
        except IndexError:
            product_image_url = None
        return product_image_url
