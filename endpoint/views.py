from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Auto, Categories
from .serializers import AutoSerializer


# Create your views here.
class AutoAPIList(generics.ListCreateAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    permission_classes = (IsAuthenticated, )


class AutoAPICreate(generics.ListCreateAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    permission_classes = (IsAuthenticated, )


class AutoAPIUpdate(generics.ListCreateAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    permission_classes = (IsAdminUser, )


class AutoAPIDelete(generics.ListCreateAPIView):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    permission_classes = (IsAdminUser, )

# TODO: Добавить view с возможностью искать по БД

# TODO: Добавить view с возможностью загружать и выгружать в csv, xlsx
