from django.db import models

# Create your models here.
class Template_notificacion(models.Model):
    idtemplate_notificacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    tipo_evento = models.CharField(max_length=45)
    asunto_email = models.CharField(max_length=45)
    cuerpo_email = models.CharField(max_length=500)
    mensaje_sms = models.CharField(max_length=45)
    estado = models.BooleanField(default=True)
    class Meta:
        mananaged = False
        db_table = 'template_notificacion'