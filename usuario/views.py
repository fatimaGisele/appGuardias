from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import UserSerializer, CreateUserSerializer, ChangePasswordSerializer, UpdateUserSerializer
from .models import Usuario
from turno.models import Turno
from turno.serializers import TurnoListSerializer
from guardiasServer.permissions import EsJefe, es_jefe, es_lider
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class UserView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer 

    def get_permissions(self):
        # lectura, token FCM y estadisticas: cualquier usuario autenticado
        if self.action in ('list', 'retrieve', 'guardar_fcm_token', 'estadisticas_equipo'):
            return [IsAuthenticated()]
        # editar: jefe, o el propio usuario (con campos limitados, ver update)
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated()]
        # crear y desactivar usuarios: solo lider o encargado
        return [EsJefe()]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        elif self.action == 'create':
            return CreateUserSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateUserSerializer
        return ChangePasswordSerializer
    
    #GET
    def list(self, request):
        usuario = self.queryset.filter(activo=True) #estado true es igual a activo
        serializer = self.get_serializer(usuario, many=True)
        return Response(serializer.data)
    
    #filtra x id
    def retrieve(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        serializer = UserSerializer(usuario) #self.get_serializer(usuario)
        return Response(serializer.data)
            
    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # solo un lider puede crear a otro lider
        if serializer.validated_data['rol_id'].nombre.lower() == 'lider' and not es_lider(request.user):
            return Response({'error': 'Solo un lider puede crear otro lider'},
                            status=status.HTTP_403_FORBIDDEN)
        usuario = serializer.save()
        return Response(UserSerializer(usuario).data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None, **kwargs):
        usuario = get_object_or_404(Usuario, pk=pk)
        jefe = es_jefe(request.user)
        if not jefe and usuario.pk != request.user.pk:
            return Response({'error':' No tienes los permisos necesarios'}, status=status.HTTP_403_FORBIDDEN)
        if usuario.rol.nombre.lower() == 'lider' and not es_lider(request.user) == usuario.pk != request.user.pk:
            return Response({'error':' No tienes los permisos necesarios'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        if not jefe:
            permitidos = ('nombre', 'apellido', 'telefono')
            data = {k: v for k, v in request.data.items() if k in permitidos}
        serializer = self.get_serializer(usuario, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(UserSerializer(usuario).data)
    
    
    def destroy(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        usuario.activo = False
        usuario.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
     
    
    def turnos_usuario(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)       
        turnos = Turno.objects.filter(usuario_idusuario=usuario)
        serializer = TurnoListSerializer(turnos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='fcm-token')
    def guardar_fcm_token(self, request):
        token =  request.data.get('token')
        if not token:
            return Response({'error':'Token requerido'}, status=status.HTTP_400_BAD_REQUEST)     
        request.user.fcm_token = token
        request.user.save()
        return Response({'mesagge':'Token guardado'})

    @action(detail=False, methods=['get'], url_path='estadisticas', permission_classes=[IsAuthenticated])
    def estadisticas_equipo(self, request):
        usuario = Usuario.objects.filter(activo = True)
        resultado = []
        for u in usuario:
            turnos = Turno.objects.filter(usuario_asignado=u)
            resultado.append({
                'idusuario':u.idusuario,
                'nombre': u.nombre,
                'apellido': u.apellido,
                'rol': u.rol.nombre,
                'total': turnos.count(),
                'cubiertas': turnos.filter(estado='completado').count(),
                'activas': turnos.filter(estado='activo').count(),
                'perdidas': turnos.filter(estado='perdido').count(),
                'programadas': turnos.filter(estado='programado').count(),
            })
        return Response(resultado)

    


