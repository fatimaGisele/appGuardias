from rest_framework import viewsets
from .models import Grupo_escalamiento
from .serializers import GrupoEscalamientoSerializer
from rest_framework.permissions import IsAuthenticated

class GrupoEscalamientoView(viewsets.ModelViewSet):
    queryset = Grupo_escalamiento.objects.all()
    serializer_class = GrupoEscalamientoSerializer
    #permission_classes = [IsAuthenticated]
