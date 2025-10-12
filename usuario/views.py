from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from .serializers import UserSerializer, CreateUserSerializer, ChangePasswordSerializer
from .models import Usuario

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
    
    @api_view(['GET'])
    def list(self, request):
        usuario = self.queryset.filter(activo=True)
        serializer = self.get_serializer(usuario, many=True)
        return Response(serializer.data)
    
    @api_view(['GET']) #filtra x id
    def retrieve(self, request, pk=None):
        usuario = get_object_or_404(Usuario, pk=pk)
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)

    @api_view(['POST'])
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


