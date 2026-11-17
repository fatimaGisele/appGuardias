from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from calendario.services import sincronizar_evento_turno
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import RelevoCreateSerializer, RelevoSerializer
from .models import Relevo
from guardiasServer.notificaciones.services import enviar_msj_usuario, enviar_email
from usuario_grupo.models import Usuario_grupo
from relevo.models import Relevo
from guardiasServer.permissions import SoloJefeEscribe, es_jefe


# Create your views here.
class RelevoView(viewsets.ModelViewSet):
    queryset = Relevo.objects.all()
    serializer_class = RelevoSerializer
    permission_classes = [SoloJefeEscribe]

    def get_queryset(self):
        relevos = Relevo.objects.all()
        if es_jefe(self.request.user):
            return relevos
        return relevos.filter(
            Q(usuario_destino=self.request.user)| Q(usuario_origen_solicitante=self.request.user)
        )

    def get_serializer_class(self):
        if self.action == 'create':
            return RelevoCreateSerializer
        return RelevoSerializer

    
    
def notificar_jefes_relevo(turno, mensaje, mensaje_email, asunto):
    #"""Notifica a todos los jefes del grupo de escalamiento del turno"""
    if not turno.grupo_escalamiento:
        return
    jefes = Usuario_grupo.objects.filter(
        grupo_escalamiento=turno.grupo_escalamiento,
        activo=True
    ).select_related('usuario').order_by('prioridad')
    for usuario_grupo in jefes:
        enviar_msj_usuario(usuario_grupo.usuario, mensaje)
        enviar_email(usuario_grupo.usuario,asunto,mensaje_email)

def _obtener_relevo_pendiente(request, relevo_id):   
    relevo = get_object_or_404(
        Relevo.objects.select_for_update().select_related('turno_origen'),
        idrelevo=relevo_id,
        usuario_destino=request.user,
    )
    if relevo.estado != 'solicitado':
        return None, Response({'error': 'Este relevo ya fue respondido'},
                              status=status.HTTP_400_BAD_REQUEST)
    if relevo.turno_origen.estado != 'perdido':
        return None, Response({'error': 'El turno ya no necesita relevo'},
                              status=status.HTTP_400_BAD_REQUEST)
    return relevo, None

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def aceptar_relevo(request, relevo_id):
    with transaction.atomic():
        relevo, error = _obtener_relevo_pendiente(request, relevo_id)
        if error:
            return error

        turno = relevo.turno_origen
        turno.usuario_asignado = request.user
        turno.estado = 'activo'
        turno.save()

        relevo.estado = 'aceptado'
        relevo.fecha_respuesta = timezone.now()
        relevo.save()
        sincronizar_evento_turno(turno) #el event de google pasa a tener como inv al relevo y pasa mail

        mensaje = (
        f'*Relevo aceptado*\n'
        f'El guardia {request.user.nombre} {request.user.apellido} '
        f'aceptó cubrir el turno *{turno.nombre}*.\n'
        f'Fecha: {turno.fecha_inicio.strftime("%d/%m/%Y %H:%M")}'
        )
        mensaje_email = (
        f'Relevo aceptado: {turno.nombre}\n\n'
        f'El guardia {request.user.nombre} {request.user.apellido} '
        f'aceptó cubrir el turno {turno.nombre}.\n'
        f'Fecha: {turno.fecha_inicio.strftime("%d/%m/%Y %H:%M")}'
        )
        notificar_jefes_relevo(turno, mensaje, mensaje_email, 'relevo aceptado')
        return Response({'mensaje': 'Turno aceptado'}, status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rechazar_relevo(request, relevo_id):
    motivo = request.data.get('motivo') or 'Sin motivo especificado'

    with transaction.atomic():
        relevo, error = _obtener_relevo_pendiente(request, relevo_id)
        if error:
            return error

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
        mensaje_email = (
            f'Relevo rechazado: {turno.nombre}\n\n'
            f'El guardia {request.user.nombre} {request.user.apellido} '
            f'rechazó cubrir el turno {turno.nombre}.\n'
            f'Motivo: {motivo}'
        )
        notificar_jefes_relevo(turno, mensaje, mensaje_email, 'relevo rechazado')
        return Response({'mensaje': 'Turno rechazado'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def relevos_pendientes(request):
    relevos = Relevo.objects.filter(
        usuario_destino = request.user,
        estado = 'solicitado',
        turno_origen__estado='perdido',
    ).select_related('turno_origen').order_by('turno_origen__fecha_inicio')
    data = []
    for r in relevos:
        data.append({
            'idrelevo': r.idrelevo,
            'idturno': r.turno_origen.idturno,
            'turno_nombre': r.turno_origen.nombre,
            'fecha_inicio': r.turno_origen.fecha_inicio,
            'fecha_fin': r.turno_origen.fecha_fin,
            'estado': r.estado,
        })
    return Response(data)


    