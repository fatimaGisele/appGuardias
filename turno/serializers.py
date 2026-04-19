from rest_framework import serializers
from .models import Turno
from usuario.models import Usuario
from relevo.models import Relevo
from usuario.serializers import UserSerializer

    
class TurnoSerializer(serializers.ModelSerializer):
    # Mostra los datos del usuario asignado
    usuario_asignado = UserSerializer(source='usuario_asignado', read_only=True)
    
    class Meta:
        model = Turno
        fields = '__all__'

class TurnoCreateSerializer(serializers.ModelSerializer):
    usuario_relevo_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(
            rol__nombre__in=['lider', 'encargado'],  
            activo=True
        ),
        write_only=True
    )
    class Meta:
        model = Turno
        fields = [
            'nombre',
            'descripcion',
            'fecha_inicio',
            'fecha_fin',
            'calendario',
            'grupo_escalamiento',
            'usuario_asignado',   
            'usuario_relevo_id'
            ]    
    def validate(self, data):
        if data['usuario_asignado'] == data['usuario_relevo_id']:
            raise serializers.ValidationError(
            'El usuario encargado de la guardia y el relevo no pueden ser el mismo usuario.'
        )
        rol_nombre = data['usuario_asignado'].rol.nombre
        if rol_nombre not in ['lider', 'encargado']:
            raise serializers.ValidationError(
            'El usuario asignado debe tener el rol de lider o encargado.'
        )
        return data
        
    def create(self, validate_data):
        usuario_relevo = validate_data.pop('usuario_relevo_id')
        request = self.context.get('request')

        turno = Turno.objects.create(
            **validate_data,
            usuario_creador = request.user
        )

        Relevo.objects.create(
            turno_origen = turno,
            turno_destino = turno,
            usuario_origen_solicitante = request.user,
            usuario_destino = usuario_relevo,
            motivo = 'relevo solicitado',
            estado = 'solicitado'
        )
        return turno

            

class TurnoListSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario_asignado.nombre', read_only=True)
    usuario_email = serializers.CharField(source='usuario_asiganado.email', read_only=True)
    
    class Meta:
        model = Turno
        fields = [
            'idturno',
            'grupo_escalamiento',
            'usuario_asignado',
            'usuario_creador',
            'calendario',
            'nombre',
            'descripcion',
            'estado',
            'fecha_inicio',
            'fecha_fin',
            'fecha_creacion',
            'fecha_actualizacion']
