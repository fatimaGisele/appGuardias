from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView


router = DefaultRouter()
router.register(r'', UserView, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
]