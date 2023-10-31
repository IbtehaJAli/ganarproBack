from django.template.defaulttags import url
from django.urls import path

from app.api.gc_planify.views import  GeneralContractorRetrieve, GeneralContractorRetrieveUpdate

urlpatterns = [
    path('company_info', GeneralContractorRetrieveUpdate.as_view(), name='general-contractor-retrieve-update'),
    # path('company_info', GeneralContractorRetrieve.as_view(),
    #      name='general-contractor-detail')
]
