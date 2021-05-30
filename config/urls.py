"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from file.views import FileViewSet
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from network.views import NetworkViewSet
from socialaccount.views import SocialAccountViewSet
from contact.views import ContactViewSet
from story.views import StoryViewSet

from relationship.views import RelationshipViewSet
from notification.views import NotificationViewSet

# from user.views import ProfileViewSet
from file.views import FileViewSet
from user.views import ProfileViewSet
from like.views import LikeViewSet
from rest_framework_swagger.views import get_swagger_view

# schema_view = get_swagger_view(title="Social API")


"""
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Social API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="kayode.adechinan@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = DefaultRouter()
router.register("networks", NetworkViewSet)
router.register("social-accounts", SocialAccountViewSet)
router.register("contacts", ContactViewSet)
router.register("stories", StoryViewSet)
router.register("relationships", RelationshipViewSet)
router.register("notifications", NotificationViewSet)
router.register("users", ProfileViewSet)
router.register("files", FileViewSet)
"""
router = DefaultRouter()
router.register("files", FileViewSet)
router.register("stories", StoryViewSet, basename="stories")
router.register("networks", NetworkViewSet)
router.register("social-accounts", SocialAccountViewSet)
router.register("contacts", ContactViewSet)
router.register("relationships", RelationshipViewSet)
router.register("notifications", NotificationViewSet)
router.register("likes", LikeViewSet)
router.register("users", ProfileViewSet, basename="feed")


urlpatterns = [
    path("admin/", admin.site.urls),
    # path("pages/", include("page.urls")),
    # path("doc/", schema_view),
    # path(
    #    "doc/",
    #    schema_view.with_ui("swagger", cache_timeout=0),
    #    name="schema-swagger-ui",
    # ),
    path("api/v1/", include("user.urls")),
    path("api/v1/", include(router.urls)),
]


admin.site.site_header = "Eyeco Administration Portal"
admin.site.site_title = "Eyeco Administration Portal"
admin.site.index_title = "Eyeco Administration Portal"
admin.site.site_url = "/admin"
