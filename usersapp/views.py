from django.shortcuts import render
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from django.views.generic import CreateView, RedirectView
from .models import BlogUser
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View


# Create your views here.
class UserLoginView(LoginView):
    template_name = 'usersapp/login.html'

# class UserLogoutView(LogoutView):
#     def dispatch(self, request, *args, **kwargs):
#         # Обработка GET-запросов
#         if request.method == 'GET':
#             return self.get(request, *args, **kwargs)
#         # Обработка POST-запросов
#         return super().dispatch(request, *args, **kwargs)

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

class CustomLogoutView(RedirectView):
    url = reverse_lazy('usersapp:login')  # Перенаправляем на страницу входа после выхода
    permanent = False

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


# class UserLogoutView(LogoutView):
#     def get(self, request, *args, **kwargs):
#         response = super().get(request, *args, **kwargs)
#         return response


class UserCreateView(CreateView):
    model = BlogUser
    template_name = 'usersapp/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')
