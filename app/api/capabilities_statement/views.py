from django.shortcuts import render
from rest_framework import generics, status, views
from .serializers import capabilityStatementSerializer
from ..authentication.models.user_registration import UserProfile
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..users.permissions import IsOwner
from .models import capability_statement
from .helpers import upload_to_cloudinary


# Create your views here.
class CapabilityStatementCreateView(generics.CreateAPIView):
    serializer_class = capabilityStatementSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    allowed_methods = ['POST']

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')

        if capability_statement.objects.filter(user_id=user_id).count() == 5:
            return Response({'error': 'You can save only 5 Capability Statements'}, status=status.HTTP_200_OK)

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        upload_image(request.data, request.FILES.get('logo_image'), 'logo_image')
        upload_image(request.data, request.FILES.get('core_competencies_image'), 'core_competencies_image')
        upload_image(request.data, request.FILES.get('past_performance_image'), 'past_performance_image')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CapabilityStatementEditView(generics.RetrieveUpdateAPIView):
    serializer_class = capabilityStatementSerializer
    permission_classes = (IsAuthenticated, IsOwner)

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('userId')

        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

        upload_image(request.data, request.FILES.get('logo_image'), 'logo_image')
        upload_image(request.data, request.FILES.get('core_competencies_image'), 'core_competencies_image')
        upload_image(request.data, request.FILES.get('past_performance_image'), 'past_performance_image')

        try:
            capability_statement_info = capability_statement.objects.get(user_id=user_id,
                                                                         pdf_name=request.data['pdf_name'])
            serializer = self.get_serializer(capability_statement_info, data=request.data)
        except capability_statement.DoesNotExist:
            return Response({'error': 'Unable to find pdf'}, 500)

        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=user_id)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        pdf_name = request.query_params.get('pdf_name')
        try:
            capability_statement_info = capability_statement.objects.get(user_id=user_id, pdf_name=pdf_name)
            # Get the related UserProfile instance
            user_profile = capability_statement_info.user

            # Create a dictionary with the serializer data and the 'file_url' from UserProfile
            data = {
                **self.get_serializer(capability_statement_info).data,
                'logo_url': user_profile.file_url
            }
            return Response(data, status=status.HTTP_200_OK)
        except capability_statement.DoesNotExist:
            return Response({'error': 'Capability Statement not found for the specified userId.'},
                            status=status.HTTP_200_OK)


class total_statements(views.APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        try:
            capability_statement_info = capability_statement.objects.filter(user_id=user_id).values_list("pdf_name",
                                                                                                         flat=True)
            return Response({"pdfs": capability_statement_info}, status=status.HTTP_200_OK)
        except capability_statement.DoesNotExist:
            return Response({'error': 'Capability Statement not found for the specified userId.'},
                            status=status.HTTP_200_OK)


class delete_statement(views.APIView):
    permission_classes = (IsAuthenticated, IsOwner)

    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('userId')
        pdf_name = request.query_params.get('pdf_name')
        try:
            capability_statement_row = capability_statement.objects.filter(user_id=user_id, pdf_name=pdf_name)
            capability_statement_row.delete()
            return Response({"deleted": True, "message": "Pdf Deleted Successfully"}, status=status.HTTP_200_OK)
        except capability_statement.DoesNotExist:
            return Response({'error': 'Capability Statement not found'},
                            status=status.HTTP_200_OK)


def upload_image(data, image, key):
    if image:
        url = upload_to_cloudinary(image)
        if url:
            data[key] = url
        else:
            return Response({'error': f'Failed to upload {key}'}, 500)
