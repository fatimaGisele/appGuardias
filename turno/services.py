from incidencia.models import Incidencia
from escalamiento.models import Escalamiento
from usuario_grupo.models import Usuario_grupo
from relevo.models import Relevo
from guardiasServer.notificaciones.services import enviar_whatsapp, enviar_msj_relevo
from django.utils import timezone

def notificar_turno_perdido(turno):
    #se crea la incidencia
    incidencia = Incidencia.objects.create(
        turno = turno,
        titulo = f"turno perdido: {turno.nombre}",
        descripcion = f"La guardia no fue tomada por: {turno.usuario_asignado}",
        gravedad = 'alta',
        estado = 'abierta',
        fecha_ocurrencia = timezone.now()
    )

    # se busca a los encargados del grupo de escalamiento del turno 
    if not turno.grupo_escalamiento:
        return
    encargados = Usuario_grupo.objects.filter(
        grupo_escalamiento = turno.grupo_escalamiento,
        activo = True
    ).select_related('usuario').order_by('prioridad')

    for usuario_grupo in encargados:
        jefecito = usuario_grupo.usuario

    #se crea el escalamiento ahhhhh!!!
    escalamiento = Escalamiento.objects.create(
        incidencia = incidencia,
        usuario_notificado = jefecito,
        nivel = usuario_grupo.prioridad,
        tipo_notificacion = 'msj whatsapp',
        estado = 'pendiente',
        mensaje_enviado=f'El responsable {turno.usuario_asignado.nombre} no se presentó a su turno {turno.nombre_turno}.',
        fecha_escalamiento = timezone.now() 
    )

    # se envia el msj dd whatsapp

    mensaje = (
        f'*Turno perdido*\n'
        f'Guardia: {turno.usuario_asignado.nombre} {turno.usuario_asignado.apellido}\n'
        f'Turno: {turno.nombre_turno}\n'
        f'Hora inicio: {turno.fecha_inicio.strftime("%d/%m/%Y %H:%M")}\n'
        f'Por favor tome las medidas necesarias.'
    )
    enviado = enviar_whatsapp(jefecito, mensaje, escalamiento)
    escalamiento.estado = 'enviado' if enviado else 'fallido'
    escalamiento.save()
    notificar_relevo(turno)


#se notifica al relevo 
def notificar_relevo(turno):
    relevo = Relevo.objects.filter(
        turno_origen = turno,
        estado = 'solicitado'
    ).select_related('usuario_destino').first()
    if not relevo:
        return
    mensaje = (
        f'*Guardia disponible*\n'
        f'El turno *{turno.nombre}* quedó sin cobertura.\n'
        f'Fecha: {turno.fecha_inicio.strftime("%d/%m/%Y %H:%M")}\n'
        f'Podés aceptar o rechazar el turno desde la app.'
    )
    enviar_msj_relevo(relevo.usuario_destino, mensaje)