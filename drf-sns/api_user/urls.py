from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

app_name = 'user'

urlpatterns = [
    path('', include(router.urls)),
]