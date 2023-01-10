from vania_art_studio.products.common import Product
from vania_art_studio.products.forms import AddCardForm, AddAlbumForm, AddFrameForm, AddChristeningSetForm
from vania_art_studio.products.models import Card, Album, Frame, ChristeningSet, Comments


def get_clicked_product(product, pk):
    if product == 'card':
        return Card.objects.filter(pk=pk).get(pk=pk)
    elif product == 'album':
        return Album.objects.filter(pk=pk).get(pk=pk)
    elif product == 'frame':
        return Frame.objects.filter(pk=pk).get(pk=pk)
    elif product == 'christeningset':
        return ChristeningSet.objects.filter(pk=pk).get(pk=pk)


def get_product_form(product_category, product_instance, request_method, request_files=None, request_post=None):
    if product_category == 'card':
        if request_method == 'GET':
            return AddCardForm(instance=product_instance)
        else:
            return AddCardForm(request_post, request_files, instance=product_instance)

    elif product_category == 'album':
        if request_method == 'GET':
            return AddAlbumForm(instance=product_instance)
        else:
            return AddAlbumForm(request_post, request_files, instance=product_instance)

    elif product_category == 'frame':
        if request_method == 'GET':
            return AddFrameForm(instance=product_instance)
        else:
            return AddFrameForm(request_post, request_files, instance=product_instance)
    else:
        if request_method == 'GET':
            return AddChristeningSetForm(instance=product_instance)
        else:
            return AddChristeningSetForm(request_post, request_files, instance=product_instance)


def get_product_model_name(product_pk):
    if Card.objects.filter(pk=product_pk):
        return 'card'
    elif Album.objects.filter(pk=product_pk):
        return 'album'
    elif Frame.objects.filter(pk=product_pk):
        return 'frame'
    return 'christeningset'


def get_add_to_cart_value(class_name):
    class_names = {
        'CardsPage': 'card',
        'AlbumsPage': 'album',
        'FramesPage': 'frame',
        'ChristeningSetsPage': 'christeningset'
    }
    return class_names[class_name]


def sort_products(criteria, queryset, page):
    sorted_querysets = {
        'male_products': sorted(queryset, key=lambda x: x.type, reverse=True),
        'female_products': sorted(queryset, key=lambda x: x.type),
        'price_ascending': sorted(queryset, key=lambda x: x.price),
        'price_descending': sorted(queryset, key=lambda x: x.price, reverse=True),
        'quantity_ascending': sorted(queryset, key=lambda x: x.quantity if page == 'products' else x.cart_quantity),
        'quantity_descending': sorted(queryset, key=lambda x: x.quantity if page == 'products' else x.cart_quantity,
                                      reverse=True)
    }

    return sorted_querysets[criteria] if criteria else queryset


def sort_comments(criteria, comments, session):
    sorted_comments_collections = {
        'most_recent': comments.order_by('-id'),
        'oldest': comments.order_by('id'),
        None: comments.order_by('id')
    }

    if criteria:
        session['comment_criteria'] = criteria
    else:
        try:
            criteria = session['comment_criteria']
        except KeyError:
            session['comment_criteria'] = None

    return sorted_comments_collections[criteria]


def send_comment_form(form_type, comment_form, comment_id, clicked_product, user_pk):
    if form_type == 'add_comment':
        comment = comment_form.cleaned_data.get('comment')
        Comments.objects.create(product=clicked_product, commentator_id=user_pk, comment=comment)
    else:
        selected_comment = Comments.objects.filter(id=comment_id).get(id=comment_id)
        selected_comment.comment = comment_form.cleaned_data.get('comment')
        selected_comment.save()


def get_products_total_price(products_ids):
    total_price = 0

    for product_id in products_ids:
        product = Product.objects.filter(pk=product_id).get(pk=product_id)
        product_cart_quantity = product.cart_quantity
        total_price += product_cart_quantity * product.price

    return total_price


def get_products_based_on_search(search_result):
    cards_base_options = ('картичка', 'картички')
    cards_male_options = (
        'мъжки картички', 'мъжка картичка', 'картичка за мъже', 'картички за мъже',
        'картичка за момче', 'картички за момче', 'картичка за момчета', 'картички за момчета',
    )
    cards_female_options = (
        'женски картички', 'женска картичка', 'картичка за жени', 'картички за жени',
        'картичка за момиче', 'картички за момиче', 'картичка за момичета', 'картички за момичета',
    )

    albums_base_options = ('албум', 'албуми')
    albums_male_options = (
        'мъжки албум', 'мъжки албуми', 'албум за мъже', 'албуми за мъже',
        'албум за момче', 'албуми за момче', 'албум за момчета', 'албуми за момчета',
    )
    albums_female_options = (
        'женски албум', 'албум за жени', 'албуми за жени',
        'албум за момиче', 'албуми за момиче', 'албум за момичета', 'албуми за момичета',
    )

    frames_base_options = ('рамка', 'рамки')
    frames_male_options = (
        'мъжки рамки', 'мъжка рамка', 'рамка за мъже', 'рамки за мъже',
        'рамка за момче', 'рамки за момче', 'рамка за момчета', 'рамки за момчета',
    )
    frames_female_options = (
        'женски рамки', 'женска рамка', 'рамка за жени', 'рамки за жени',
        'рамка за момиче', 'рамки за момиче', 'рамка за момичета', 'рамки за момичета',
    )

    christeningset_base_options = ('кръщене', 'кръщенета')
    christeningset_male_options = (
        'мъжко кръщене', 'мъжки кръщенета', 'кръщене за мъже', 'кръщенета за мъже',
        'кръщене за момче', 'кръщенета за момче', 'кръщене за момчета', 'кръщенета за момчета',
    )
    christeningset_female_options = (
        'женско кръщене', 'кръщене за жени', 'кръщенета за жени',
        'кръщене за момиче', 'кръщенета за момиче', 'кръщене за момичета', 'кръщенета за момичета',
    )

    search_keys = {
        cards_base_options: Card.objects.all(),
        cards_male_options: Card.objects.filter(type='male'),
        cards_female_options: Card.objects.filter(type='female'),
        albums_base_options: Album.objects.all(),
        albums_male_options: Album.objects.filter(type='male'),
        albums_female_options: Album.objects.filter(type='female'),
        frames_base_options: Frame.objects.all(),
        frames_male_options: Frame.objects.filter(type='male'),
        frames_female_options: Frame.objects.filter(type='female'),
        christeningset_base_options: ChristeningSet.objects.all(),
        christeningset_male_options: ChristeningSet.objects.filter(type='male'),
        christeningset_female_options: ChristeningSet.objects.filter(type='female')
    }

    for options in search_keys.keys():
        encoded_options = [option.encode(encoding='utf-8') for option in options]

        if search_result.encode(encoding='utf-8') in encoded_options:
            try:
                add_to_cart_product = get_product_model_name(search_keys[options][0].pk)
            except IndexError:
                add_to_cart_product = None
            return search_keys[options], add_to_cart_product
    return [], None
