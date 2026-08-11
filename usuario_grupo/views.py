from rest_framework import viewsets, status
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Usuario_grupo
from .serializers import UsuarioGrupoSerializer

class UsuarioGrupoView(viewsets.ModelViewSet):
    queryset = Usuario_grupo.objects.all()
    serializer_class = UsuarioGrupoSerializer
    #permission_classes = [IsAuthenticated]

    def list(self, request): #filtrar x grupo
        queryset = self.queryset
        grupo_id = request.query_params.get('grupo', None)
        usuario_id = request.query_params.get('usuario', None)

        if grupo_id:
            queryset = queryset.filter(grupo_escalamiento=grupo_id)
        if usuario_id:
            queryset = queryset.filter(usuario=usuario_id)

        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data)
        
    @action(detail=True, methods=['post'], url_path='activar')
    def activar(self, request, pk=None):
        usuario_grupo = self.get_object()
        usuario_grupo.activo = True
        usuario_grupo.save()
        return Response({'mensaje': 'Usuario activado en el grupo'})
    
    @action(detail=True, methods=['post'], url_path='desactivar')
    def desactivar(self, request, pk=None):
        usuario_grupo = self.get_object()
        usuario_grupo.activo = False
        usuario_grupo.save()
        return Response({'mensaje': 'Usuario desactivado en el grupo'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mi_equipo(request):
    mi_grupo = Usuario_grupo.objects.filter(
        usuario = request.user,
        activo = True
    ).select_related('grupo_escalamiento')
    resultado = []
    for ug in mi_grupo:
        grupo = ug.grupo_escalamiento
        miembros_grupo = Usuario_grupo.objects.filter(
            grupo_escalamiento = grupo,
            activo = True
        ).select_related('usuario', 'usuario__rol')
        resultado.append({
            'idgrupo': grupo.idgrupo_escalamiento,
            'nombre': grupo.nombre,
            'descripcion': grupo.descripcion,
            'miembros': [{
                'idusuario': m.usuario.idusuario,
                'nombre': m.usuario.nombre,
                'apellido': m.usuario.apellido,
                'email': m.usuario.email,
                'rol': m.usuario.rol.nombre,
                'prioridad': m.prioridad,
            }for m in miembros_grupo]
        })
        return Response(resultado)
