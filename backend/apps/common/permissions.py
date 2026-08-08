from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Allows access only to SUPER_ADMIN users.
    """

    message = "Super Admin access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == "SUPER_ADMIN"
        )


class IsAdminOrSuperAdmin(BasePermission):
    """
    Allows access to ADMIN and SUPER_ADMIN users.
    """

    message = "Admin or Super Admin access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {
                "ADMIN",
                "SUPER_ADMIN",
            }
        )


class IsManagerOrAbove(BasePermission):
    """
    Allows access to MANAGER, ADMIN, and SUPER_ADMIN users.
    """

    message = "Manager, Admin, or Super Admin access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {
                "MANAGER",
                "ADMIN",
                "SUPER_ADMIN",
            }
        )


class IsStaffUser(BasePermission):
    """
    Allows access to all internal construction-management staff.

    CUSTOMER users are excluded.
    """

    message = "Staff access is required."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in {
                "SUPER_ADMIN",
                "ADMIN",
                "MANAGER",
                "ENGINEER",
                "WORKER",
            }
        )


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Allows authenticated users to access the API.

    Unauthenticated users may only perform safe/read-only requests.
    """

    def has_permission(self, request, view):
        if request.method in {"GET", "HEAD", "OPTIONS"}:
            return True

        return bool(
            request.user
            and request.user.is_authenticated
        )