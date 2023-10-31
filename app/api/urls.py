from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt import views as jwt_views
from app.api.authentication.views import EmailTokenObtainPairView
from app.api.emails.views import send_verification_email
from app.api.users.views import UserRegistrationView, customer_portal, stripe_webhook

schema_view_ = get_schema_view(
    openapi.Info(
        title="CleanUp API",
        default_version="v1",
        description="Official documentation for the CleanUp API.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
swagger_ui_view = get_swagger_view()

urlpatterns = [
    re_path(
        r"^docs/$",
        schema_view_.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^docs(?P<format>\.json|\.yaml)$",
        schema_view_.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^redoc/$", schema_view_.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("users", include(("app.api.users.urls", "authentication"), namespace="authentication")),
    path("register", UserRegistrationView.as_view(), name='register'),
    path('company_details/', include(("app.api.company_details.urls", "company_details"), namespace="company_details")),
    path('statements/', include(("app.api.capabilities_statement.urls", "capability_statement"), namespace="capability_statement")),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login', EmailTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path(r'password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path("proposals", include(("app.api.proposal.urls", "proposal"), namespace="proposal")),
    path("project-types", include(("app.api.project_type.urls", "project_types"), namespace="project_types")),
    path("mortgage_calculator", include(("app.api.mortgage_calculator.urls", "mortgage_calculator"),
                                        namespace="mortgage_calculator")),
    path("gc_qualify", include(("app.api.gcqualify.urls", "gc_qualify"),
                               namespace="gc_qualify")),
    path("projects", include(("app.api.projects.urls", "projects"),
                             namespace="projects")),
    path('project/<int:project_id>/contact-roles', include('app.api.contact_roles.urls')),
    path('stripe_webhook', stripe_webhook),
    path('email-templates', include('app.api.email_templates.urls')),
    path('project/<int:project_id>/', include('app.api.emails.urls')),
    path('emails/domain-verification', send_verification_email, name='email-verification'),
    path('gcplanify/', include(("app.api.gc_planify.urls", "gc_planify"),
                               namespace="gc_planify")),
]
