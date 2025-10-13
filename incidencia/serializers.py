from rest_framework import serializers
from .models import Incidencia
from turno.serializers import TurnoSerializer

class IncidenciaSerializer(serializers.ModelSerializer):
    turno_detalle = TurnoSerializer(source='idturno', read_only=True)
    
    class Meta:
        model = Incidencia
        fields = '__all__'

class IncidenciaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incidencia
        fields = ['idincidencia','turno_idturno', 'titulo', 'descripcion', 'gravedad', 'estado',
                  'fecha_ocurrencia', 'fecha_creacion', 'fecha_actualizacion']
        
    def validate_gravedad(self, value):
        #gravedad del asunto xF
        valores_validos = ['baja', 'media', 'alta', 'critica']
        if value not in valores_validos:
            raise serializers.ValidationError(f"Gravedad debe ser: {', '.join(valores_validos)}")
        return value