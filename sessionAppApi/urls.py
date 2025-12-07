
from rest_framework import routers
from django.urls import path, include
from .views import SessionViewSet

router = routers.DefaultRouter()
router.register('session', SessionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
