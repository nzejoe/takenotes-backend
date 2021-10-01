from django.urls import path

from .views import AccountListAPI


urlpatterns = [
   path('', AccountListAPI.as_view(), name='account_list')
]
