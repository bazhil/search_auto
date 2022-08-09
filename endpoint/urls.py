# coding: utf-8
from rest_framework import routers
from .api import VenicleViewSet, CategoriesViewSet

router = routers.DefaultRouter()
router.register('api/auto', VenicleViewSet, 'auto')
router.register('api/categories', CategoriesViewSet, 'categories')

urlpatterns = router.urls
