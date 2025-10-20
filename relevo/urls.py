from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RelevoView

router = DefaultRouter()
router.register(r'', RelevoView, basename='relevo')

urlpatterns = [
    path('', include(router.urls)),
]