from collections import OrderedDict

from django.contrib.auth.models import AnonymousUser
from django.db.models import Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app.api.authentication.models.user_registration import UserProfile
from app.api.email_templates.models import EmailTemplate
from app.api.gcqualify.models import PlanRoom
# from simplejson import OrderedDict


from app.api.projects.helpers import get_project_board_filters, project_research_query
from app.api.projects.serializers import ProjectSerializer, CompanyAccountSerializer, HotScopeSerializer, \
    OpportunitySerializer
from app.api.projects.models import Opportunity, ContactRole, CompanyAccount, HotScope
from app.api.users.permissions import IsOwner


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_overdue(self, queryset, field_name, value):
        if value:
            return queryset.overdue()
        return queryset

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('building_types', data['filter_counts']['building_types']),
            ('phases', data['filter_counts']['statuses']),
            ('sizes', data['filter_counts']['sizes']),
            ('email_templates', data['email_templates']),
            ('results', data['projects']),
        ]))


class ProjectList(generics.ListAPIView):
    """
       List all snippets, or create a new snippet.
       """
    serializer_class = ProjectSerializer
    # permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        user = self.request.user
        if isinstance(user, AnonymousUser):
            user = None
        return Opportunity.objects.api_filter_by(self.request.query_params, user)

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        building_types, statuses, sizes = get_project_board_filters(self.get_queryset())
        filter_counts = {'building_types': building_types, 'statuses': statuses, 'sizes': sizes}
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        # Get email templates
        email_templates = EmailTemplate.objects.filter(type='PB') \
            .order_by('ordering').values('id', 'name')

        # Create a new dictionary to hold both the serialized data and the email templates
        # print(f"serializer.data {serializer.data}")
        response_data = {
            'projects': serializer.data,
            'email_templates': email_templates,
            'filter_counts': filter_counts
        }

        if page is not None:
            return self.get_paginated_response(response_data)

        return Response(response_data)


class TableResultsSetPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_overdue(self, queryset, field_name, value):
        if value:
            return queryset.overdue()
        return queryset

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
        ]))


class ProjectsListTable(ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = Opportunity.objects.all()
    pagination_class = TableResultsSetPagination
    allowed_method = ['GET']

    def get_queryset(self):
        query_params = self.request.query_params
        location_list = query_params.get("location")
        phase = query_params.get("phase")
        sort = query_params.get("sort")

        if location_list is not None:
            locations = location_list.split(",")
            location_query = Q()

            for location in locations:
                location_query |= Q(state__icontains=location.strip())

            query = Opportunity.objects.filter(location_query)
        else:
            query = Opportunity.objects.all()

        query = project_research_query(query)

        if phase == "all":
            query = query.filter(Q(status="NA") | Q(status="A"))
        elif phase == 'historical':
            query = query.filter(Q(status="NA"))
        else:
            query = query.filter(Q(status="A"))

        if sort is not None:
            query = query.order_by(sort)
        else:
            query = query.order_by('-last_modified_date')

        return query


class ProjectDetail(generics.RetrieveAPIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    lookup_field = 'url_slug'
    serializer_class = ProjectSerializer
    # permission_classes = (IsAuthenticated,)
    queryset = Opportunity.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_id = request.user.id
        serializer_data = serializer.data
        try:
            profile = request.user.profile
            if instance in profile.project_viewed.all():
                profile.project_viewed.remove(instance)
                profile.project_viewed.add(instance)
            else:
                profile.project_viewed.add(instance)

            if profile.project_viewed.count() > 30:
                first = profile.project_viewed.first()
                profile.project_viewed.remove(first)

        except AttributeError as ex:
            profile = None
        serializer_data['similar_projects'] = Opportunity.objects \
                                                  .get_similar_projects(serializer_data['state_short'],
                                                                        serializer_data['project_type'],
                                                                        instance.id, profile)[
                                              :5]
        serializer_data['email_templates'] = EmailTemplate.objects.filter(type='PB') \
            .order_by('ordering').values('id', 'name')

        return Response(serializer_data)


class CompanyAccountList(generics.ListAPIView):
    serializer_class = CompanyAccountSerializer

    def get_queryset(self):
        return CompanyAccount.objects.api_filter_by(self.request.query_params, self.request.profile)


@permission_classes((AllowAny,))
@authentication_classes((AllowAny,))
@api_view(['GET'])
def list_companies(request):
    try:
        profile = request.user.profile
    except AttributeError as ex:
        profile = None

    if request.query_params.get('plan_room'):
        companies = CompanyAccount.objects.api_filter_by(request.query_params, profile).values('id', 'name',
                                                                                               'planroom_link',
                                                                                               'prequalification_application',
                                                                                               'billing_city',
                                                                                               'billing_state',
                                                                                               'max_date_visited',
                                                                                               'max_note')
        return JsonResponse(list(companies), safe=False)

    companies = CompanyAccount.objects.api_filter_by(request.query_params, profile).values('id', 'name',
                                                                                           'planroom_link',
                                                                                           'prequalification_application',
                                                                                           'billing_city',
                                                                                           'billing_state', 'max_note',
                                                                                           'max_upload')
    return JsonResponse(list(companies), safe=False)


@api_view(["POST"])
def save_search(request):
    if request.method == "POST":
        user_id = request.data.get('userId')
        try:
            user = UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User does not exist for specified userId.'},
                            status=status.HTTP_404_NOT_FOUND)

    else:
        return Response("Invalid Request", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def favorite(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    if request.method == 'POST':
        instance = get_object_or_404(Opportunity, pk=pk)
        request.user.account.project_favorites.add(instance)
        message = "Project added to favorite list"
        return Response(message, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def un_favorite(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    if request.method == 'DELETE':
        instance = get_object_or_404(Opportunity, pk=pk)
        request.user.account.project_favorites.remove(instance)
        message = "Project removed from favorite list"
        return Response(message, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def archive(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    if request.method == 'POST':
        instance = get_object_or_404(Opportunity, pk=pk)
        request.user.account.project_archives.add(instance)
        message = "Project added to archive list"
        return Response(message, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def un_archive(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    if request.method == 'DELETE':
        instance = get_object_or_404(Opportunity, pk=pk)
        request.user.account.project_archives.remove(instance)
        message = "Project removed from archive list"
        return Response(message, status=status.HTTP_204_NO_CONTENT)


class HotScopeList(ListAPIView):
    """
       List all snippets, or create a new snippet.
       """
    serializer_class = HotScopeSerializer
    queryset = HotScope.objects.all()
    # permission_classes = (IsAuthenticated,)


@api_view(['POST'])
def favorite(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    if request.method == 'POST':
        instance = get_object_or_404(Opportunity, pk=pk)
        request.user.profile.project_favorites.add(instance)
        message = "Project added to favorite list"
        return Response(message, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def un_favorite(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    if request.method == 'DELETE':
        instance = get_object_or_404(Opportunity, pk=pk)
        request.user.profile.project_favorites.remove(instance)
        message = "Project removed from favorite list"
        return Response(message, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def archive(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    if request.method == 'POST':
        instance = get_object_or_404(Opportunity, pk=pk)
        request.user.profile.project_archives.add(instance)
        message = "Project added to archive list"
        return Response(message, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def un_archive(request, ids):
    """
    Retrieve, update or delete a code snippet.
    """
    if request.method == 'DELETE':
        # instance = get_object_or_404(Opportunity, pk=pk)
        request.user.profile.project_archives.remove(*Opportunity.objects.filter(id__in=ids.split(',')))
        message = "Project removed from archive list"
        return Response(message, status=status.HTTP_204_NO_CONTENT)


class OpportunityListView(APIView):

    def get(self, request):
        north = request.query_params.get('north')
        south = request.query_params.get('south')
        east = request.query_params.get('east')
        west = request.query_params.get('west')

        if north and south and east and west:
            print('here1')
            opportunities = Opportunity.objects.filter(
                latitude__lte=north,
                latitude__gte=south,
                longitude__lte=east,
                longitude__gte=west
            )[:5]
        else:
            print('here')
            opportunities = Opportunity.objects.all()[:5]

        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
