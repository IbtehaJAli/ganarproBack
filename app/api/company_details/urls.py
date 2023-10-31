from django.urls import path
from .views import BasicCompanyDetailsCreateView, CompanyInfoCreateView, SocialsCreateView, OrgDetailsCreateView, \
    ProjectHistoryCreateView, CurrentWorkCreateView, CompletedWorkCreateView, InsuranceCreateView, SafetyCreateView, \
    FinanceCreateView, SupplierCreateView, LegalCreateView, ShippingReceivingsCreateView, UpdateCountView, ProjectTypesView

urlpatterns = [
    path('basic_company', BasicCompanyDetailsCreateView.as_view(), name='basic-company'),
    path('company_info', CompanyInfoCreateView.as_view(), name='company-info'),
    path('socials', SocialsCreateView.as_view(), name='socials'),
    path('org_details', OrgDetailsCreateView.as_view(), name='org-details'),
    path('project_history', ProjectHistoryCreateView.as_view(), name='project-history'),
    path('current_work', CurrentWorkCreateView.as_view(), name='current-work'),
    path('completed_work', CompletedWorkCreateView.as_view(), name='completed-work'),
    path('insurance', InsuranceCreateView.as_view(), name='insurance'),
    path('safety', SafetyCreateView.as_view(), name='safety'),
    path('finance', FinanceCreateView.as_view(), name='finance'),
    path('supplier', SupplierCreateView.as_view(), name='supplier'),
    path('legal', LegalCreateView.as_view(), name='legal'),
    path('shipping_receivings', ShippingReceivingsCreateView.as_view(), name='shipping-receivings'),
    path('update_count', UpdateCountView.as_view(), name='update-count'),
    path('project_types', ProjectTypesView.as_view(), name="project_types")
]
