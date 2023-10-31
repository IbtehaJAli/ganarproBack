from django.urls import path
from .views import total_statements, CapabilityStatementCreateView, delete_statement, CapabilityStatementEditView

urlpatterns = [
    path('capability_statement_create', CapabilityStatementCreateView.as_view(), name='capability_statement_create'),
    path('capability_statement', CapabilityStatementEditView.as_view(), name='capability_statement'),
    path('get_total_statements', total_statements.as_view(), name='get_total_statements'),
    path('delete_statement', delete_statement.as_view(), name="delete_statement"),
]
