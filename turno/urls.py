from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TurnoView, checkin

router = DefaultRouter()
router.register(r'', TurnoView, basename='turno')

urlpatterns = [
    path('', include(router.urls)),
    path('checkin/<int:turno_id>/', checkin, name='checkin'),
]