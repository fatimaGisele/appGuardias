from django.db import models
from django.contrib.auth.models import AbstractUser
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
    password = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'usuario'

class User(AbstractUser):
    telefono = models.CharField(max_length=45, blank=True, null=True)
    rol = models.CharField(max_length=45, blank=True, null=True)
    
    def __str__(self):
        return self.username