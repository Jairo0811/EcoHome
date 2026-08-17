from rest_framework.permissions import SAFE_METHODS, BasePermission


class SafeReadOnlyOrAdmin(BasePermission):
    """Allow anonymous reads while restricting mutations to staff users."""

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
