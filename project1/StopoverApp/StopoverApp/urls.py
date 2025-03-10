"""
URL configuration for StopoverApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stopover.views import (StopoverViewSet, create_stopover, get_stopover,
                            get_stopover_by_email, patch_stopover)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = DefaultRouter()
router.register(r'stopover-list', StopoverViewSet, basename='stopover-list')

schema_view = get_schema_view(
    openapi.Info(
        title="REST API",
        default_version='v1',
        description="API documentation for StopoverApp",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('create-stopover/', create_stopover, name='create_stopover'),
    path('get-stopover/<int:id>', get_stopover, name='get_stopover'),
    path('get-stopover/', get_stopover_by_email, name='get_stopover_by_email'),
    path('patch-stopover/<int:id>', patch_stopover, name='patch_stopover'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
