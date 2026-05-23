from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    custom permission to allow only owners of an object to edit it"""
    
    def has_object_permission(self, request, view, obj):
    # read permissions are allowd to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #write permissions are only allowed to the owner of snippet this lower code checks the owner from db with the user from request and returns true if correct
        return obj.owner == request.user
    

"""
def has_object_permission(self, request, view, obj):

DRF automatically calls this when accessing a specific object.

Arguments:

request → current request (GET, PUT, authenticated user, etc.)
view → current view class
obj → actual database object being accessed



SAFE_METHODS is built into DRF.

Contains:

('GET', 'HEAD', 'OPTIONS')
"""