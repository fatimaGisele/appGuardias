from rest_framework import serializers
from .models import Usuario_grupo
from usuario.serializers import UserSerializer
from grupo_escalamiento.serializers import GrupoEscalamientoSerializer

class UsuarioGrupoSerializer(serializers.ModelSerializer):
    usuario_detalle = UserSerializer(source='usuario', read_only=True)
    grupo_detalle = GrupoEscalamientoSerializer(source='grupo_escalamiento', read_only=True)
    class Meta:
        model = Usuario_grupo
        fields = [
            'idusuario_grupo',
            'usuario',
            'grupo_escalamiento',
            'prioridad',
            'activo'
        ]
        read_only_fields = ['idusuario_grupo']

 
    def validated(self, data):
        existe = Usuario_grupo.objects.filter(
            usuario = data['usuario'],
            grupo_escalamiento = data['grupo_escalamiento']
        )
        if self.instance:
            existe = existe.include(pk=self.instance.pk)
        if existe.exists():
            raise serializers.ValidationError(
                'Este usuario ya pertenece a este grupo de escalamiento.'
            )
        return data