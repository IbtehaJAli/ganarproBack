from django.urls import path

from .views import BidAmountPricingModelDetail, StateLaborPricingModelDetail, StateLaborPricingModelListCreateAPI, \
    BidAmountPricingModelListCreateAPI, CleanUPEstimateListCreateAPI, CleanUPEstimateDetail, get_calculation_info

urlpatterns = [
    path("/bidamount_pricing/<str:project_type>", BidAmountPricingModelDetail.as_view(), name="bid-amount-pricing"),
    path("/bidamount_pricing", BidAmountPricingModelListCreateAPI.as_view(), name="bid-amount-pricing-list"),
    path("/state_labor_pricing/<str:state>", StateLaborPricingModelDetail.as_view(), name="state_labor_pricing"),
    path("/state_labor_pricing", StateLaborPricingModelListCreateAPI.as_view(), name="state_labor_pricing_list"),
    path("/cleanup_estimates", CleanUPEstimateListCreateAPI.as_view(), name="estimates-list-create"),
    path("/cleanup_estimates/<int:pk>", CleanUPEstimateDetail.as_view(), name="estimates-detail"),
    path('/calculation_info', get_calculation_info, name="calculation_info")
]
