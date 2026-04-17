from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RelevoView
from . import views

router = DefaultRouter()
router.register(r'', RelevoView, basename='relevo')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:relevo_id>/aceptar/', views.aceptar_relevo, name='aceptar-relevo'),
    path('<int:relevo_id>/rechazar/', views.rechazar_relevo, name='rechazar-relevo'),
]

