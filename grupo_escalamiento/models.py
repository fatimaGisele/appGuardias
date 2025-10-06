from django.db import models

# Create your models here.
class Grupo_escalamiento(models.Model):
    idgrupo_escalamiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=250)
    num_orden_escalamiento = models.IntegerField
    estado = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'grupo_escalamiento'
