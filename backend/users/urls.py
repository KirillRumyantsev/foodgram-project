from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', CustomUserViewSet, basename='users')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
