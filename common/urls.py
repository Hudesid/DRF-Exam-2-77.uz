from django.urls import path
from .views import StaticPageRetrieveAPIView, RegionListAPIView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="77.uz",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('common/regions-with-districts/', RegionListAPIView.as_view(), name='region_list'),
    path('common/pages/<slug:slug>/', StaticPageRetrieveAPIView.as_view(), name='common_detail'),
    path('swagger/', schema_view.as_view(), name='swagger-docs'),
]