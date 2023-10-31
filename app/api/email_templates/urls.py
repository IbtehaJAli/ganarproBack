from django.urls import path

from app.api.email_templates.views import EmailTemplateList, EmailTemplateDetail

app_name = 'email-template'
urlpatterns = [
    path('', EmailTemplateList.as_view(), name='template-list'),
    path('/<int:pk>', EmailTemplateDetail.as_view(), name='template-detail'),
]
