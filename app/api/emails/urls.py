from django.urls import path

from app.api.emails.views import SendEmailList, CheckAvailabilityEmail

app_name = 'email'
urlpatterns = [
    path('emails', SendEmailList.as_view(), name='email-list'),
    path('check-availability', CheckAvailabilityEmail.as_view(), name='check-availability'),
]
