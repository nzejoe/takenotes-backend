from django.urls import path

from .views import Notes, Labels


urlpatterns = [
   path('', Notes.as_view(), name='notes'),
   path('labels/', Labels.as_view(), name='notes'),
]
