from rest_framework.permissions import IsAuthenticated


class RolePermissionMixin:
    """
    Supports both GenericAPIView (HTTP methods)
    and ViewSet (actions).

    Examples:

    GenericAPIView:
    role_permissions = {
        "GET": IsAdminManagerEngineer,
        "POST": IsAdminOrManager,
        "PUT": IsAdminOrManager,
        "PATCH": IsAdminOrManager,
        "DELETE": IsSuperAdmin,
    }

    ViewSet:
    role_permissions = {
        "list": IsAdminManagerEngineer,
        "retrieve": IsAdminManagerEngineer,
        "create": IsAdminOrManager,
        "update": IsAdminOrManager,
        "partial_update": IsAdminOrManager,
        "destroy": IsSuperAdmin,
    }
    """

    role_permissions = {}

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        permission_class = None

        # ViewSet action support
        if hasattr(self, "action"):
            permission_class = self.role_permissions.get(
                self.action
            )

        # GenericAPIView / APIView support
        if permission_class is None:
            permission_class = self.role_permissions.get(
                self.request.method
            )

        if permission_class:
            permission_classes.append(permission_class)

        return [permission() for permission in permission_classes]