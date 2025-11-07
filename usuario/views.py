from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .serializers import UserSerializer, CreateUserSerializer, ChangePasswordSerializer
from .models import Usuario
from turno.models import Turno
from turno.serializers import TurnoListSerializer
import bcrypt

# Create your views here.
class UserView(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer 
    
    def get_serializer_class(self):
        if self.action == 'list':
            return UserSerializer
        elif self.action == 'create':
            return CreateUserSerializer
        return ChangePasswordSerializer
    
    #GET
    def list(self, request):
        usuario = self.queryset.filter(estado=True) #estado true es igual a activo
        serializer = self.get_serializer(usuario, many=True)
        return Response(serializer.data)
    
    #filtra x id
    def retrieve(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)

    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error':'el email o la contraseña son incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            usuario = Usuario.objects.get(email = email)
        except Usuario.DoesNotExist:
            return Response({'error':'el email NO EXISTE'}, status=status.HTTP_401_UNAUTHORIZED)
        if bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('UTF-8')):
            usuarioData = {
                "idusuario": usuario.idusuario,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "email": usuario.email,
                "telefono": usuario.telefono,
                "rol": usuario.rol
            }
            return Response(usuarioData, status=status.HTTP_200_OK)
        else:
            return Response({'error':'el email o la password NO EXISTE'}, status=status.HTTP_401_UNAUTHORIZED)

            
    
    def update(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        serializer = self.get_serializer(usuario, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
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
    


