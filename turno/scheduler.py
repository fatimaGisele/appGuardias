from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from turno.models import Turno
from turno.services import notificar_turno_perdido

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

def iniciar_scheduler():
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
