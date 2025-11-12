from django.db import models

# Create your models here.
class Calendario(models.Model):
    idcalendario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tipo_calendario = models.CharField(max_length=45)
    activo = models.BooleanField(default=True)
    config_api = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = True
        db_table = 'calendario'

    def __str__(self):
        return self.nombre