from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuario.urls')),
    path('turnos/', include('turno.urls')),
    path('incidencias/', include('incidencia.urls')),
    path('relevos/', include('relevo.urls')),   
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
]
