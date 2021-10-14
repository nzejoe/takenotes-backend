from rest_framework import serializers

from .models import Note, Label



class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        exclude = ['author']

    def create(self, validated_data):
        return Note.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.label = validated_data.get('label', instance.label)
        instance.save()
        return instance


class LabelSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    class Meta:
        model = Label
        fields = "__all__"

