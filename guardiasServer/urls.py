from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuario.urls')),
    path('api/turnos/', include('turno.urls')),
    path('api/incidencias/', include('incidencia.urls')),
    path('api/relevos/', include('relevo.urls')),     
]
