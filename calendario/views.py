import json
from django.shortcuts import redirect
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .services import get_flow
from django.conf import settings
from .models import Calendario
from .serializers import CalendarioSerializer, CalendarioCreateSerializer


class CalendarioView(viewsets.ModelViewSet):
    queryset = Calendario.objects.all()
    serializer_class = CalendarioSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CalendarioCreateSerializer
        return CalendarioSerializer
    
    def create(self, request):
        serializer = CalendarioCreateSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='conectar')
    def conectar_google(self, request, pk = None):
        calendario = self.get_object()
        plataforma = request.GET.get('plataforma', 'web')
        redirect_uri = (
                settings.GOOGLE_REDIRECT_URI_MOBILE
                if plataforma == 'mobile'
                else settings.GOOGLE_REDIRECT_URI_WEB
            )
        flow = get_flow(redirect_uri = redirect_uri)
        auth_url , state = flow.authorization_url(
            access_type = 'offline',
            include_granted_scopes = 'true',
            state = f"{calendario.idcalendario}:{request.user.idusuario}"
        )
        return Response({'auth_url': auth_url})

    @action(detail=True, methods=['post'], url_path='desconectar')
    def desconectar_google(self, request, pk=None):
        calendario = self.get_object()
        calendario.config_api = None
        calendario.tipo_calendario = ''
        calendario.activo = False
        calendario.save()
        return Response({'mensaje': 'Google Calendar desconectado correctamente'})

    @action(detail=True, methods=['get'], url_path='estado')
    def estado_conexion(self, request, pk=None):
        calendario = self.get_object()
        conectado = bool(calendario.config_api)
        return Response({
                'calendario': calendario.nombre,
                'conectado': conectado,
                'tipo': calendario.tipo_calendario if conectado else None,
            })




@api_view(['GET'])
def google_oauth_callback(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code or not state:
        return Response({'error': 'Parámetros inválidos'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        calendario_id, usuario_id = state.split(':')
        calendario = Calendario.objects.get(idcalendario=calendario_id)
    except (ValueError, Calendario.DoesNotExist):
        return Response({'error': 'Calendario no encontrado'},status=status.HTTP_404_NOT_FOUND)

    flow = get_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials

    # Guardamos el token en configuracion_api 
    calendario = Calendario.objects.get(idcalendario=calendario_id)
    calendario.tipo_calendario = 'google'
    calendario.config_api = json.dumps({
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
    })
    calendario.activo = True
    calendario.save()

    return Response({'mensaje': 'Google Calendar conectado correctamente'})