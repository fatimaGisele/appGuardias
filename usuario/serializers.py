from rest_framework import serializers
from .models import Usuario
from django.contrib.auth import authenticate
import bcrypt

#listar
class UserSerializer(serializers.ModelSerializer):
      class Meta:
        model = Usuario
        fields = ['idusuario','nombre','apellido','email','telefono','rol','activo',
                      'fecha_creacion','fecha_actualizacion']
        
#crear y validar
class CreateUserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)
        password2 = serializers.CharField(write_only=True)
        class Meta:
            model = Usuario
            fields = ['idusuario','nombre','apellido','email','telefono','rol','activo',
                        'fecha_creacion','fecha_actualizacion','password','password2']
            extra_kwargs = {
               'password' : {'write_only': True}
            }

        def validatePsw(self, data):
                if data['password'] !=  data['password2']:
                    raise serializers.ValidationError("Las contraseñas no coinciden")
                return data

        def validate_email(self, value):
                if Usuario.objects.filter(email=value).exists():
                    raise serializers.ValidationError("Este email ya existe")
                return value
            
        def create(self, validated_data):
                validated_data.pop('password2')
                raw_password = validated_data.pop('password')

                hashed_password = bcrypt.hashpw(
                raw_password.encode('utf-8'),
                 bcrypt.gensalt()
                ).decode('utf-8')

                usuario = Usuario(**validated_data)
                usuario.password = hashed_password
                usuario.save()
                return usuario
            
    
 #cambiar constraseña       
class ChangePasswordSerializer(serializers.Serializer):
        vieja_password = serializers.CharField(write_only=True)
        new_password = serializers.CharField(write_only=True)
        new_password2 = serializers.CharField(write_only=True)

        def validate(self, data):
            if data['new_password'] != data['new_password2']:
                raise serializers.ValidationError( "Las contraseñas no coinciden")
            return data