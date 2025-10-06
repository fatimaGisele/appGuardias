from django.db import models
from turno.models import Turno

# Create your models here.
class Incidencia(models.Model):
    idincidencia = models.AutoField(primary_key=True)
    turno_idturno = models.ForeignKey(
        Turno,
        on_delete = models.DO_NOTHING,
        db_column= 'turno_idturno'
    ) 
    titulo = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=250)
    gravedad = models.CharField(max_length=45)
    estado = models.CharField(max_length=45)
    fecha_ocurrencia = models.DateTimeField(auto_now_add=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacionn = models.DateTimeField(auto_now=True)
    class Meta:
        managed = False
        db_table = 'incidencia'