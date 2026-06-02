from rest_framework.permissions import BasePermission

class EsJefe(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.rol.nombre in ['lider', 'encargado'] 
            )