from twilio.rest import Client
from django.conf import settings
from historial_notificacion.models import Historial_notificacion
import logging

logger = logging.getLogger(__name__)

def enviar_whatsapp(usuario, msg, escalamiento):
    cliente = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    estado  = 'enviado'
    error_msg = None

    try:
        cliente.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            to= f"whatsapp:+{usuario.telefono}",
            body=msg
        )
    except Exception as e:
        estado = "fallido"
        error_msg = str(e)
        logger.error(f"error enviando msg de whatapp al usuario {usuario.email}")

    
    Historial_notificacion.objects.create(
        usuario = usuario,
        escalamiento = escalamiento,
        tipo_notificacion = 'whatsapp sms',
        contenido = msg,
        estado = estado,
        mensaje_error = error_msg
    )

    return estado == 'enviado'


def enviar_msj_relevo(usuario, mensaje):
    cliente = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        cliente.messages.create(
            from_=settings.TWILIO_WHATSAPP_FROM,
            to= f"whatsapp:+{usuario.telefono}",
            body=mensaje
        )
        return True
    except Exception as e:
        logger.error(f"el mensaje fallo {e}")
        return False 

        