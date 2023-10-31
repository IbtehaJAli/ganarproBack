from django.urls import path

from .views import ProjectTypeListCreateAPI, ProjectTypeDetail

urlpatterns = [
    path("", ProjectTypeListCreateAPI.as_view(), name="project_type-list-create"),
    path("/<str:pk>", ProjectTypeDetail.as_view(), name="project_type-detail"),
]
