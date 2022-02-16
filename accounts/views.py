import json

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from rest_framework import permissions, status, serializers, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .models import Account
from .serializers import (AccountsSerializer, PasswordResetForm,
                          UserRegistrationSerializer)

# call the signal
from . import signals


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
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class UserAuth(ObtainAuthToken):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        data = {}
        user = None

        if serializer.is_valid():            
            user = serializer.validated_data['user']

            # get token or create one if none exists
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        else:
            if user is None:
                raise serializers.ValidationError(
                    {'error': 'true', 'message': 'User or password is invalid!'}
                )
            data = serializer.errors
        return Response(data)


class UserLogout(APIView):

    def post(self, request):

        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'logged out': "logout was successful!"}, status=status.HTTP_200_OK)


class UserRegister(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})

        data = {}

        if serializer.is_valid(raise_exception=True):
            account = serializer.save()

            # get user token key
            token = Token.objects.get(user=account).key

            data['token'] = token
            data['username'] = account.username
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
        else:
            data = serializer.errors
        return Response(data)  # populate data with serializers errors


class PasswordReset(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):

        serializer = PasswordResetForm(
            data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            user = Account.objects.get(email=email)
            current_site = request.META.get('HTTP_ORIGIN')
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_url = f'{current_site}/account/password_reset_confirm/{uid}/{token}'
            context = {
                'username': user.username,
                'domain': confirm_url
            }
            # email message
            mail_subject = "Password reset"
            message = render_to_string(
                'account/password_reset_email.html', context)
            email_message = EmailMessage(mail_subject, message, to=[email, ])
            email_message.send()

            return Response({'email': email})
        else:
            return Response(serializer.errors)


class PasswordResetConfirm(APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, reqeust, uidb64, token):

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = Account.objects.get(pk=uid)
        except Account.DoesNotExist:
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            data = json.dumps({'success': True, 'user_id': uid})
        else:
            data = json.dumps({'success': False})

        return Response(data)


class PasswordResetComplete(APIView):
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, pk):
        try:
            user = Account.objects.get(pk=pk)
        except (Account.DoesNotExist, ValueError, TypeError):
            user = None

        if user is not None:
            data = json.dumps({'validAccount': True})
            statusRes = status.HTTP_200_OK
        else:
            data = json.dumps({'validAccount': False})
            statusRes = status.HTTP_404_NOT_FOUND

        return Response(data, status=statusRes)

    def put(slef, request, pk):

        try:
            user = Account.objects.get(pk=pk)
        except (Account.DoesNotExist, ValueError, TypeError):
            user = None

        if user is not None:
            password = request.data['password']
            user.set_password(password)
            user.save()

            data = json.dumps({'success': True})
            statusRes = status.HTTP_200_OK
        else:
            data = json.dumps({'success': False})
            statusRes = status.HTTP_400_BAD_REQUEST

        return Response(data, status=statusRes)


class PasswordChange(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        user = request.user
        current_password = request.data['currentPassword']
        new_password = request.data['password']

        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
            data = json.dumps(
                {'error': False, 'message': 'Password accepted!'})
        else:
            data = json.dumps(
                {'error': True, 'message': 'Current password is incorrect!'})
        return Response(data)
