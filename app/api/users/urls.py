from django.urls import path


from app.api.users.views import UserList, UserDetail, update_free_mode_action, customer_portal

urlpatterns = [
    path('', UserList.as_view(), name='user-list'),
    path('/profile', UserDetail.as_view(), name='user-detail'),
    path('/free_mode_action', update_free_mode_action, name='user-detail'),
    path('/free_mode_action', update_free_mode_action, name='free_mode_action'),
    path('/create-customer-portal-session', customer_portal, name='customer_portal'),
]
