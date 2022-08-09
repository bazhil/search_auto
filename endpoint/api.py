# coding: utf-8
from .models import Venicle, Categories
from rest_framework import viewsets, permissions
from .serializers import VenicleSerializer, CategoriesSerializer


class VenicleViewSet(viewsets.ModelViewSet):
    queryset = Venicle.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = VenicleSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CategoriesSerializer
