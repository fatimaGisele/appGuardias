from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RolView

router =  DefaultRouter()
router.register(r'', RolView)

urlpatterns = [
    path('', include(router.urls)),
]