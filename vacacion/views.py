from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import Vacacion
from .serializers import VacacionSerializer, SolicitarVacacionSerializer,dias_vacaciones_segun_antiguedad,dias_usados_en_año
from usuario.models import Usuario


class VacacionView(viewsets.ModelViewSet):
    queryset = Vacacion.objects.all()
    serializer_class = VacacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        rol = user.rol.nombre
        # Lider/encargado ve todas las solicitudes
        if rol in ['lider', 'encargado']:
            return Vacacion.objects.all().order_by('-fecha_solicitud')
        # Guardia/relevo ve solo las suyas
        return Vacacion.objects.filter(
            usuario=user
        ).order_by('-fecha_solicitud')

    
    @action(detail=False, methods=['post'], url_path='solicitar')
    def solicitar(self, request):
        serializer = SolicitarVacacionSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            vacacion = serializer.save()
            return Response(
                VacacionSerializer(vacacion).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=True, methods=['post'], url_path='aprobar')
    def aprobar(self, request, pk=None):
        vacacion = self.get_object()
        if vacacion.estado != 'pendiente':
            return Response(
                {'error': 'Solo se pueden aprobar solicitudes pendientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        vacacion.estado = 'aprobada'
        vacacion.nota_aprobador = request.data.get('nota', '')
        vacacion.fecha_respuesta = timezone.now()
        vacacion.save()
        return Response(VacacionSerializer(vacacion).data)

   
    @action(detail=True, methods=['post'], url_path='rechazar')
    def rechazar(self, request, pk=None):
        vacacion = self.get_object()
        if vacacion.estado != 'pendiente':
            return Response(
                {'error': 'Solo se pueden rechazar solicitudes pendientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        vacacion.estado = 'rechazada'
        vacacion.nota_aprobador = request.data.get('nota', '')
        vacacion.fecha_respuesta = timezone.now()
        vacacion.save()
        return Response(VacacionSerializer(vacacion).data)

    
    @action(detail=False, methods=['get'], url_path='mis-dias') 
    def mis_dias(self, request):
        usuario = request.user
        año = timezone.now().year
        disponibles = dias_vacaciones_segun_antiguedad(usuario.fecha_ingreso)
        usados = dias_usados_en_año(usuario, año)
        return Response({
            'año': año,
            'disponibles': disponibles,
            'usados': usados,
            'restantes': disponibles - usados,
        })

    # vacaciones pendientes para lider/encargado
    @action(detail=False, methods=['get'], url_path='pendientes')
    def pendientes(self, request):
        vacaciones = Vacacion.objects.filter(
            aprobador=request.user,
            estado='pendiente'
        ).select_related('usuario').order_by('fecha_inicio')
        return Response(VacacionSerializer(vacaciones, many=True).data)
