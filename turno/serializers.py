from rest_framework import serializers
from .models import Turno
from usuario.models import Usuario
from relevo.models import Relevo
from usuario.serializers import UserSerializer
from calendario.services import crear_evento_google
from turno.scheduler import programar_notificaciones_turno
from vacacion.models import Vacacion
    
class TurnoSerializer(serializers.ModelSerializer):
    # Mostra los datos del usuario asignado
    usuario_asignado = UserSerializer(read_only=True)
    
    class Meta:
        model = Turno
        fields = '__all__'

class TurnoCreateSerializer(serializers.ModelSerializer):
    usuario_relevo_id = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(
            rol__nombre__in=['guardia','relevo'],  
            activo=True
        ),
        write_only=True
    )
    forzar = serializers.BooleanField(default=False, write_only=True)
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
            'usuario_relevo_id',
            'forzar'
            ]   
         
    def validate(self, data):
        forzar = data.pop('forzar', False)
        if data['usuario_asignado'] == data['usuario_relevo_id']:
            raise serializers.ValidationError(
            'El usuario encargado de la guardia y el relevo no pueden ser el mismo usuario.'
        )
        rol_nombre = data['usuario_asignado'].rol.nombre
        if rol_nombre not in ['guardia', 'relevo']:
            raise serializers.ValidationError(
            'El usuario asignado debe tener el rol de guardia o relevo'
        )
        if not forzar:
            inicio = data['fecha_inicio'].date()
            fin = data['fecha_fin'].date()

            vacas = Vacacion.objects.filter(
                usuario=data['usuario_asignado'],
                estado='aprobada',
                fecha_inicio__lte=fin,
                fecha_fin__gte=inicio,
            ).first()

            if vacas:
                raise serializers.ValidationError({
                    'usuario_asignado':(
                        f'{data["usuario_asignado"].nombre} {data["usuario_asignado"].apellido}'
                        f'Tiene vacaciones aprobadas del {vacas.fecha_inicio.strftime("%d/%m/%Y")}'
                        f'al {vacas.fecha_fin.strftime("%d/%m/%Y")}'
                        f'¿Queres asignarle la guardia de todos modos?'
                    )
                })
        data['forzar'] = forzar
        return data



        
    def create(self, validated_data):
        validated_data.pop('forzar', None)
        usuario_relevo = validated_data.pop('usuario_relevo_id')
        request = self.context.get('request')

        turno = Turno.objects.create(
            **validated_data,
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
        crear_evento_google(turno)
        programar_notificaciones_turno(turno)
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
            'fecha_actualizacion',
            'usuario_nombre',
            'usuario_email'
            ]

