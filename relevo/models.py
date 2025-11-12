from django.db import models
from turno.models import Turno
from usuario.models import Usuario

# Create your models here.
class Relevo(models.Model):
    idrelevo = models.AutoField(primary_key=True)
    turno_origen = models.ForeignKey(
        Turno,
        on_delete= models.CASCADE,
        related_name='relevo_origen'
    )    
    turno_destino = models.ForeignKey(
        Turno,
        on_delete= models.CASCADE,
        related_name='relevos_destino'
    )    
    usuario_origen_solicitante = models.ForeignKey(
        Usuario,
        on_delete= models.CASCADE,
        related_name='usuario_que_asigna'
    )    
    usuario_destino= models.ForeignKey(
        Usuario,
        on_delete= models.CASCADE,
        related_name='usuario_toma_turno'
    )    
    motivo = models.CharField(max_length=45)
    estado = models.CharField(
        max_length=45,
        choices=[
            ('solicitado', 'Solicitado'),
            ('aceptado', 'Aceptado'),
            ('rechazado', 'Rechazado'),
            ('completado', 'Completado'),
        ])
    notas = models.TextField(blank=True, null=True)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True, null=True)
    fecha_completado =models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'relevo'
        managed = True