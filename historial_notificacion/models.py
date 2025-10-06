from django.db import models
from usuario.models import Usuario
from relevo.models import Relevo

# Create your models here.
class Historial_notificacion(models.Model):
    idhistorial_notificacion = models.AutoField(primary_key=True)
    usuario_idusuario = models.ForeignKey(
        Usuario,
        on_delete= models.DO_NOTHING,
        db_column= 'usuario_idusario'
    )   
    relevo_idrelevo = models.ForeignKey(
            Relevo,
        on_delete= models.DO_NOTHING,
        db_column= 'relevo_idrelevo'
    )     
    tipo_notificacion = models.CharField(max_length=45)
    contenido = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)
    error_msj_notificacion = models.CharField(max_length=45)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(auto_now_add=True)
    fecha_entrega = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = False
        db_table = 'historial_notificacion'