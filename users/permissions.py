from rest_framework import permissions


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.groups.filter(name="Moderators").exists():
            return True
        return False


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
