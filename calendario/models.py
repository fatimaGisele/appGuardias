from django.db import models

# Create your models here.
class Calendario(models.Model):
    idcalendario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=250)
    tipo_calendario = models.CharField(max_length=45)
    estado = models.BooleanField(default=True)
    config_api = models.CharField(max_length=45)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'calendario'