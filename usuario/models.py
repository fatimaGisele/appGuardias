from django.db import models

# Create your models here.
class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    email = models.CharField(max_length=45, unique=True)
    telefono = models.CharField(max_length=45)
    rol = models.CharField(max_length=45)
    estado = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'usuario'
