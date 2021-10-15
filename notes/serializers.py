from django.utils.text import slugify
from rest_framework import serializers

from .models import Note, Label



class NoteSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Note
        fields = '__all__'

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
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Label
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data['author']
        name = validated_data['name']
        name_exists = Label.objects.filter(slug=slugify(name), author=user)
        if name_exists:
            raise serializers.ValidationError({'name': 'Name already exists!'})
        return Label.objects.create(**validated_data)


