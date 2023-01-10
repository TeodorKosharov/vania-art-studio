from django.urls import path
from vania_art_studio.account.views import RegisterUserView, LoginUserView, ProfileUserView, LogoutUserView

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register page'),
    path('login/', LoginUserView.as_view(), name='login page'),
    path('profile/', ProfileUserView.as_view(), name='profile page'),
    path('logout/', LogoutUserView.as_view(), name='logout user')
)
