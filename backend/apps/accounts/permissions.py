from rest_framework.permissions import BasePermission

from .models import User


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.SUPER_ADMIN
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ADMIN
        )


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.MANAGER
        )


class IsEngineer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.ENGINEER
        )


class IsWorker(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == User.Role.WORKER
        )


class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.SUPER_ADMIN,
                User.Role.ADMIN,
                User.Role.MANAGER,
            ]
        )


class IsAdminManagerEngineer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [
                User.Role.SUPER_ADMIN,
                User.Role.ADMIN,
                User.Role.MANAGER,
                User.Role.ENGINEER,
            ]
        )