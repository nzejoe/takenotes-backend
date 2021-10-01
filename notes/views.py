from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Label, Note


class Notes(APIView):
    pass

