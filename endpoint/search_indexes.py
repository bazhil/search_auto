# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

from elasticsearch_dsl import (
    Document,
    Date,
    Keyword,
    Text,
    Boolean,
    Integer
)


class VenicleIndex(Document):
    """
    VenicleIndex.init(using=es_client)
    """
    pk = Integer()
    mark = Text(fields={'raw': Keyword()})
    model = Text(fields={'raw': Keyword()})
    category = Text(fields={'raw': Keyword()})

    class Meta:
        index = 'venicle'