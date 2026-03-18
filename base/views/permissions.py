from rest_framework import permissions

class IsRRHH(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios en el grupo 'RRHH'.
    """
    def has_permission(self, request, view):
        # 1. ¿Está el usuario autenticado (tiene un token válido)?
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 2. ¿Pertenece al grupo 'RRHH'?
        return request.user.groups.filter(name='RRHH').exists()

class IsVentas(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios en el grupo 'Ventas'.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.groups.filter(name='Ventas').exists()