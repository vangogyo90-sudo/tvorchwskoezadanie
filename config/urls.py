"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from cats.views import CatViewSet
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)
from health.views import (ClinicViewSet, DoctorViewSet, HealthPassportViewSet,
                          HealthRecordViewSet, VaccineViewSet, VaccineAdministrationViewSet)
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("cats", CatViewSet, basename="cats")
router.register("health-passports", HealthPassportViewSet, basename="health-passports")
router.register("health-records", HealthRecordViewSet, basename="health-records")
router.register("clinics", ClinicViewSet, basename="clinics")
router.register("doctors", DoctorViewSet, basename="doctors")
router.register("vaccines", VaccineViewSet, basename="vaccines")
router.register("vaccine-administrations", VaccineAdministrationViewSet, basename="vaccine-administrations")

urlpatterns = [
    path('admin/', admin.site.urls),
    # Simple dashboard alias used by templates
    path('dashboard/', __import__("cats.views", fromlist=["feed"]).feed, name='dashboard'),
    # Top-level frontend routes (non-namespaced) used by templates
    path('', __import__("cats.views", fromlist=["feed"]).feed, name='feed'),
    path('cats/', __import__("cats.views", fromlist=["feed"]).feed, name='cats-list'),
    path('cats/add/', __import__("cats.views", fromlist=["add_cat"]).add_cat, name='add-cat'),
    path('cats/<int:pk>/', __import__("cats.views", fromlist=["cat_detail"]).cat_detail, name='cat-detail'),
    path("api/schema/", SpectacularAPIView.as_view(permission_classes=[AllowAny]), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema", permission_classes=[AllowAny]), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema", permission_classes=[AllowAny]), name="redoc"),
    path("api/", include(router.urls)),
    path("api/auth/", include("rest_framework.urls")),
    # Frontend pages
    path("", include(([
        path("", __import__("cats.views", fromlist=["feed"]).feed, name="feed"),
        path("cats/", __import__("cats.views", fromlist=["feed"]).feed, name="cats-list"),
        path("cats/add/", __import__("cats.views", fromlist=["add_cat"]).add_cat, name="add-cat"),
        path("cats/<int:pk>/", __import__("cats.views", fromlist=["cat_detail"]).cat_detail, name="cat-detail"),
    ], "cats"), namespace="cats")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
