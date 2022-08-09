# coding: utf-8

from rest_framework import serializers
from .models import Venicle, Categories


class VenicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venicle
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'