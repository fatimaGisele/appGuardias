from django.db import models

# Create your models here.
class Grupo_escalamiento(models.Model):
    idgrupo_escalamiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(blank=True, null=True)
    num_orden_escalamiento = models.IntegerField()
    activo = models.BooleanField(default=True)

    class Meta:
        db_table = 'grupo_escalamiento'
        managed = True
