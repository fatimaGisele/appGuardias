from django.db import models
from turno.models import Turno

# Create your models here.
class Incidencia(models.Model):
    idincidencia = models.AutoField(primary_key=True)
    turno_id = models.ForeignKey(
        Turno,
        on_delete = models.CASCADE
    ) 
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    gravedad = models.CharField(
        max_length=45,
        choices=[
            ('baja', 'Baja'),
            ('media', 'Media'),
            ('alta', 'Alta'),
            ('critica', 'Crítica'),
        ])
    estado = models.CharField(
        max_length=45,
        choices=[
            ('abierta', 'Abierta'),
            ('en_proceso', 'En Proceso'),
            ('resuelta', 'Resuelta'),
            ('cerrada', 'Cerrada'),
        ])
    fecha_ocurrencia = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacionn = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'incidencia'
        managed = True
    
    def __str__(self):
        return self.titulo