from django.urls import path

# from rest_framework.authtoken.views import obtain_auth_token

from . import views


urlpatterns = [
    path('', views.AccountListAPI.as_view(), name='account_list'),
    path('login/', views.UserAuth.as_view(), name="login"),
    path('logout/', views.UserLogout.as_view(), name="logout"),
    path('register/', views.UserRegister.as_view(), name="register"),
    path('password_reset/', views.PasswordReset.as_view(), name="password_reset"),
    path('password_reset_complete/<uuid:pk>/',
         views.PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('password_reset_confirm/<uidb64>/<token>/',
         views.PasswordResetConfirm.as_view(), name="password_reset_confirm"),
]
