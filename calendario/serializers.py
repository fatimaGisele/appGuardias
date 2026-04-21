from rest_framework import serializers
from .models import Calendario

class CalendarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendario
        fields = [
            'idcalendario',
            'nombre',
            'descripcion',
            'tipo_calendario',
            'activo',
            'config_api',
            'fecha_creacion'
            ]
        read_only_fields = ['idcalendario', 'fecha_creacion']

class CalendarioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendario
        fields = [
            'nombre',
            'descripcion',
            'tipo_calendario'
        ]
    def create(self, validated_data):
        calendario = Calendario.objects.create(
            **validated_data,
            activo = True
            )
        return calendario
