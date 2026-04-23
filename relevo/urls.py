from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RelevoView

router = DefaultRouter()
router.register(r'', RelevoView, basename='relevo')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:relevo_id>/aceptar/', RelevoView.aceptar_relevo , name='aceptar-relevo'),
    path('<int:relevo_id>/rechazar/',  RelevoView.rechazar_relevo, name='rechazar-relevo'),
]

