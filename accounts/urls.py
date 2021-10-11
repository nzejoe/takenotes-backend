from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token

from .views import AccountListAPI, UserRegister


urlpatterns = [
   path('', AccountListAPI.as_view(), name='account_list'),
   path('login/', obtain_auth_token, name="login"),
   path('register/', UserRegister.as_view(), name="register"),
]
