
from rest_framework.permissions import BasePermission


class SomePermission(BasePermission):
    """
    We can override permissions like this to define permissions and then use them in permission
    classes of a view.
    """
    def has_permission(self, request, view):
        return True
