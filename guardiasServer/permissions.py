from rest_framework.permissions import BasePermission, SAFE_METHODS

ROLES_JEFE = ('lider', 'encargado')

def _rol(user):
    if not (user and user.is_authenticated) or not getattr(user, 'rol_id', None):
        return ''
    return user.rol.nombre.lower()


def es_jefe(user):
    return _rol(user) in ROLES_JEFE


def es_lider(user):
    return _rol(user) == 'lider'


class EsJefe(BasePermission):
    """Solo lider o encargado."""
    def has_permission(self, request, view):
        return es_jefe(request.user)


class SoloJefeEscribe(BasePermission):
    """Cualquier usuario autenticado puede leer; solo lider o encargado escriben."""
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return es_jefe(request.user)