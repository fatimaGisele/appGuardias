from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, viewsets
from .serializers import TurnoSerializer, TurnoCreateSerializer, TurnoListSerializer
from .models import Turno
# Create your views here.
class TurnoViewSet(viewsets.ModelViewSet):
    queryset = Turno.objects.all()
    # serializer_class = TurnoSerializer
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TurnoListSerializer
        elif self.action == 'create':
            return TurnoCreateSerializer
        return TurnoSerializer
    
    @api_view(['POST'])
    def create(request):
        serializer = TurnoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

