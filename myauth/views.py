from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from usuario.serializers import CreateUserSerializer
from usuario.models import Usuario
from rol.models import Rol
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def register(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"'Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({'error':'el email o la contraseña son incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        usuario = Usuario.objects.get(email = email)
    except Usuario.DoesNotExist:
        return Response({'error':'el email NO EXISTE'}, status=status.HTTP_401_UNAUTHORIZED)
    
    if bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('UTF-8')):
        refreshToken = RefreshToken.for_user(usuario)
        access = refreshToken.access_token
        usuarioData = ({
            "refreshToken" : str(refreshToken),
            "access": str(access),
            "usuario": {
            "idusuario": usuario.idusuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "rol": usuario.rol.nombre,
            "rol_id": usuario.rol.idrol,}
        })
        return Response(usuarioData, status=status.HTTP_200_OK)
    else:
        return Response({'error':'el email o la password NO EXISTE'}, status=status.HTTP_401_UNAUTHORIZED)

            
    
    
    
 
    
