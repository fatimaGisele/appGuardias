from django.db import models
from usuario.models import Usuario
from incidencia.models import Incidencia

# Create your models here.
class Escalamiento(models.Model):
    idescalamiento = models.AutoField(primary_key=True)
    incidencia_idincidencia = models.ForeignKey(
        Incidencia,
        on_delete= models.DO_NOTHING,
        db_column= 'incidencia_idincidencia'
    )    
    usuario_idusuario = models.ForeignKey(
        Usuario,
        on_delete= models.DO_NOTHING,
        db_column= 'usuario_idusuario'
    )  
    nivel = models.IntegerField
    tipo_notificacion =models.CharField(max_length=45)
    estado =models.CharField(max_length=45)
    mensaje_enviado = models.CharField(max_length=45)
    fecha_escalamiento = models.DateTimeField(auto_now=True)
    fecha_respuesta  = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'escalamiento'
    