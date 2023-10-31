from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from app.api.authentication.views import EmailTokenObtainPairView
from app.api.users.views import UserRegistrationView
