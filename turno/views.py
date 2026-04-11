from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets
from .serializers import TurnoSerializer, TurnoCreateSerializer, TurnoListSerializer
from .models import Turno
from incidencia.models import Incidencia
from .services import notificar_turno_perdido
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
    def create(self, request):
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
            turnos = turnos.filter(usuario_asignado=usuario)

        serializer = self.get_serializer(turnos, many=True)
        return Response(serializer.data)
    
   #list turnos activos del dia
    def activos_hoy(self, request):
        hoy = timezone.now().date()
        turnos = self.queryset.filter(
            fecha_inicio__date=hoy,
            estado='activo'
        )
        serializer = self.get_serializer(turnos, many=True)
        return Response(serializer.data)


### REVISAAAAAAR AHHHHHH
    #TURNO PERDIDO y creacion de una incidencia
    def marcar_perdido(self, request, pk=None):
        turno = get_object_or_404(Turno, pk=pk)

        if turno.estado != 'programado':
            return Response(
                {'error': 'Solo se pueden marcar como perdidos turnos programados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        turno.estado = 'perdido'
        turno.save() 

        incidencia = Incidencia.objects.create(
            turno=turno,
            titulo=f'Turno perdido: {turno.nombre}',
            descripcion='El turno no fue tomado por el usuario asignado',
            gravedad='alta',
            estado='abierta'
        )

        notificar_turno_perdido(turno)
            
        return Response({
            'mensaje': 'Turno marcado como perdido',
            'turno': TurnoSerializer(turno).data,
            'incidencia_id': incidencia.idincidencia
        })
    
    
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def checkin(request, turno_id):
        try:
            turno = Turno.objects.get(
                idturno=turno_id,
                usuario_asignado=request.user,  
                estado='programado'
            )
        except Turno.DoesNotExist:
            return Response({'error': 'Turno no encontrado o ya procesado'}, status=status.HTTP_404_NOT_FOUND)

        turno.estado = 'activo'
        turno.save()

        return Response({'mensaje': 'Check-in realizado correctamente'}, status=status.HTTP_200_OK)
        
