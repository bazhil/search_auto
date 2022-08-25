# coding: utf-8

import abc

from django.http import HttpResponse
from elasticsearch_dsl import Q
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView

from endpoint.serializers import VenicleSerializer
from search.documents import VenicleDocument


# TODO: попробуй https://github.com/veryacademy/django-ecommerce-project-v2/blob/main/part-6/ecommerce/search/views.py

class PaginatedElasticSearchAPIView(APIView, LimitOffsetPagination):
    serializer_class = VenicleSerializer
    document_class = VenicleDocument

    @abc.abstractmethod
    def generate_q_expression(self, query):
        """This method should be overridden
        and return a Q() expression."""
    #     TODO: https://tamerlan.dev/how-to-integrate-elasticsearch-with-drf/
    #      + https://django.fun/tutorials/django-rest-framework-i-elasticsearch/
    #      + https://github.com/veryacademy/django-ecommerce-project-v2/blob/main/part-6/ecommerce/search/views.py
        q = Q(
            'multi_match',
            query=query,
            fields=[
                'mark',
                # 'model',
                # 'issue_year',
            ])

        return q


    def get(self, request, query):
        try:
            q = self.generate_q_expression(query)
            search = self.document_class.search().query(q)
            response = search.execute()

            print(f'response = {response}')
            print(f'Found {response.hits.total.value} hit(s) for query: "{query}"')

            results = self.paginate_queryset(response, request, view=self)
            serializer = self.serializer_class(results, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=500)
