from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from turno.models import Turno
from turno.services import notificar_turno_perdido
from guardiasServer.notificaciones.services import enviar_msj_usuario

def verificar_turnos_perdidos():
    ahora = timezone.now()

    turnos_perdidos = Turno.objects.filter(
        estado = 'programado',
        fecha_inicio__lte = ahora,
    )
    for turno in turnos_perdidos:
        turno.estado = 'perdido'
        turno.save()
        notificar_turno_perdido(turno)

def notificar_inicio_turno(turno_id):
    try:
        turno = Turno.objects.get(idturno=turno_id, estado='programado')
        mensaje = (
            f'*Tu turno está por comenzar*\n'
            f'Turno: {turno.nombre}\n'
            f'Hora de inicio: {turno.fecha_inicio.strftime("%d/%m/%Y %H:%M")}\n'
            f'Por favor presentate a tiempo.'
        )
        enviar_msj_usuario(turno.usuario_asignado, mensaje)
    except Turno.DoesNotExist:
        pass 


def notificar_recordatorio_turno(turno_id):
    try:
        turno = Turno.objects.get(idturno=turno_id, estado='programado')
        mensaje = (
            f'*Tu turno comienza en 30 minutos*\n'
            f'Turno: {turno.nombre}\n'
            f'Hora de inicio: {turno.fecha_inicio.strftime("%d/%m/%Y %H:%M")}'
        )
        enviar_msj_usuario(turno.usuario_asignado, mensaje=mensaje)
    except Turno.DoesNotExist:
        pass

scheduler = None
def iniciar_scheduler():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    scheduler.add_job(
        verificar_turnos_perdidos,
        trigger='interval',
        minutes=5,          
        id='verificar_turnos',
        replace_existing=True
    )

    scheduler.start()

def programar_notificaciones_turno(turno):
    if scheduler is None or not scheduler.running: #Se llama al crear un turno para programar las notificaciones
        return
    
    #notificar media hora antes del inico del turnillo
    media_hora_antes = turno.fecha_inicio - timezone.timedelta(minutes=30)
    if media_hora_antes > timezone.now():
        scheduler.add_job(
            notificar_recordatorio_turno,
            trigger = 'date',
            run_date = media_hora_antes,
            args = [turno.idturno],
            id = f'RECORDATORIO DE TURNO {turno.idturno}',
            replace_existing = True
        )

    #notificar al momento de inicio del turo
    if turno.fecha_inicio > timezone.now():
        scheduler.add_job(
           notificar_inicio_turno,
           trigger = 'date',
           run_date = turno.fecha_inicio,
           args = [turno.idturno],
           id= f'inicio de turno {turno.idturno} ',
           replace_existing = True
        )
        