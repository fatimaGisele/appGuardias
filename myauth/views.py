from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle
from rest_framework import status
from django.conf import settings
from usuario.serializers import CreateUserSerializer
from usuario.models import Usuario
from rol.models import Rol
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken

ROL_REGISTRO_PUBLICO = 'guardia'
class LoginThrottle(AnonRateThrottle):
    scope = 'login'

class RegisterThrottle(AnonRateThrottle):
    scope = 'register'


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([RegisterThrottle])
def register(request):
    """siempre se crea un usuario con el rol de menor privilegio.
    El rol que mande inicialemnte el cliente se ignora; los otros roles los asigna el lider desde POST /usuarios/."""
    if not settings.PUBLIC_REGISTRATION:
        return Response({'error': 'El registro publico esta deshabilitado'},
                        status=status.HTTP_403_FORBIDDEN)

    rol = Rol.objects.filter(nombre__iexact=ROL_REGISTRO_PUBLICO).first()
    if rol is None:
        return Response({'error': 'Registro no disponible: falta configurar los roles'},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)

    data = request.data.copy()
    data['rol_id'] = rol.pk
    serializer = CreateUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message":"'Usuario creado correctamente"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([RegisterThrottle])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    error = Response({'error': 'Email o contraseña incorrectos'}, status= status.HTTP_401_UNAUTHORIZED)

    if not email or not password:
        return error
    try:
        usuario = Usuario.objects.select_related('rol').get(email = email)
    except Usuario.DoesNotExist:
        return error

    try:
        password_ = bcrypt.checkpw(password.encode('utf-8'), usuario.password.encode('UTF-8'))
    except ValueError:
        password_ = False
    
    if not password_ or not usuario.activo or not usuario.is_active:
        return error
    
    refreshToken = RefreshToken.for_user(usuario)
    access = refreshToken.access_token
    return Response({
        "refreshToken" : str(refreshToken),
        "access": str(access),
            "usuario": {
            "idusuario": usuario.idusuario,
            "nombre": usuario.nombre,
            "apellido": usuario.apellido,
            "email": usuario.email,
            "telefono": usuario.telefono,
            "rol": usuario.rol.nombre,
            "rol_id": usuario.rol.idrol,
            }
    }
   , status=status.HTTP_200_OK)

            
    
    
    
 
    
