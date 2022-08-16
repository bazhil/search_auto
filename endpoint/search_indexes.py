# coding: utf-8
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, GeoPoint

class VenicleIndex(Document):
    pk = Integer()
    mark = Text(fields={'raw': Keyword})
    model = Text(fields={'raw': Keyword})

    class Index:
        name = 'venicle'


VenicleIndex.init()
