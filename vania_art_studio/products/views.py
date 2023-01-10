from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from vania_art_studio.products.models import Card, Album, Frame, ChristeningSet, ShoppingCart, Comments
from vania_art_studio.products.forms import AddCardForm, AddAlbumForm, AddFrameForm, AddChristeningSetForm, \
    FilterProductsForm, FilterViewProductsForm, FilterCommentsForm, AddCommentForm, EditCommentForm, SearchForm
from vania_art_studio.products.common import get_template, get_permissions, set_product_owner_and_redirect, \
    is_user_authorized, Product
from vania_art_studio.account.common import get_picture_url
from vania_art_studio.products.utils import get_clicked_product, get_product_form, get_product_model_name, \
    sort_products, sort_comments, send_comment_form, get_products_total_price, get_products_based_on_search
from vania_art_studio.products.mixins import BaseProductMixin


class HomePage(ListView):
    model = Comments
    template_name = get_template('home', 'products')
    context_object_name = 'comments'
    paginate_by = 4

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = self.get_context_data(*args, **kwargs)
        user = request.user if request.user.__class__.__name__ != 'AnonymousUser' else None
        context['user'] = user
        context['search_form'] = SearchForm()

        # Cleaning the shopping cart if the user is logged out:
        if user is None:
            for _ in range(len(ShoppingCart.objects.all())):
                cart_product = ShoppingCart.objects.all()[0]
                product = Product.objects.filter(pk=cart_product.product_id).get(pk=cart_product.product_id)
                product.quantity += product.cart_quantity
                product.cart_quantity = 0
                product.save()
                ShoppingCart.objects.all()[0].delete()

        return self.render_to_response(context)


class CardsPage(BaseProductMixin):
    model = Card
    template_name = get_template('cards', 'products')
    context_object_name = 'cards'


class AlbumsPage(BaseProductMixin):
    model = Album
    template_name = get_template('albums', 'products')
    context_object_name = 'albums'


class FramesPage(BaseProductMixin):
    model = Frame
    template_name = get_template('frames', 'products')
    context_object_name = 'frames'


class ChristeningSetsPage(BaseProductMixin):
    model = ChristeningSet
    template_name = get_template('christening-set', 'products')
    context_object_name = 'christening_sets'


class ShoppingCartProducts(LoginRequiredMixin, ListView):
    model = ShoppingCart
    template_name = get_template('shopping-cart', 'products')
    context_object_name = 'cart_products'

    def get_queryset(self):
        queryset = list(super().get_queryset())
        queryset = sorted(queryset, key=lambda product: product.pk)

        """
         The records in ShoppingCart model are simple objects, containing
         only the product_id. That is why I am overriding the queryset -
         every object in it becomes a product object with all its properties
         (description, price, ect...). I am adding extra property to every 
         object - model_name, which is used for details page. 
        """

        for index in range(len(queryset)):
            queryset[index] = Product.objects.filter(pk=queryset[index].product_id).get(pk=queryset[index].product_id)
            queryset[index].product_image = get_picture_url(queryset[index], 'product')
            queryset[index].model_name = get_product_model_name(queryset[index].pk)

        criteria = self.request.GET.get('field')

        if criteria:
            self.request.session['criteria'] = criteria
        else:
            try:
                criteria = self.request.session['criteria']
            except KeyError:
                self.request.session['criteria'] = None

        return sort_products(criteria, queryset, 'cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_cart_empty'] = True if not ShoppingCart.objects.all() else False
        context['cart_page'] = True
        context['filter_form'] = FilterProductsForm(initial={'field': self.request.session['criteria']})
        context['search_form'] = SearchForm()

        columns_criteria = self.request.GET.get('products_per_row')

        if columns_criteria:
            self.request.session['columns_criteria'] = columns_criteria
        else:
            try:
                columns_criteria = self.request.session['columns_criteria']
            except KeyError:
                self.request.session['columns_criteria'] = 3

        context['view_products_form'] = FilterViewProductsForm(initial={'products_per_row': columns_criteria})
        context['products_per_row'] = self.request.session['columns_criteria']

        if not context['is_cart_empty']:
            context['total_price'] = get_products_total_price(
                [cart_product.product_id for cart_product in ShoppingCart.objects.all()])
        return context


class AddCard(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = get_template('card', 'products-add')
    form_class = AddCardForm
    permission_required = get_permissions('card')
    extra_context = {'search_form': SearchForm()}

    def get_success_url(self):
        return set_product_owner_and_redirect(Card, self.request.user.id, 'cards page')


class AddAlbum(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = get_template('album', 'products-add')
    form_class = AddAlbumForm
    permission_required = get_permissions('album')
    extra_context = {'search_form': SearchForm()}

    def get_success_url(self):
        return set_product_owner_and_redirect(Album, self.request.user.id, 'albums page')


class AddFrame(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = get_template('frame', 'products-add')
    form_class = AddFrameForm
    permission_required = get_permissions('frame')
    extra_context = {'search_form': SearchForm()}

    def get_success_url(self):
        return set_product_owner_and_redirect(Frame, self.request.user.id, 'frames page')


class AddChristeningSet(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = get_template('christeningset', 'products-add')
    form_class = AddChristeningSetForm
    permission_required = get_permissions('christeningset')
    extra_context = {'search_form': SearchForm()}

    def get_success_url(self):
        return set_product_owner_and_redirect(ChristeningSet, self.request.user.id, 'christening set page')


def search_page(request):
    search_result = request.GET.get('search')
    product_list = []
    add_to_cart_product = None

    # Saving the search result in session is needed, because the page is reloaded when using filter forms
    if search_result:
        request.session['search_result'] = search_result
    else:
        if 'search_result' in request.session.keys():
            search_result = request.session['search_result']

    # Filter form criteria:
    criteria = request.GET.get('field')

    if criteria:
        request.session['criteria'] = criteria
    else:
        try:
            criteria = request.session['criteria']
        except KeyError:
            request.session['criteria'] = None
    #####

    # View products form:
    products_per_row = request.GET.get('products_per_row')

    if products_per_row:
        request.session['products_per_row'] = products_per_row
    else:
        try:
            products_per_row = request.session['products_per_row']
        except KeyError:
            request.session['products_per_row'] = None
    #####

    product_list, add_to_cart_product = get_products_based_on_search(search_result.lower().strip())
    product_list = sorted(product_list, key=lambda product: product.pk)

    for index in range(len(product_list)):
        product_list[index].product_image = get_picture_url(product_list[index], 'product')

    context = {
        'user': request.user if request.user.__class__.__name__ != 'AnonymousUser' else None,
        'search_form': SearchForm(initial={'search': search_result}),
        'object_list': sort_products(criteria, product_list, 'products'),
        'add_to_cart_product': add_to_cart_product,
        'filter_form': FilterProductsForm(initial={'field': criteria}),
        'view_products_form': FilterViewProductsForm(initial={'products_per_row': products_per_row}),
        'products_per_row': products_per_row
    }

    return render(request, 'products/search-page.html', context)


def product_details(request, product, page, form_type, comment_id, pk):
    clicked_product = get_clicked_product(product, pk)
    clicked_product.product_image = get_picture_url(clicked_product, 'product')
    user = request.user if request.user.__class__.__name__ != 'AnonymousUser' else None
    url_names = {
        'card': 'cards page',
        'album': 'albums page',
        'frame': 'frames page',
        'christeningset': 'christening set page',
        'cart': 'shopping cart',
        'search': 'search page'
    }

    add_comment_form = AddCommentForm()
    edit_comment_form = EditCommentForm()
    comments = sort_comments(request.GET.get('field'), Comments.objects.filter(product_id=pk), request.session)

    # page variable is used for going back url

    if request.method == 'POST':
        if form_type == 'add_comment':
            add_comment_form = AddCommentForm(request.POST)
            if add_comment_form.is_valid():
                send_comment_form('add_comment', add_comment_form, comment_id, clicked_product, user.pk)
                return redirect('product details', product=product, page=page, form_type=None, comment_id=0, pk=pk)

        elif form_type == 'edit_comment':
            edit_comment_form = EditCommentForm(request.POST)
            if edit_comment_form.is_valid():
                send_comment_form('edit_comment', edit_comment_form, comment_id, clicked_product, user.pk)
                return redirect('product details', product=product, page=page, form_type=None, comment_id=0, pk=pk)

    context = {
        'product': clicked_product,
        'user': user,
        'back_url': url_names[product] if page == 'products' else url_names[page],
        'add_comment_form': add_comment_form,
        'edit_comment_form': edit_comment_form,
        'filter_form': FilterCommentsForm(initial={'field': request.session['comment_criteria']}),
        'comments': comments,
        'page': page,
        'search_form': SearchForm()

    }

    return render(request, 'products/product-details.html', context)


@login_required()
def product_update(request, product, pk):
    selected_product = get_clicked_product(product, pk)
    user = request.user if request.user.__class__.__name__ != 'AnonymousUser' else None

    if not is_user_authorized(get_permissions(product), request.user, selected_product.owner_id):
        return HttpResponseForbidden()

    if request.method == 'GET':
        form = get_product_form(product, selected_product, request.method)
    else:
        form = get_product_form(product, selected_product, request.method, request.FILES, request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'{product}s page') if product != 'christeningset' else redirect('christening set page')

    context = {
        'product': selected_product,
        'form': form,
        'user': user,
        'search_form': SearchForm()
    }

    return render(request, 'products/product-update.html', context)


@login_required()
def product_delete(request, product, pk):
    selected_product = get_clicked_product(product, pk)
    if not is_user_authorized(get_permissions(product), request.user, selected_product.owner_id):
        return HttpResponseForbidden()
    selected_product.delete()
    return redirect(f'{product}s page') if product != 'christeningset' else redirect('christening set page')


@login_required()
def add_to_cart(request, product, pk):
    product_instance = Product.objects.filter(pk=pk).get(pk=pk)
    product_instance.quantity -= 1
    product_instance.cart_quantity += 1
    product_instance.save()

    if product_instance.pk not in [cart_product.product_id for cart_product in ShoppingCart.objects.all()]:
        ShoppingCart.objects.create(product=product_instance)

    if '/search/' in str(request.META.get('HTTP_REFERER')):
        return redirect('search page')
    return redirect(f'{product}s page') if product != 'christeningset' else redirect('christening set page')


@login_required()
def remove_from_cart(request, option, pk):
    product_instance = Product.objects.filter(pk=pk).get(pk=pk)
    if option == 'one':
        product_instance.cart_quantity -= 1
        product_instance.quantity += 1
        product_instance.save()

        if product_instance.cart_quantity == 0:
            ShoppingCart.objects.get(product_id=pk).delete()
    else:
        product_instance.quantity += product_instance.cart_quantity
        product_instance.cart_quantity = 0
        product_instance.save()
        ShoppingCart.objects.get(product_id=pk).delete()

    return redirect('shopping cart')


@login_required()
def delete_comment(request, comment_id, product, page, product_pk):
    Comments.objects.filter(id=comment_id).get(id=comment_id).delete()
    return redirect('product details', product=product, page=page, form_type=None, comment_id=0, pk=product_pk)


@login_required()
def complete_order(request):
    for cart_product in ShoppingCart.objects.all():
        product = Product.objects.filter(pk=cart_product.product_id).get(pk=cart_product.product_id)
        product.cart_quantity = 0
        product.save()

    ShoppingCart.objects.all().delete()
    return redirect('home page')
