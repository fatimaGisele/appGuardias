from rest_framework import serializers
from .models import Usuario

#listar
class UserSerializer(serializers.ModelSerializer):
      class Meta:
        model = Usuario
        fields = ['idusuario','nombre','apellido','email','telefono','rol','estado',
                      'fecha_creacion','fecha_actualizacion']
        
#crear y validar
class CreateUserSerializer(serializers.ModelSerializer):
        password = serializers.CharField(write_only=True)
        password2 = serializers.CharField(write_only=True)
        class Meta:
            model = Usuario
            fields = ['idusuario','nombre','apellido','email','telefono','rol','estado',
                        'fecha_creacion','fecha_actualizacion','password','password2']
            
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
                password = validated_data.pop('password')
                usuario = Usuario(**validated_data)
                usuario.set_password(password)
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