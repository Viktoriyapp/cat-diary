from rest_framework.permissions import BasePermission


class CanViewAllMoodsPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm('moods.can_view_all_moods')