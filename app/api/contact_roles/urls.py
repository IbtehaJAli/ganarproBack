from django.urls import path

from app.api.contact_roles.views import ContactRoleList

app_name = 'contact-role'
urlpatterns = [
    path('', ContactRoleList.as_view(), name='contact-role-list'),
]
