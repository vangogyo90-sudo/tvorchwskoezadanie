from django.urls import path

from . import views


urlpatterns = [
    path("register/", views.register, name="register"),
    path("", views.dashboard, name="dashboard"),
    path("owner/", views.owner_dashboard, name="owner-dashboard"),
    path("vet/", views.vet_dashboard, name="vet-dashboard"),
    path("admin-panel/", views.admin_dashboard, name="admin-dashboard"),
]
