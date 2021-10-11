from django.urls import path

# from rest_framework.authtoken.views import obtain_auth_token

from .views import AccountListAPI,UserAuth, UserRegister


urlpatterns = [
   path('', AccountListAPI.as_view(), name='account_list'),
   path('login/', UserAuth.as_view(), name="login"),
   path('register/', UserRegister.as_view(), name="register"),
]
