"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import environ

env = environ.Env()

schema_view = get_schema_view(
    openapi.Info(
        title="Etlas API",
        default_version='v1',
        description="Etlas API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=env('url'),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path("timeline/", include("timeline.urls")),
    path("tours/", include("tours.urls")),
    path("articles/", include("articles.urls")),
    path("questions/", include("knowledge_check.urls")),
    path("users/", include("users.urls")),
    path("auth/", include("authentication.urls")),
    path("social-auth/", include("social_auth.urls")),
    path("monuments/", include("monuments.urls")),
    path("favorites/", include("favorites.urls")),
    path("contact-us/", include("contact_us.urls")),
    path("user-payment/", include("user_payment.urls")),
]
