from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsOwner(IsAuthenticatedOrReadOnly):
    message = 'Permission denied.'
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in self.SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user == obj.author
        )
