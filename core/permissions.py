from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IsOwner(IsAuthenticatedOrReadOnly):
    message = 'Permission denied.'
    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_object_permission(self, request, view, obj):
        return request.user == obj.author or request.method in self.SAFE_METHODS
