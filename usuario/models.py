from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, password, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, apellido, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True')
        return self.create_user(email, nombre, apellido, password, **extra_fields)

class Usuario(AbstractUser):
    username = None
    idusuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=45)
    rol = models.CharField(
        max_length=45,
        choices=[
        ('guardia', 'Guardia'),
        ('lider', 'Líder'),
        ('encargado', 'Encargado'), 
        ('relevo', 'Relevo')])
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']
    class Meta:
        managed= True
        db_table = 'usuario'

    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"