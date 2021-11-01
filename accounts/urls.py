from django.urls import path

# from rest_framework.authtoken.views import obtain_auth_token

from .views import AccountListAPI, PasswordReset,UserAuth, UserLogout, UserRegister


urlpatterns = [
   path('', AccountListAPI.as_view(), name='account_list'),
   path('login/', UserAuth.as_view(), name="login"),
   path('logout/', UserLogout.as_view(), name="logout"),
   path('register/', UserRegister.as_view(), name="register"),
   path('password_reset/', PasswordReset.as_view(), name="password_reset"),
]
