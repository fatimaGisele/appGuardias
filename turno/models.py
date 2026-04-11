from django.db import models
from calendario.models import Calendario
from usuario.models import Usuario
from grupo_escalamiento.models import Grupo_escalamiento


# Create your models here.
class Turno(models.Model):
    ESTADO_CHOICES = [
        ('programado', 'Programado'),
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('perdido', 'Perdido'),
    ]
    idturno = models.AutoField(primary_key=True)
    grupo_escalamiento = models.ForeignKey(
        Grupo_escalamiento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='turnos'
    )
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
    calendario = models.ForeignKey(
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
        return self.nombre