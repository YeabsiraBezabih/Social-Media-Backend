from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Django Social Media API", # Customize your API title
      default_version='v1',
      description="API documentation for the Django Social Media App Capstone Project", # Customize description
      terms_of_service="https://www.example.com/terms/", # Optional terms of service URL
      contact=openapi.Contact(email="contact@example.com"), # Optional contact email
      license=openapi.License(name="MIT License"), # Optional license information
   ),
   public=True,
   permission_classes=(permissions.AllowAny,), # Set permission to AllowAny for public documentation
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),

    # Swagger Documentation URLs:
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'), # OpenAPI schema as JSON/YAML
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # Redoc UI
]