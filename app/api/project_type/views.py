from django.http import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.api.project_type.models import ProjectType
from app.api.project_type.serializers import ProjectTypeSerializer
from app.api.users.permissions import IsOwner


# Create your views here.

class ProjectTypeListCreateAPI(generics.ListCreateAPIView):
    serializer_class = ProjectTypeSerializer

    def get_queryset(self):
        return ProjectType.objects.order_by('name')

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        # serializer.context["user_id"] = request.user.id
        if serializer.is_valid(raise_exception=True):
            # create_proposal_template(request.data)
            request.user.profile.free_template_count = request.user.profile.free_template_count - 1
            request.user.profile.save()
            serializer.save(user=request.user)
            return_message = {
                "message": "Proposal created successfully",
                "data": serializer.data,
            }

            return Response(return_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    serializer_class = ProjectTypeSerializer
    queryset = ProjectType.objects.all()

    def get_object(self, pk):
        try:
             if isinstance(pk, int):
                return  ProjectType.objects.get(pk=pk)
             else:
                 return ProjectType.objects.get(name=pk)
        except ProjectType.DoesNotExist:
            try:
                return ProjectType.objects.get(name='Any Type General Cleaning')
            except:
                 raise Http404

    def get(self, request, pk, format=None):
        proposal = self.get_object(pk)
        serializer = ProjectTypeSerializer(proposal)
        return Response(serializer.data)

