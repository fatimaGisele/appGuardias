from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioGrupoView

router = DefaultRouter()
router.register(r'', UsuarioGrupoView, basename='usuario_grupo')

urlpatterns = [
    path('', include(router.urls)),
]