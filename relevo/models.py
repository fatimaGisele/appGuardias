from django.db import models
from turno.models import Turno
from usuario.models import Usuario

# Create your models here.
class Relevo(models.Model):
    idrelevo = models.AutoField(primary_key=True)
    turno_origen = models.ForeignKey(
        Turno,
        on_delete= models.DO_NOTHING,
        db_column= 'turno_origen',
        related_name='relevos_como_origen'
    )    
    turno_destino = models.ForeignKey(
        Turno,
        on_delete= models.DO_NOTHING,
        db_column= 'turno_destino',
        related_name='relevos_como_destino'
    )    
    usuario_origen = models.ForeignKey(
        Usuario,
        on_delete= models.DO_NOTHING,
        db_column= 'usuario_idusuario',
        related_name='usuario_que_asigna'
    )    
    usuario_destino= models.ForeignKey(
        Usuario,
        on_delete= models.DO_NOTHING,
        db_column= 'usuario_relevo',
        related_name='usuario_que_toma_turno'
    )    
    motivo = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)
    notas = models.CharField(max_length=250)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(auto_now=True)
    fecha_completado =models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'relevo'