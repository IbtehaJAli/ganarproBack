from datetime import timezone, datetime

from django.core.mail import EmailMessage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, status
import cloudinary.uploader
from app.api.gcqualify.models import UserRegions, PlanRoom, PreQualify
from app.api.gcqualify.serializers import RegionsSerializer, PlanRoomSerializer


class RegionList(generics.ListAPIView):
    serializer_class = RegionsSerializer

    def get_queryset(self):
        return UserRegions.objects.order_by('name')


class PlanRoomDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlanRoomSerializer

    def get_object(self, pk):
        return PlanRoom.objects.get(pk=pk)

    def post(self, request, *args, **kwargs):
        plan_room = self.get_object(self.kwargs.get('pk'))
        serializer = PlanRoomSerializer(plan_room, data=request.data, partial=True)
        # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response("", status=status.HTTP_201_CREATED)
        return Response("message", status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_plan_room(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        company_account_id = request.data.get('company_account_id')
        note = request.data.get('note')
        region = request.data.get('region')
        prequal_id = request.data.get('prequal_id')
        date_visited = request.data.get('date_visited')
        flag = request.data.get('flag')

        if date_visited:
            date_visited = datetime.strptime(date_visited, '%Y-%m-%dT%H:%M:%S.%fZ')
            date_visited.replace(tzinfo=timezone.utc)
            # began_application_process = timezone.now().replace(minute=0, second=0, microsecond=0)
            defaults = {"date_visited": date_visited}

            obj, created = PlanRoom.objects.update_or_create(company_account_id=company_account_id,
                                                             user_profile=user_profile, defaults=defaults)
            return Response("message", status=status.HTTP_201_CREATED)
        elif note:
            defaults = {"note": note}

            obj, created = PlanRoom.objects.update_or_create(company_account_id=company_account_id,
                                                             user_profile=user_profile, defaults=defaults)
            return Response('message', status=status.HTTP_201_CREATED)

        elif flag:
            company_name = request.data.get('company_account_name')
            email = request.user.email
            full_name = f"{request.user.profile.first_name} {request.user.profile.last_name}"
            body = f"""This User: {full_name} with email {email} flagged this company Plan room link as broken
                    """
            email = EmailMessage(
                f"{company_name} Plan room link is broken, pls fix",
                body,
                from_email=f'support@ganarpro.com',
                to=[email],
            )
            email.send()
            return Response('message', status=status.HTTP_200_OK)


@api_view(['POST'])
def create_pre_qualify(request):
    if request.method == 'POST':
        user_profile = request.user.profile
        company_account_id = request.data.get('company_account_id')
        note = request.data.get('note')
        upload = request.FILES.get('upload')

        if note:
            defaults = {"note": note}

            obj, created = PreQualify.objects.update_or_create(company_account_id=company_account_id,
                                                               user_profile=user_profile, defaults=defaults)
            return Response('message', status=status.HTTP_201_CREATED)
        elif upload:
            cloudinary_upload = cloudinary.uploader.upload(upload, public_id=upload.name)
            defaults = {"upload": cloudinary_upload['secure_url']}
            obj, created = PreQualify.objects.update_or_create(company_account_id=company_account_id,
                                                               user_profile=user_profile, defaults=defaults)
            return Response('message', status=status.HTTP_201_CREATED)
