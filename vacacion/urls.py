from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacacionView

router = DefaultRouter()
router.register(r'', VacacionView, basename='vacacion')

urlpatterns = [
    path('', include(router.urls)),
]