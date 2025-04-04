from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status

from api.serializer import CategorySerializer
from models import *


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response([], status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        pass

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(Category, pk=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = get_object_or_404(Category, pk=pk)
        request_body = request.data
        serializer = self.get_serializer(queryset, request_body)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, pk=None, *args, **kwargs):
        queryset = get_object_or_404(Category, pk=pk)
        serializer = self.get_serializer(queryset)
        queryset.delete()
        return Response(f"Delete successful. {serializer.data}",status=status.HTTP_204_NO_CONTENT)
