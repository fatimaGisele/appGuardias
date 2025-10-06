from django.db import models
from usuario.models import Usuario

# Create your models here.

class Configuracion_notificacion(models.Model):
    idconfiguracion_notificacion = models.AutoField(primary_key=True)
    usuario_idusuario = models.ForeignKey(
        Usuario,
        on_delete= models.DO_NOTHING,
        db_column= 'usuario_idusuario'
    )
    tipo_de_evento = models.CharField(max_length=45)
    metodo = models.CharField(max_length=45)
    estado = models.BooleanField(default= True)
    minutos_antes_turno = models.IntegerField
    intentos_maximo = models.IntegerField
    intervalo_reintesto = models.IntegerField

    class Meta:
        managed = False
        db_table = 'configuracion_notificacion'

