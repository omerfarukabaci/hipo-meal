from rest_framework.permissions import IsAuthenticated

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsOwner(IsAuthenticated):
    message = 'Permission denied.'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return obj == request.user
