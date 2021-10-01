from rest_framework import serializers

from .models import Note, Label

class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['name']


class NoteSerializer(serializers.ModelSerializer):
     class Meta:
        model = Note
        fields = ['title', 'text','label', 'created', 'updated']