from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CalendarioView, google_oauth_callback

router = DefaultRouter()
router.register(r'', CalendarioView, basename='calendario')

urlpatterns = [
    path('', include(router.urls)),
    path('oauth/callback/', google_oauth_callback, name='google-oauth-callback'),
]