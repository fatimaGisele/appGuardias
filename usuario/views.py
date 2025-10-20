from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from .serializers import UserSerializer, CreateUserSerializer, ChangePasswordSerializer
from .models import Usuario
from turno.models import Turno
from turno.serializers import TurnoListSerializer

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
        usuario = self.queryset.filter(activo=True)
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
    


