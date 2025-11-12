from django.db import models
from usuario.models import Usuario

# Create your models here.

class Configuracion_notificacion(models.Model):
    idconfiguracion_notificacion = models.AutoField(primary_key=True)
    usuario_id = models.ForeignKey(
        Usuario,
        on_delete= models.CASCADE
    )
    tipo_de_evento = models.CharField(max_length=45)
    metodo = models.CharField(max_length=45)
    activo = models.BooleanField(default= True)
    minutos_antes_turno = models.IntegerField(default=30)
    intentos_maximo = models.IntegerField(default=3)
    intervalo_reintesto = models.IntegerField(default=10)

    class Meta:
        managed = True
        db_table = 'configuracion_notificacion'

