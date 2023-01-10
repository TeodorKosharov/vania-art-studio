from django.views.generic import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from vania_art_studio.account.forms import RegisterForm, LoginForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from vania_art_studio.account.common import get_picture_url
from vania_art_studio.products.common import get_template
from vania_art_studio.products.forms import SearchForm


class RegisterUserView(CreateView):
    template_name = get_template('register', 'account')
    form_class = RegisterForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = None
        return context


class LoginUserView(LoginView):
    template_name = get_template('login', 'account')
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = None
        return context


class ProfileUserView(LoginRequiredMixin, FormView):
    template_name = get_template('profile', 'account')
    form_class = ProfileForm
    success_url = '/account/profile/'

    def get(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_profile = request.user.profile
        context['profile'] = current_profile
        context['profile_picture_url'] = get_picture_url(current_profile, 'profile')
        context['search_form'] = SearchForm()
        return self.render_to_response(context)

    # We have to change the user of the form from 'owner' to user, otherwise IntegrityError is raised upon save()
    def form_valid(self, form):
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = self.request.user
            form.save()
            return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        current_profile = self.request.user.profile
        initial['first_name'] = current_profile.first_name
        initial['last_name'] = current_profile.last_name
        initial['age'] = current_profile.age
        initial['city'] = current_profile.city
        return initial


class LogoutUserView(LogoutView):
    pass
