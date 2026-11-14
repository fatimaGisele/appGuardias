from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Rol
from .serializers import RolSerializer
from guardiasServer.permissions import SoloJefeEscribe

class RolView(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [SoloJefeEscribe]


