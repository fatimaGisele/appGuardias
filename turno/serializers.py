from rest_framework import serializers
from .models import Turno
from usuario.serializers import UserSerializer

    
class TurnoSerializer(serializers.ModelSerializer):
    # Mostra los datos del usuario asignado
    usuario_asignado = UserSerializer(source='idusuario', read_only=True)
    
    class Meta:
        model = Turno
        fields = '__all__'

class TurnoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = ['idturno','usuario_idusuario','calendario_idcalendario','nombre','descripcion','estado',
                      'fecha_inicio','fecha_fin','fecha_creacion','fecha_actualizacion']    
        def create(self, validate_data):
            turno = Turno.objects.create(**validate_data) 
            return turno

class TurnoListSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='idusuario.nombre', read_only=True)
    usuario_email = serializers.CharField(source='idusuario.email', read_only=True)
    
    class Meta:
        model = Turno
        fields = ['idturno','usuario_idusuario','calendario_idcalendario','nombre','descripcion','estado',
                      'fecha_inicio','fecha_fin','fecha_creacion','fecha_actualizacion']
