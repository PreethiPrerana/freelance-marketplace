from rest_framework.permissions import BasePermission
class HasRole(BasePermission):
 allowed = ()
 def has_permission(self, request, view):
  return bool(request.user and request.user.is_authenticated and request.auth and request.auth.get("role") in self.allowed)
