from django.db import models

class Rol(models.Model):
    CHOICES_ROL=[
        ('guardia', 'Guardia'),
        ('lider', 'Líder'),
        ('encargado', 'Encargado'), 
        ('relevo', 'Relevo')]

    idrol = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=50, 
        choices=CHOICES_ROL,
        default= "guardia")  
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)


    REQUIRED_FIELDS = ['nombre']
    class Meta:
        managed= True
        db_table = 'rol'

    
    def __str__(self):
        return f"{self.nombre}"

