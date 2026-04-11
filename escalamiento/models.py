from django.db import models
from usuario.models import Usuario
from incidencia.models import Incidencia

# Create your models here.
class Escalamiento(models.Model):
    ESTADO_CHOICES = [
            ('pendiente', 'Pendiente'),
            ('enviado', 'Enviado'),
            ('confirmado', 'Confirmado'),
            ('fallido', 'Fallido'),
        ]
    idescalamiento = models.AutoField(primary_key=True)
    incidencia = models.ForeignKey(
        Incidencia,
        on_delete= models.CASCADE
    )    
    usuario_notificado = models.ForeignKey(
        Usuario,
        on_delete= models.CASCADE
    )  
    nivel = models.IntegerField()
    tipo_notificacion = models.CharField(max_length=45)
    estado =models.CharField(
        max_length=45,
        choices=ESTADO_CHOICES,
        default="enviado")
    mensaje_enviado = models.TextField(blank=True, null=True)
    fecha_escalamiento = models.DateTimeField(auto_now=True)
    fecha_respuesta  = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'escalamiento'
        managed = True
    