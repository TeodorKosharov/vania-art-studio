from django.urls import path
from vania_art_studio.products.views import HomePage, CardsPage, AlbumsPage, FramesPage, \
    ChristeningSetsPage, ShoppingCartProducts, AddCard, AddAlbum, AddFrame, AddChristeningSet, product_details, \
    search_page, product_update, product_delete, add_to_cart, remove_from_cart, delete_comment, complete_order

urlpatterns = (
    path('', HomePage.as_view(), name='home page'),
    path('cards/', CardsPage.as_view(), name='cards page'),
    path('albums/', AlbumsPage.as_view(), name='albums page'),
    path('frames/', FramesPage.as_view(), name='frames page'),
    path('christening-set/', ChristeningSetsPage.as_view(), name='christening set page'),

    path('search/', search_page, name='search page'),

    path('add-card/', AddCard.as_view(), name='add card page'),
    path('add-album/', AddAlbum.as_view(), name='add album page'),
    path('add-frame/', AddFrame.as_view(), name='add frame page'),
    path('add-christeningset/', AddChristeningSet.as_view(), name='add christeningset page'),
    path('shopping-cart/', ShoppingCartProducts.as_view(), name='shopping cart'),

    path('details/<str:product>/<str:page>/<str:form_type>/<int:comment_id>/<int:pk>/', product_details,
         name='product details'),
    path('update/<str:product>/<int:pk>/', product_update, name='product update'),
    path('delete/<str:product>/<int:pk>/', product_delete, name='product delete'),
    path('add-to-cart/<str:product>/<int:pk>/', add_to_cart, name='add to cart'),
    path('remove-from-cart/<str:option>/<int:pk>/', remove_from_cart, name='remove from cart'),

    path('delete-comment/<int:comment_id>/<str:product>/<str:page>/<int:product_pk>/', delete_comment,
         name='delete comment'),

    path('complete-order/', complete_order, name='complete order')

)
