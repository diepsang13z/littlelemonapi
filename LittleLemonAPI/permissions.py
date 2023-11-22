from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.groups.name('Managers')
        isValid = role.exists()
        return isValid
        
        
class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        role = request.user.groups.name('Delivery crew')
        isValid = role.exists()
        return isValid