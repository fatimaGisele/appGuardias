from django.db import models
from calendario.models import Calendario
from usuario.models import Usuario


# Create your models here.
class Turno(models.Model):
    idturno = models.AutoField(primary_key=True)
    usuario_idusuario = models.ForeignKey(
        Usuario, 
        on_delete=models.DO_NOTHING,  
        db_column='usuario_idusuario')
    calendario_idcalendario = models.ForeignKey(
        Calendario,
        on_delete=models.DO_NOTHING,  
        db_column='calendario_idcalendario'
    )
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=250)
    estado = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField(auto_now=True)
    fecha_fin = models.DateTimeField(auto_now=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'turno'