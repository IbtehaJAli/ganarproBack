from django.urls import path

from . import views
from .views import ProposalListCreateAPI, ProposalDetail

urlpatterns = [
    path("", ProposalListCreateAPI.as_view(), name="proposal-list-create"),
    path("/<int:pk>", ProposalDetail.as_view(), name="proposal-detail"),
    path("/download/<int:pk>",  views.proposal_download, name="proposal-download"),
    path("/subscription", views.subscriptions, name="proposal-subscriptions"),

]
