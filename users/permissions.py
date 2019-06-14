from rest_framework.permissions import IsAuthenticated

class IsOwner(IsAuthenticated):
    message = 'Permission denied.'

    def has_object_permission(self, request, view, obj):
        return obj == request.user
