from django.db import models
from calendario.models import Calendario
from usuario.models import Usuario


# Create your models here.
class Turno(models.Model):
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('perdido', 'Perdido'),
    ]
    idturno = models.AutoField(primary_key=True)
    usuario_asignado = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name="turnos_asignado",
        null=True)
    usuario_creador = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name="turnos_creados",
        null=True,)
    calendario_id = models.ForeignKey(
        Calendario,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=45,
        choices=ESTADO_CHOICES,
        default= "programado"
    )
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'turno'
        managed = True

    def __str__(self):
        return self.nombre_turno