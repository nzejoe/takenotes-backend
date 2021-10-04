from django.urls import path

from .views import (
    Notes,
    NoteDetail,
    Labels,
    LabelDetail
)


urlpatterns = [
    path('notes/', Notes.as_view(), name='notes'),
    path('notes/<uuid:pk>/', NoteDetail.as_view(), name="note_detail"),
    path('labels/', Labels.as_view(), name='labels'),
    path('labels/<int:pk>/', LabelDetail.as_view(), name='label_detail'),
]
