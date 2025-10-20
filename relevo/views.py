from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import RelevoCreateSerializer, RelevoSerializer
from .models import Relevo

# Create your views here.
class RelevoView(viewsets.ModelViewSet):
    queryset = Relevo.objects.all()
    serializer_class = RelevoSerializer

    def get_serializer_class(self):
        if self.action =='create':
            return RelevoCreateSerializer
        return RelevoCreateSerializer
    
    #aceptar un relevo
    def aceptar_relevo(self, request, pk=None):
        relevo = get_object_or_404(relevo, pk=pk)
        if relevo.estado != 'solicitado':
            return Response(
                {'error': 'Solo se pueden aceptar relevos en estado solicitado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        relevo.estado = 'aceptado'
        relevo.fecha_respuesta = datetime.now()
        relevo.save()
        serializer = self.get_serializer(relevo)
        return Response(serializer.data)
    
    # Obtener unn lista derelevos pendientes
    def relevos_pendientes(self, request):
        pendientes = self.queryset.filter(estado='solicitado')
        serializer = self.get_serializer(pendientes, many=True)
        return Response(serializer.data)
    