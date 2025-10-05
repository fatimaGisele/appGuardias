from rest_framework import serializers
from .models import Usuario

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['idusuario','nombre','apellido','email','telefono','rol','estado',
                      'fecha_creacion','fecha_actualizacion','password']
        
    def create(self, validate_data):
        usuario = Usuario.objects.create(**validate_data) 
        return usuario
