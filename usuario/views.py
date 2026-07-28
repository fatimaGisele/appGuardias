from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import UserSerializer, CreateUserSerializer, ChangePasswordSerializer, UpdateUserSerializer
from .models import Usuario
from turno.models import Turno
from turno.serializers import TurnoListSerializer
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class UserView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer 
    
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
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)
            
    
    def update(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        serializer = self.get_serializer(usuario, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(usuario).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
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

    


