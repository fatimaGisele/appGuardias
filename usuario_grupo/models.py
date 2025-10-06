from django.db import models
from usuario.models import Usuario
from grupo_escalamiento.models import Grupo_escalamiento

# Create your models here.
class Usuario_grupo(models.Model):
    idusuario_grupo = models.AutoField(primary_key=True)
    idusuario = models.ForeignKey(
        Usuario, 
        on_delete=models.DO_NOTHING,
        db_column='idusuario'
    )
    idgrupo_escalamiento = models.ForeignKey(
        Grupo_escalamiento,
        on_delete= models.DO_NOTHING,
        db_column='idgrupo_escalamiento'
    )
    prioridad = models.IntegerField
    estado =models.BooleanField(default=True)
    class Meta:
        managed =False
        db_table = 'usuario_grupo'