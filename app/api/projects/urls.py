from django.urls import path

from . import views
from .views import ProjectList, ProjectDetail, favorite, un_favorite, archive, un_archive, CompanyAccountList, \
    HotScopeList, ProjectsListTable, OpportunityListView

app_name = 'projects'
urlpatterns = [
    path('', ProjectList.as_view(), name='project-list'),
    path('/list', ProjectsListTable.as_view(), name="project-list-table"),
    path('/mapv2', OpportunityListView.as_view(), name='mapv2'),
    path('/companies', views.list_companies, name='company-list'),
    path('/hotscopes', HotScopeList.as_view(), name='hot-scope-list'),
    path('/<str:url_slug>', ProjectDetail.as_view(), name='project-detail'),
    path('/<int:pk>/favorite', favorite, name='favorite-project'),
    path('/<int:pk>/unfavorite', un_favorite, name='unfavorite-project'),
    path('/<int:pk>/favorite', favorite, name='favorite-project'),
    path('/<int:pk>/unfavorite', un_favorite, name='unfavorite-project'),
    path('/<int:pk>/archive', archive, name='archive-project'),
    path('/<str:ids>/unarchive', un_archive, name='unarchive-projet'),


]
