from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView 

from .models import Account
from .serializers import AccountsSerializer, UserRegistrationSerializer


class AccountListAPI(APIView):
    
    def get(self, request):
        accounts = Account.objects.all()
        serializer = AccountsSerializer(accounts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        accounts = Account.objects.all()
        serializer = AccountsSerializer(accounts, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class UserRegister(APIView):
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
