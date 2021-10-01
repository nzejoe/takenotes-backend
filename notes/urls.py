from django.urls import path

from .views import Notes, NoteDetail, Labels


urlpatterns = [
   path('', Notes.as_view(), name='notes'),
   path('<uuid:pk>/', NoteDetail.as_view(), name="note_detail"),
   path('labels/', Labels.as_view(), name='notes'),
]
