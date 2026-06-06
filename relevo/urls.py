from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RelevoView, aceptar_relevo, rechazar_relevo

router = DefaultRouter()
router.register(r'', RelevoView, basename='relevo')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:relevo_id>/aceptar/', aceptar_relevo , name='aceptar-relevo'),
    path('<int:relevo_id>/rechazar/', rechazar_relevo, name='rechazar-relevo'),
]

