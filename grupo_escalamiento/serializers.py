from rest_framework import serializers
from .models import Grupo_escalamiento

class GrupoEscalamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupo_escalamiento
        fields = [
            'idgrupo_escalamiento',
            'nombre',
            'descripcion',
            'num_orden_escalamiento',
            'activo'
        ]
        read_only_fields = ['idgrupo_escalamiento']