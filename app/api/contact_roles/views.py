from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.api.contact_roles.serializers import ContactRoleSerializer
from app.api.projects.models import Opportunity, ContactRole


class ContactRoleList(generics.ListAPIView):
    """
       List all snippets, or create a new snippet.
       """
    serializer_class = ContactRoleSerializer
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        project = get_object_or_404(Opportunity, id=self.kwargs['project_id'])
        return ContactRole.objects.filter(opportunity_id=project.oppid)

    def list(self, request, *args, **kwargs):
        project = get_object_or_404(Opportunity, id=self.kwargs['project_id'])
        data = ContactRole.objects.get_contactroles_by_project_id(project.oppid, self.request.user.id, project.id) \
            .values('id', 'contact_role_id', 'contact_id', 'company_id', 'name', 'email', 'phone', 'title',
                    'user_project_activities', 'user_total_system_activities', 'last_date')
        return Response(data)


