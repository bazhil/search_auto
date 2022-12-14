import uuid

from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Venicle
from .serializers import VenicleSerializer

from django.http.response import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from elasticsearch import Elasticsearch, RequestsHttpConnection
import pandas as pd


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


@api_view(['GET'])
def view_venicle(request, pk):
    item = Venicle.objects.get(pk=pk)
    data = VenicleSerializer(instance=item)
    if data:
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
        df = pd.read_excel(request.FILES['files'])
        for venicle in df.values:
            try:
                data = VenicleSerializer(data={
                    # 'id': venicle[0],
                    'mark': venicle[1],
                    'model': venicle[2],
                    'reg_number': venicle[3],
                    'issue_year': venicle[4],
                    'vin': venicle[5],
                    'sts_number': venicle[6],
                    'sts_date': venicle[7],
                    'description': venicle[8],
                    'category': venicle[9]
                })
                if data.is_valid():
                    data.save()

            except Exception as ex:
                print(f'?????? ???????????????? ???????????? ???? excel-?????????? ?????????????????? ????????????: {ex}')

        return Response({'status': 200})


class ExportImportCSV(APIView):

    def get(self, request):
        venicles = Venicle.objects.all()
        serializer = VenicleSerializer(venicles, many=True)
        df = pd.DataFrame(serializer.data)
        file_path = f'static/csv/{uuid.uuid4()}.csv'
        df.to_csv(file_path, encoding="UTF-8", index=False)
        response = FileResponse(open(file_path, 'rb'))

        return response

    def post(self, request):
        df = pd.read_csv(request.FILES['files'])
        for venicle in df.values:
            try:
                data = VenicleSerializer(data={
                    # 'id': venicle[0],
                    'mark': venicle[1],
                    'model': venicle[2],
                    'reg_number': venicle[3],
                    'issue_year': venicle[4],
                    'vin': venicle[5],
                    'sts_number': venicle[6],
                    'sts_date': venicle[7],
                    'description': venicle[8],
                    'category': venicle[9]
                })
                if data.is_valid():
                    data.save()
            except Exception as ex:
                print(f'?????? ???????????????? ???????????? ???? csv-?????????? ?????????????????? ????????????: {ex}')

        return Response({'status': 200})
