from django.urls import path

from . import views
from .views import RegionList, PlanRoomDetail

urlpatterns = [
    path("/regions", RegionList.as_view(), name="region-list"),
    path("/plan_rooms", views.create_plan_room, name="plan_room_create"),
    path('/pre_qualify_create', views.create_pre_qualify, name="pre_qualify")
]
