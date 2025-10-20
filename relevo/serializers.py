from rest_framework import serializers
from .models import Relevo
from usuario.serializers import UserSerializer
from turno.serializers import TurnoSerializer

class RelevoSerializer(serializers.ModelSerializer):
    usuario_origen_detalle = UserSerializer(source='usuario_idusuario', read_only=True)
    usuario_destino_detalle = UserSerializer(source='usuario_relevo', read_only=True)
    turno_origen_detalle = TurnoSerializer(source='turno_origen', read_only=True)
    turno_destino_detalle = TurnoSerializer(source='turno_destino', read_only=True)
    
    class Meta:
        model = Relevo
        fields = '__all__'

class RelevoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Relevo
        fields = ['idrelevo','turno_origen', 'turno_destino',  
                  'usuario_origen', 'usuario_destino', 'motivo', 'estado', 'notas', 'fecha_solicitud',
                  'fecha_respuesta', 'fecha_completado']