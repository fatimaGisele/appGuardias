from django.db import models

class Rol(models.Model):
    idrol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)  
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)


    REQUIRED_FIELDS = ['nombre']
    class Meta:
        managed= True
        db_table = 'rol'

    
    def __str__(self):
        return f"{self.nombre}"

#  choices=[
#         ('guardia', 'Guardia'),
#         ('lider', 'Líder'),
#         ('encargado', 'Encargado'), 
#         ('relevo', 'Relevo')]