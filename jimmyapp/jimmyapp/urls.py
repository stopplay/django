"""jimmyapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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

from rest_framework import routers
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from jimmyapp.views import hello_geek
from users import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'establishments', views.EstablishmentViewSet)
router.register(r'address', views.AddressViewSet)
router.register(r'order', views.OrderViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Jimmys API",
        default_version='v1',
        description="Api for testing integrations",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('geek/', hello_geek),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
