from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView

from .permissions import IsAuthorOrReadOnly

from .models import Label, Note
from .serializers import NoteSerializer, LabelSerializer


class Notes(APIView):
    
    def get(self, request):
        notes_list = Note.objects.filter(author__id=request.user.id).order_by(('-created'))
        serializer = NoteSerializer(notes_list, many=True)
        return Response(serializer.data)

    
    def post(self, request):
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response({'created': True, 'note': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'created': False, 'error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)


class NoteDetail(APIView):
    permission_classes = [IsAuthorOrReadOnly]

    def get(self,request, pk):
        try:
            note = Note.objects.get(id=pk, author__id=request.user.id) # make sure only owner can view note
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            note = Note.objects.get(id=pk)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = NoteSerializer(note,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'updated': True, 'note': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'updated': False, 'error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def delete(self, request, pk):
        try:
            note = Note.objects.get(id=pk)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response({'deleted': True, 'msg': f'{note.title} was deleted.'}, status=status.HTTP_204_NO_CONTENT)



class Labels(APIView):

    def get(self, request):
        label_list = Label.objects.filter(author__id=request.user.id)
        serializer = LabelSerializer(label_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LabelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'created': True, 'label': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'created': False, 'error': serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)

class LabelDetail(APIView):

    def get(self, request, pk=None):
        try:
            label = Label.objects.get(id=pk, author__id=request.user.id)
        except Label.DoesNotExist:
            return Response({'error': 'Label not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LabelSerializer(label)
        return Response(serializer.data)


    def put(self, request, pk=None):
        try:
            label = Label.objects.get(id=pk)
        except Label.DoesNotExist:
            return Response({'error': 'Label not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LabelSerializer(label, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response({'updated': False, 'label': serializer.errors}, status=status.HTTP_404_NOT_FOUND)
        return Response({'updated': True, 'label': serializer.data}, status=status.HTTP_201_CREATED)
        

    def delete(self, request, pk=None):
        try:
            label = Label.objects.get(id=pk)
        except Label.DoesNotExist:
            return Response({'error': 'Label not found'}, status=status.HTTP_404_NOT_FOUND)
        label.delete()
        return Response({'deleted':True, 'msg': f'{label.name} was deleted'}, status=status.HTTP_204_NO_CONTENT)
