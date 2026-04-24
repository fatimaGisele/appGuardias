from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GrupoEscalamientoView

router = DefaultRouter()
router.register(r'', GrupoEscalamientoView, basename='grupo_escalamiento')

urlpatterns = [
    path('', include(router.urls)),
]