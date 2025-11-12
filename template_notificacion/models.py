from django.db import models

# Create your models here.
class Template_notificacion(models.Model):
    idtemplate_notificacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)
    tipo_evento = models.CharField(max_length=45)
    asunto_email = models.CharField(max_length=150)
    cuerpo_email = models.TextField()
    mensaje_sms = models.TextField()
    activo = models.BooleanField(default=True)
    class Meta:
        db_table = 'template_notificacion'
        managed = True