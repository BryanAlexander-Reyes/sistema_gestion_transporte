from rest_framework import permissions


# Roles y permisos
class RolePermission(permissions.BasePermission):
    admin_role = "Administrador"
    operator_role = "Operador"
    auditor_role = "Auditor"
    audit_viewset = "AuditoriaRegistroViewSet"
    admin_viewsets = ("RolViewSet", "PermisoViewSet")

    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True

        view_name = view.__class__.__name__

        if view_name in self.admin_viewsets:
            return self.user_has_role(request.user, self.admin_role)

        if view_name == self.audit_viewset:
            return self.user_has_any_role(
                request.user,
                [self.admin_role, self.auditor_role]
            )

        if request.method in permissions.SAFE_METHODS:
            return True

        return self.user_has_any_role(
            request.user,
            [self.admin_role, self.operator_role]
        )

    def user_has_role(self, user, role_name):
        return (
            user
            and user.is_authenticated
            and user.groups.filter(name=role_name).exists()
        )

    def user_has_any_role(self, user, role_names):
        return (
            user
            and user.is_authenticated
            and user.groups.filter(name__in=role_names).exists()
        )
