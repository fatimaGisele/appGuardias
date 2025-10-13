from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from .serializers import IncidenciaCreateSerializer, IncidenciaSerializer
from .models import Incidencia

class IncidenciaView(viewsets.ModelViewSet):
    queryset = Incidencia.objects.all()
    serializer_class = IncidenciaSerializer

    def get_serializer_class(self):
        if self.action =='create':
            return IncidenciaCreateSerializer
        return IncidenciaSerializer
    
    