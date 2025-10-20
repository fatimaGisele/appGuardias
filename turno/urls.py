from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TurnoView

router = DefaultRouter()
router.register(r'', TurnoView, basename='turno')

urlpatterns = [
    path('', include(router.urls)),
]