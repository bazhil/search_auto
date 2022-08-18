from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Venicle, Categories
from .serializers import VenicleSerializer

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from elasticsearch import Elasticsearch, RequestsHttpConnection

from rest_framework_elasticsearch import es_views, es_pagination, es_filters
from .search_indexes import VenicleIndex


es_client = Elasticsearch(
    hosts=['elasticsearch:9200/'],
    connection_class=RequestsHttpConnection
)

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


# class AutoAPIDelete(generics.ListCreateAPIView):
#     queryset = Venicle.objects.all()
#     serializer_class = VenicleSerializer
#     permission_classes = (IsAdminUser, )


# TODO: Добавить view с возможностью загружать и выгружать в csv, xlsx

@api_view(['GET'])
def view_venicles(request):
    """
    TODO: не работает, исследовать и починить!
    """

    # checking for the parameters from the URL
    if request.query_params:
        items = Venicle.objects.filter(**request.query_param.dict())
    else:
        items = Venicle.objects.all()

    # if there is something in items else raise error
    if items:
        data = VenicleSerializer(items)

        return Response(data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def add_venicle(request):
    venicle = VenicleSerializer(data=request.data)

    # validating for already existing data
    if Venicle.objects.filter(**request.data).exists():
        raise VenicleSerializer.ValidationError('This data already exists')

    if venicle.is_valid():
        venicle.save()
        return Response(venicle.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_venicle(request, pk):
    item = Venicle.objects.get(pk=pk)
    data = VenicleSerializer(instance=item, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_venicle(request, pk):
    item = get_object_or_404(Venicle, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


class VenicleView(es_views.ListElasticAPIView):
    es_client = es_client
    es_model = VenicleIndex
    es_pagination_class = es_pagination.ElasticLimitOffsetPagination

    es_filter_backends = (
        es_filters.ElasticFieldsFilter,
        es_filters.ElasticSearchFilter,
        es_filters.ElasticOrderingFilter,
    )
    es_ordering_fields = (
        ("category", "category")
    )
    es_filter_fields = (
        es_filters.ESFieldFilter('mark', 'mark'),
        es_filters.ESFieldFilter('nodel', 'model')
    )
    es_search_fields = (
        'model',
        'model',
    )
