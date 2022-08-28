import uuid

from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Venicle, Categories, ExcelFileUpload
from .serializers import VenicleSerializer

from django.http.response import JsonResponse, HttpResponse, FileResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from elasticsearch import Elasticsearch, RequestsHttpConnection

from rest_framework_elasticsearch import es_views, es_pagination, es_filters
from .search_indexes import VenicleIndex
import pandas as pd

from search_auto.settings import BASE_DIR


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


class ExportImportExcel(APIView):

    def get(self, request):
        venicles = Venicle.objects.all()
        serializer = VenicleSerializer(venicles, many=True)
        df = pd.DataFrame(serializer.data)
        file_path = f'static/excel/{uuid.uuid4()}.xlsx'
        df.to_excel(file_path, encoding="UTF-8", index=False)
        response = FileResponse(open(file_path, 'rb'))

        return response

    def post(self, request):
        # TODO: разобраться, почему не грузится Excel
        excel_upload_obj = ExcelFileUpload.objects.create(excel_file_ulpoad=request.FILES['files'])
        df = pd.read_csv(f'{BASE_DIR}/static/{excel_upload_obj.excel_file_ulpoad}')
        for venicle in (df.values.to_list()):
            try:
                Venicle.objects.create(
                    mark=venicle[0],
                    model=venicle[1],
                    category=venicle[2],
                    reg_number=venicle[3],
                    issue_year=venicle[4],
                    vin=venicle[5],
                    sts_number=venicle[6],
                    sts_date=venicle[7],
                    description=venicle[8],
                )
            except Exception as ex:
                print(f'При загрузке данных из excel-файла произошла ошибка: {ex}')

        return Response({'status': 200})
