# coding: utf-8

from rest_framework import serializers
from rest_framework_elasticsearch.es_serializer import ElasticModelSerializer

from .models import Venicle, Categories
from .search_indexes import VenicleIndex


class VenicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venicle
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'


class ElasticVenicleSerializer(ElasticModelSerializer):
    class Meta:
        model = Venicle
        es_model = VenicleIndex
        fields = ('pk', 'title', 'created_at', 'tags', 'body', 'is_published')