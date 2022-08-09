from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Venicle, Categories
from .serializers import VenicleSerializer


# Create your views here.
class AutoAPIList(generics.ListCreateAPIView):
    queryset = Venicle.objects.all()
    serializer_class = VenicleSerializer
    permission_classes = (IsAuthenticated, )


class AutoAPIUpdate(generics.ListCreateAPIView):
    queryset = Venicle.objects.all()
    serializer_class = VenicleSerializer
    permission_classes = (IsAdminUser, )
    # authentication_classes = (TokenAuthentication, )


class AutoAPIDelete(generics.ListCreateAPIView):
    queryset = Venicle.objects.all()
    serializer_class = VenicleSerializer
    permission_classes = (IsAdminUser, )

# TODO: Добавить view с возможностью искать по БД

# TODO: Добавить view с возможностью загружать и выгружать в csv, xlsx
