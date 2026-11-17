import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from django.conf import settings
from .models import Calendario
from datetime import datetime
import logging
from googleapiclient.errors import HttpError

logging = logging.getLogger(__name__)
TZ = 'America/Argentina/Buenos_Aires'


def get_flow():
    return Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=  settings.GOOGLE_SCOPES,
        redirect_uri = settings.GOOGLE_REDIRECT_URI
    )

def get_credentials(calendario):
    config = json.loads(calendario.config_api)
    expiry = None
    if config.get('expira'):
        expiry = datetime.fromisoformat(config['expiry'])
    cred = Credentials(
        token = config['token'],
        refresh_token= config['refresh_token'],
        token_uri = 'https://oauth2.googleapis.com/token',
        client_id = config['client_id'],
        client_secret = config['client_secret'],
        scopes = settings.GOOGLE_SCOPES,
        expiry = expiry
    )
    if cred.refresh_token and (cred.expiry is None or cred.expired):
        cred.refresh(Request())
        #Si no sabemos cuando vence el token o si ya se vencio, se refresca y se guarda el token junto con l fecha de vencimientoooooooo ahhhhh
        config['token'] = cred.token
        config['expiry'] = cred.expiry.isoformat() if cred.expiry else None
        calendario.config_api = json.dumps(config)
        calendario.save(update_fields=['config_api'])

    return cred

def crear_evento_google(turno):
    try:
        calendario = turno.calendario
        if not calendario or not calendario.config_api:
            return None
        creds = get_credentials(calendario)
        service = build('calendar', 'v3', credentials=creds)

        evento = {
            'summary': f'Turno: {turno.nombre}',
            'description': turno.descripcion or '',
            'start': {
                'dateTime': turno.fecha_inicio.isoformat(),
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
            'end': {
                'dateTime': turno.fecha_fin.isoformat(),
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': 30},  # recordatorio 30 min antes
                ],
            },
            'guestsCanModify': False,
            'guestsCanInviteOthers': False
        }
        usuario = turno.usuario_asignado
        if usuario and usuario.email:
            evento['attendees'] = [{'email': usuario.email}]

        evento_creado = service.events().insert(
            calendarId='primary',
            body=evento,
            sendUpdates='all'
        ).execute()
        return evento_creado.get('id')
    except Exception as e:
        logging.error(f"Error creando evento en Google Calendar: {e}")
        return None

def actualizar_evento_google(turno):
    if not turno.google_event_id:
        return crear_evento_google(turno)
    try:
        calendario = turno.calendario
        if not calendario or not calendario.config_api:
            return None
        creds =get_credentials(calendario) 
        service = build('calendar', 'v3', credentials=creds)
        cambios = {
            'summary': f'Turno: {turno.nombre}',
            'description': turno.descripcion or '',
            'start': {
                'dateTime': turno.fecha_inicio.isoformat(),
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
            'end': {
                'dateTime': turno.fecha_fin.isoformat(),
                'timeZone': 'America/Argentina/Buenos_Aires',
            },
        }
        usuario = turno.usuario_asignado
        if usuario and usuario.email:
            cambios['attendees'] = [{'email': usuario.email}]

        service.events().patch(
            calendarId = 'primary',
            eventId = turno.google_event_id,
            body = cambios,
            sendUpdates = 'all'
        ).execute()
        return turno.google_event_id
    except Exception as e:
        logging.error(f"Error actualizando evento en Google Calendar: {e}")
        return None 
        
        
def cancelar_evento_google(turno):
    if not turno.google_event_id:
        return True
    try:
        calendario = turno.calendario
        if not calendario or not calendario.config_api:
            return False
        creds = get_credentials(calendario)
        service = build('calendar', 'v3', credentials=creds)
        service.events().delete(
            calendarId ='primary',
            eventId = turno.google_event_id,
            sendUpdates='all'
        ).execute()
        return True
    except HttpError as e:
        if e.resp.status in (404, 410):  
            return True
        logging.error(f"Error cancelando evento en Google Calendar: {e}")
        return False
    except Exception as e:
        logging.error(f"Error cancelando evento en Google Calendar: {e}")
        return False

def guardar_evento_turno(turno):
    # Crea evento en Google y guarda su id en el turno, para poder actualizarlo o cancelarlo despues.
    event_id = crear_evento_google(turno)
    if event_id:
        turno.google_event_id = event_id
        turno.save(update_fields=['google_event_id'])
    return event_id


def sincronizar_evento_turno(turno):
    event_id = actualizar_evento_google(turno)
    if event_id and event_id != turno.google_event_id:
        turno.google_event_id = event_id
        turno.save(update_fields=['google_event_id'])
    return event_id