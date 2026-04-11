from django.db import models
from turno.models import Turno
from usuario.models import Usuario

# Create your models here.
class Incidencia(models.Model):
    GRAVEDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    ESTADO_CHOICES = [
        ('abierta', 'Abierta'),
        ('en_proceso', 'En Proceso'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada')
        ]
    idincidencia = models.AutoField(primary_key=True)
    turno = models.ForeignKey(
        Turno,
        on_delete = models.CASCADE
    ) 
    usuario_reporta = models.ForeignKey(
        Usuario,
        on_delete = models.CASCADE,
        related_name='incidencias_reportadas',
        null= True
    ) 
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    gravedad = models.CharField(
        max_length=45,
        choices=GRAVEDAD_CHOICES)
    estado = models.CharField(
        max_length=45,
        choices=ESTADO_CHOICES,
        default="abierta")
    fecha_ocurrencia = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacionn = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'incidencia'
        managed = True
    
    def __str__(self):
        return self.titulo