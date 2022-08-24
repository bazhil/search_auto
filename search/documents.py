# coding: utf-8
from django_elasticsearch_dsl import fields, Document
from django_elasticsearch_dsl.registries import registry
from endpoint.models import Categories, Venicle
from elasticsearch_dsl.connections import connections


# TODO: проверить методы сделанные по аналогии: https://django.fun/tutorials/django-rest-framework-i-elasticsearch/
# TODO: или попробовать это: https://tamerlan.dev/how-to-integrate-elasticsearch-with-drf/

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

@registry.register_document
class CategoryDocument(Document):
    id = fields.IntegerField()

    class Index:
        name = 'categories'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Categories
        fields = [
            'category',
            'description',
        ]


@registry.register_document
class VenicleDocument(Document):
    categories = fields.ObjectField(properties={
        'category': fields.TextField(),
        'description': fields.TextField(),
    })
    # category = fields.TextField()

    class Index:
        name = 'venicles'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Venicle
        fields = [
            'mark',
            'model',
            'issue_year',
        ]
        related_models = [Categories, ]
