from django.db.models import fields
from rest_framework import serializers

from .models import Account

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password']
