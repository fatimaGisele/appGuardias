from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserView, estadisticas_equipo


router = DefaultRouter()
router.register(r'', UserView, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    path('/estadisticas', estadisticas_equipo, name='estadisticas-equipo')
]