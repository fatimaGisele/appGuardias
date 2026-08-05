from rest_framework import serializers
from .models import Vacacion
from usuario.models import Usuario
from datetime import date, timedelta

def calcular_dias_habiles(fecha_inicio, fecha_fin):
    """Cuenta días hábiles entre dos fechas"""
    dias = 0
    actual = fecha_inicio
    while actual <= fecha_fin:
        if actual.weekday() < 5:  
            dias += 1
        actual += timedelta(days=1)
    return dias

def dias_vacaciones_segun_antiguedad(fecha_ingreso):
    """días disponibles según antigüedad"""
    if not fecha_ingreso:
        return 15
    hoy = date.today()
    años = (hoy - fecha_ingreso).days // 365
    if años < 5:
        return 15
    elif años < 10:
        return 20
    elif años < 15:
        return 25
    elif años < 20:
        return 30
    else:
        return 35

def dias_usados_en_año(usuario, año):
    """Días hábiles ya usados o pendientes en el año"""
    from .models import Vacacion
    vacaciones = Vacacion.objects.filter(
        usuario=usuario,
        fecha_inicio__year=año,
        estado__in=['aprobada', 'pendiente']
    )
    return sum(v.dias_habiles for v in vacaciones)


class VacacionSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(
        source='usuario.nombre', read_only=True)
    aprobador_nombre = serializers.CharField(
        source='aprobador.nombre', read_only=True)

    class Meta:
        model = Vacacion
        fields = [
            'idvacacion', 'usuario', 'usuario_nombre',
            'aprobador', 'aprobador_nombre',
            'fecha_inicio', 'fecha_fin', 'dias_habiles',
            'motivo', 'estado', 'nota_aprobador',
            'fecha_solicitud', 'fecha_respuesta',
        ]
        read_only_fields = [
            'idvacacion', 'dias_habiles', 'estado',
            'fecha_solicitud', 'fecha_respuesta',
        ]


class SolicitarVacacionSerializer(serializers.ModelSerializer):
    aprobador = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(
            rol__nombre__in=['lider', 'encargado'],
            activo=True
        )
    )

    class Meta:
        model = Vacacion
        fields = ['fecha_inicio', 'fecha_fin', 'motivo', 'aprobador']

    def validate(self, data):
        inicio = data['fecha_inicio']
        fin = data['fecha_fin']
        usuario = self.context['request'].user

        if fin < inicio:
            raise serializers.ValidationError(
                'La fecha de fin debe ser posterior al inicio.'
            )
        if inicio < date.today():
            raise serializers.ValidationError(
                'La fecha de inicio no puede ser en el pasado.'
            )

        dias = calcular_dias_habiles(inicio, fin)
        if dias == 0:
            raise serializers.ValidationError(
                'El período seleccionado no contiene días hábiles.'
            )

        # Verificar días disponibles
        dias_disponibles = dias_vacaciones_segun_antiguedad(usuario.fecha_ingreso)
        dias_usados = dias_usados_en_año(usuario, inicio.year)
        dias_restantes = dias_disponibles - dias_usados

        if dias > dias_restantes:
            raise serializers.ValidationError(
                f'No tenés suficientes días disponibles. '
                f'Solicitás {dias} días hábiles pero solo tenés {dias_restantes} disponibles.'
            )

        data['dias_habiles'] = dias
        return data

    def create(self, validated_data):
        usuario = self.context['request'].user
        return Vacacion.objects.create(
            usuario=usuario,
            **validated_data
        )