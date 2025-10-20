from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from .serializers import TurnoSerializer, TurnoCreateSerializer, TurnoListSerializer
from .models import Turno
# Create your views here.
class TurnoView(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    serializer_class = TurnoSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TurnoListSerializer
        elif self.action == 'create':
            return TurnoCreateSerializer
        return TurnoSerializer
    
    #'POST'
    def create(request):
        serializer = TurnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
  #list turnos activos
    def list(self, request): 
        turnos = self.queryset.all()
        estado = request.query_params.get('estado', None)
        usuario = request.query_params.get('usuario', None)
        
        if estado:
            turnos = turnos.filter(estado=estado)
        if usuario:
            usuario = turnos.filter(usuario_idusuario=usuario)

        serializer = self.get_serializer(turnos, many=True)
        return Response(serializer.data)
    
   #list turnos activos del dia
    def activos_hoy(self, request):
        hoy = datetime.now().date()
        turnos = self.queryset.filter(
            fecha_inicio=hoy,
            estado='activo'
        )
        serializer = self.get_serializer(turnos, many=True)
        return Response(serializer.data)


### REVISAAAAAAR AHHHHHH
    #TURNO PERDIDO y creacion de una incidencia
    def marcar_perdido(self, request, pk=None):
            turno = get_object_or_404(Turno, pk=pk)
            turno.estado = 'activo' #EL EStado del turno es activo pero el user no lo ha tomaod
            turno.save() #ha pasado mas tiemppo del debido, cuendo este tiempo transcurre se crea 
            #la incidencia, solo despues de cierto tiempo            
            from incidencia.models import Incidencia
            incidencia = Incidencia.objects.create(
                turno_idturno=turno,
                titulo=f'Turno perdido: {turno.nombre}',
                descripcion='El turno no fue tomado por el usuario asignado',
                gravedad='alta',
                estado='abierta'
            )
            
            return Response({
                'mensaje': 'Turno marcado como perdido',
                'turno': TurnoSerializer(turno).data,
                'incidencia_id': incidencia.idincidencia
            })
        
