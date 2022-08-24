# coding: utf-8
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from endpoint.views import AutoAPIList, AutoAPIUpdate
from endpoint.views import add_venicle, update_venicle, delete_venicle
from search.views import PaginatedElasticSearchAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('endpoint.urls')),
    path('api/user-auth/', include('rest_framework.urls')),
    path('api/auto/list', AutoAPIList.as_view()),
    path('api/auto/<int:pk>', AutoAPIUpdate.as_view()),
    # path('api/auto/delete/<int:pk>', AutoAPIDelete.as_view()),

    path('api/auto/create', add_venicle, name='add-venicle'),
    # path('api/auto/list', view_venicles, name='view_venicles'),
    path('api/auto/update/<int:pk>', update_venicle, name='update-venicle'),
    path('api/auto/delete/<int:pk>', delete_venicle, name='delete-venicle'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/auto/search/<str:query>/', PaginatedElasticSearchAPIView.as_view())
]
