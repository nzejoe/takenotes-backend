from django.db.models import fields
from rest_framework import serializers

from .models import Account

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['password']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, style={'input_type':"password"})

    class Meta:
        model = Account
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']

        extra_kwargs  = {
            'password': {'write_only': True}
        }

    def save(self):

        username = self.validated_data.get('username')
        email = self.validated_data.get('email')
        first_name = self.validated_data.get('first_name')
        last_name = self.validated_data.get('last_name')
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')

        # check if password match
        if password != password2:
            raise serializers.ValidationError('The two password did not match!')
        
        # validate email and username
        if(Account.objects.filter(username=username).exists()):
            raise serializers.ValidationError(f'Account with that username already exists!')

        user = Account(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        # set user password
        user.set_password(password)
        user.save()
        return user