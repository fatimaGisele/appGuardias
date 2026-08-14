from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioGrupoView,mi_equipo

router = DefaultRouter()
router.register(r'', UsuarioGrupoView, basename='usuario_grupo')

urlpatterns = [
    path('mi_equipo/', mi_equipo, name='mi_equipo'),
    path('', include(router.urls)),
]