from django.db import models
from usuario.models import Usuario
from grupo_escalamiento.models import Grupo_escalamiento

# Create your models here.
class Usuario_grupo(models.Model):
    idusuario_grupo = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name='grupos',
        null= True
    )
    grupo_escalamiento = models.ForeignKey(
        Grupo_escalamiento,
        on_delete= models.CASCADE,
        related_name='usuarios',
        null=True
    )
    prioridad = models.IntegerField()
    activo =models.BooleanField(default=True)
    class Meta:
        db_table = 'usuario_grupo'
        unique_together = ('usuario', 'grupo_escalamiento')
        managed = True