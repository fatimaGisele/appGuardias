from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidenciaView

router = DefaultRouter()
router.register(r'', IncidenciaView, basename='incidencia')

urlpatterns = [
    path('', include(router.urls)),
]