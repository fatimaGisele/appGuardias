from django.db import models
from usuario.models import Usuario
from relevo.models import Relevo
from escalamiento.models import Escalamiento

# Create your models here.
class Historial_notificacion(models.Model):
    idhistorial_notificacion = models.AutoField(primary_key=True)
    usuario_id = models.ForeignKey(
        Usuario,
        on_delete= models.CASCADE
    )   
    relevo_id = models.ForeignKey(
            Relevo,
        on_delete= models.CASCADE,
        null=True, 
        blank=True
    )     
    escalamiento = models.ForeignKey(
        Escalamiento, 
        on_delete=models.CASCADE,
        null=True, 
        blank=True)
    tipo_notificacion = models.CharField(max_length=45)
    contenido = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=45,
        choices=[
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("leido", "Leído"),
        ("fallido", "Fallido"),
    ])
    mensaje_error = models.TextField(blank=True, null=True)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    fecha_lectura = models.DateTimeField(blank=True, null=True)
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    class Meta:
        db_table = 'historial_notificacion'
        managed = True

    def __str__(self):
        destino = (
            f"Escalamiento {self.escalamiento.id_escalamiento}"
            if self.escalamiento else
            f"Relevo {self.relevo.id_relevo}" if self.relevo else
            "Sin destino"
        )
        return f"Notificación {self.id_historial} - {self.estado} ({destino})"