from django.urls import path, include
from usersapp import views
from django.contrib.auth.views import LogoutView

from usersapp.views import UserLogoutView

app_name = 'usersapp'

# views.main_view()
# urlpatterns = [
#     path('login/', views.UserLoginView.as_view(), name='login'),
#     path('logout/', LogoutView.as_view(), name='logout'),
#     path('register/', views.UserCreateView.as_view(), name='register'),
#     #path('users/', include('usersapp.urls', namespace='users')),  # Вот эта строка
# ]

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(), name='logout'),
    #path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.UserCreateView.as_view(), name='register'),
    # path('users/', include('usersapp.urls', namespace='users')),  # Вот эта строка
]
