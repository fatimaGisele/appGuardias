from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import RelevoCreateSerializer, RelevoSerializer
from .models import Relevo
from guardiasServer.notificaciones.services import enviar_msj_relevo
from usuario_grupo.models import Usuario_grupo

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
        relevo.fecha_respuesta = timezone.now()
        relevo.save()
        serializer = self.get_serializer(relevo)
        return Response(serializer.data)
    
    # Obtener unn lista derelevos pendientes
    def relevos_pendientes(self, request):
        pendientes = self.queryset.filter(estado='solicitado')
        serializer = self.get_serializer(pendientes, many=True)
        return Response(serializer.data)
    
    def notificar_jefes_relevo(turno, mensaje):
    #"""Notifica a todos los jefes del grupo de escalamiento del turno"""
        if not turno.grupo_escalamiento:
            return

        jefes = Usuario_grupo.objects.filter(
            grupo=turno.grupo_escalamiento,
            activo=True
        ).select_related('usuario_creador').order_by('prioridad')

        for usuario_grupo in jefes:
            enviar_msj_relevo(usuario_grupo.usuario, mensaje)

    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def aceptar_relevo(request, relevo_id):
        relevo = get_object_or_404(
            Relevo,
            idrelevo = relevo_id,
            usuario_destino = request.user,
            estado = 'solicitado'
        )

        turno = relevo.turno_origen
        turno.usuario_asignado = request.user
        turno.estado = 'activo'
        turno.save()

        relevo.estado = 'aceptado'
        relevo.fecha_respuesta = timezone.now()
        relevo.save()

        mensaje = (
        f'*Relevo aceptado*\n'
        f'El guardia {request.user.nombre} {request.user.apellido} '
        f'aceptó cubrir el turno *{turno.nombre}*.\n'
        f'Fecha: {turno.fecha_inicio.strftime("%d/%m/%Y %H:%M")}'
        )
        notificar_jefes_relevo(turno, mensaje)

        return Response({'mensaje': 'Turno aceptado'}, status=status.HTTP_200_OK)
    
    @api_view(['POST'])
    @permission_classes([IsAuthenticated])
    def rechazar_relevo(request, relevo_id):
        relevo = get_object_or_404(
            Relevo,
            idrelevo=relevo_id,
            usuario_relevo=request.user,
            estado='solicitado'
        )

        relevo.estado = 'rechazado'
        relevo.fecha_respuesta = timezone.now()
        relevo.notas = request.data.get('motivo', '') 
        relevo.save()
        turno = relevo.turno_origen
        mensaje = (
        f'*Relevo rechazado*\n'
        f'El guardia {request.user.nombre} {request.user.apellido} '
        f'rechazó cubrir el turno *{turno.nombre}*.\n'
        f'Fecha: {turno.fecha_inicio.strftime("%d/%m/%Y %H:%M")}\n'
        f'Motivo: {motivo}'
    )
        notificar_jefes_relevo(turno, mensaje)
        return Response({'mensaje': 'Turno rechazado'}, status=status.HTTP_200_OK)





    