from django.views.generic import ListView
from vania_art_studio.account.common import get_picture_url
from vania_art_studio.products.forms import FilterProductsForm, FilterViewProductsForm, SearchForm
from vania_art_studio.products.utils import get_add_to_cart_value, sort_products


class BaseProductMixin(ListView):
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        context = self.get_context_data(**kwargs)
        context['user'] = request.user if request.user.__class__.__name__ != 'AnonymousUser' else None
        context['add_to_cart_product'] = get_add_to_cart_value(self.__class__.__name__)
        context['filter_form'] = FilterProductsForm(initial={'field': self.request.session['criteria']})
        context['search_form'] = SearchForm()

        columns_criteria = self.request.GET.get('products_per_row')

        if columns_criteria:
            # updating the session:
            self.request.session['columns_criteria'] = columns_criteria
        else:
            try:
                # If we are coming at that page for the first time:
                columns_criteria = self.request.session['columns_criteria']
            except KeyError:
                self.request.session['columns_criteria'] = 3

        context['view_products_form'] = FilterViewProductsForm(initial={'products_per_row': columns_criteria})
        context['products_per_row'] = self.request.session['columns_criteria']

        return self.render_to_response(context)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = sorted(queryset, key=lambda product: product.pk)
        for index in range(len(queryset)):
            queryset[index].product_image = get_picture_url(queryset[index], 'product')

        """
            Firstly I am getting the criteria from the result of FilterProductsForm.
            If the form is not submitted, the criteria is None, meaning I am
            getting in else clause. There I try to get the criteria from the
            session. If it does not exist, then I am setting it in the session
            with value None. If the form is submitted we are getting into if 
            clause where the criteria is being saved/updated in the session.
            When refreshing the page, last used criteria is being extracted 
            from the session, meaning the products will still be sorted.
        """

        criteria = self.request.GET.get('field')
        if criteria:
            self.request.session['criteria'] = criteria
        else:
            try:
                criteria = self.request.session['criteria']
            except KeyError:
                self.request.session['criteria'] = None

        return sort_products(criteria, queryset, 'products')
