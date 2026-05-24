from django.urls import path , include
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
# urlpatterns = [
#     path("snippets/" , views.SnippetList.as_view() , name="snippet-list"),
#     path("snippets/<int:pk>/" , views.SnippetDetails.as_view(), name="snippet-detail"),
#     path("users/" , views.UserList.as_view(), name="user-list"),
#     path("users/<int:pk>/" , views.UserDetails.as_view(), name="user-detail"),
#     path("", views.api_root),
#     path("snippets/<int:pk>/highlight/", views.SnippetHighlight.as_view(), name="snippet-highlight"),
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)
# urlpatterns += [
#     path("api-auth/" , include("rest_framework.urls")),
# ]

"""
Using Routers¶
Because we're using ViewSet classes rather than View classes, we actually don't need to design the URL conf ourselves. The conventions for wiring up resources into views and urls can be handled automatically, using a Router class. All we need to do is register the appropriate view sets with a router, and let it do the rest.

"""

router = DefaultRouter()
router.register(r"snippets" , views.SnippetViewSet ,  basename="snippet")
router.register(r"users" , views.UserViewSet,  basename="user")

urlpatterns=[
    path("" , include(router.urls)),
]