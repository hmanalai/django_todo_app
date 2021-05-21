from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework import status 

from .models import Todo
from .serializers import TodoSerializer

class TodoList(APIView):
    def post(self, request, format=None):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        tasks = Todo.objects.all()
        serializer = TodoSerializer(tasks, many=True)
        return Response(serializer.data)


class TodoDetail(APIView):
    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TodoSerializer(task)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TodoSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

