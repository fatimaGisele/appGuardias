from datetime import datetime
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
    
    #filtra y lista por el estado y la gravedad
    def list(self, request):
        incidencia = self.queryset.all()
        gravedad = request.query_params.get('gravedad', None)
        estado = request.query_params.get('estado', None)
        if estado:
            incidencia = incidencia.filter(estado=estado)
        if gravedad:
            incidencia = incidencia.filter(gravedad=gravedad)

        serializer = self.get_serializer(incidencia, many =True)
        return Response(serializer.data)
    
    #VA A marcar una incidencia como resuelta
    def resueltas(self, request, pk=None):
        incidencia = get_object_or_404(Incidencia, pk=pk)
        incidencia.estado = 'resuelta'
        incidencia.fecha_resolucion = datetime.now()
        incidencia.save()
        
        serializer = self.get_serializer(incidencia)
        return Response(serializer.data)
    
    # Filtra para obtener incidencias críticas abiertas
    def incidencias_criticas_abiertas(self, request):
        criticas = self.queryset.filter(
            gravedad='critica',
            estado='abierta'
        )
        serializer = self.get_serializer(criticas, many=True)
        return Response(serializer.data)
