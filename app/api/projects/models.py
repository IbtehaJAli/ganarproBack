import datetime
import json
import re
from time import timezone

from django.apps import apps
from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.postgres.search import SearchVector
from django.db.models.functions import Coalesce
from django.utils import timezone
# Create your models here.
from django.db.models import Max, Q, F, Count, OuterRef, Subquery
# from app.api.authentication.models.user_registration import User

from app.api.models import TimestampedModel


class OpportunityManager(models.Manager):
    def filter_by(self, **kwargs):
        qs = self.get_queryset()

        account = kwargs.get('account', None)
        if account:
            if account.usersprojects:
                qs = qs.exclude(id__in=account.usersprojects.archive_projects())

        created_start_date = kwargs.get('created_start_date', 0)
        created_end_date = kwargs.get('created_end_date', 0)
        updated_start_date = kwargs.get('updated_start_date', 0)
        updated_end_date = kwargs.get('updated_end_date', 0)
        bid_due_start_date = kwargs.get('bid_due_start_date', 0)
        bid_due_end_date = kwargs.get('bid_due_end_date', 0)
        completion_start_date = kwargs.get('completion_start_date', 0)
        completion_end_date = kwargs.get('completion_end_date', 0)
        project_name_or_city = kwargs.get('project_name_or_city', None)
        state = kwargs.get('state', None)
        size = kwargs.get('size', None)
        project_type = kwargs.get('project_type', None)
        status = kwargs.get('status', None)
        drawings = kwargs.get('drawings', None)
        wage = kwargs.get('wage', None)
        union = kwargs.get('union', None)
        suggestion = kwargs.get('suggestion', None)
        coordinates = kwargs.get('coordinates', None)
        created_date = kwargs.get('created_date', 0)
        updated_date = kwargs.get('updated_date', 0)
        precons_date = kwargs.get('precons_date', 0)
        show_filter = kwargs.get('show_filter', None)
        est_date = kwargs.get('est_date', 0)
        less_today = timezone.now().replace(hour=23, minute=59, second=59)
        today = timezone.now().replace(hour=0, minute=0, second=0)
        if status != 'A':
            qs = qs.filter(status='A')
        elif status == 'NA':
            qs = qs.filter(status='NA')

        if created_date:
            if created_date == "custom":
                if created_start_date and created_end_date:
                    qs = qs.filter(created_date__gte=created_start_date, created_date__lte=created_end_date,
                                   created_date__isnull=False)
            else:
                if created_date == "0":
                    qs = qs.filter(created_date__gte=timezone.now().replace(hour=0, minute=0, second=0),
                                   created_date__lte=timezone.now().replace(hour=23, minute=59, second=59),
                                   created_date__isnull=False)
                else:
                    days_ago = today - datetime.timedelta(days=int(created_date))
                    qs = qs.filter(created_date__gte=days_ago, created_date__lte=less_today)

        if updated_date and updated_date != "None":
            if updated_date == "custom":
                if updated_start_date and updated_end_date:
                    qs = qs.filter(last_modified_date__gte=updated_start_date, last_modified_date__lte=updated_end_date,
                                   last_modified_date__isnull=False)
            else:
                if updated_date == "0":
                    qs = qs.filter(last_modified_date__gte=timezone.now().replace(hour=0, minute=0, second=0),
                                   last_modified_date__lte=timezone.now().replace(hour=23, minute=59, second=59),
                                   last_modified_date__isnull=False)
                else:
                    days_ago = timezone.now() - datetime.timedelta(days=int(updated_date))
                    qs = qs.filter(last_modified_date__gte=days_ago, last_modified_date__lte=today,
                                   last_modified_date__isnull=False)

        if precons_date:
            if '+' in precons_date:
                precons_date = precons_date.replace("+", "")
                days_later = timezone.now() + datetime.timedelta(days=int(precons_date))
                qs = qs.filter(bid_due_date__gte=today, bid_due_date__lte=days_later, bid_due_date__isnull=False)
            elif precons_date == '0':
                qs = qs.filter(bid_due_date__gte=timezone.now().replace(hour=0, minute=0, second=0),
                               bid_due_date__lte=timezone.now().replace(hour=23, minute=59, second=59),
                               bid_due_date__isnull=False)
            elif precons_date == "custom":
                if bid_due_start_date and bid_due_end_date:
                    qs = qs.filter(bid_due_date__gte=bid_due_start_date, bid_due_date__lte=bid_due_end_date,
                                   bid_due_date__isnull=False)
            else:
                precons_date = precons_date.replace("-", "")
                days_ago = timezone.now() - datetime.timedelta(days=int(precons_date))
                qs = qs.filter(bid_due_date__gte=days_ago, bid_due_date__lte=today, bid_due_date__isnull=False)

        if est_date:
            if '+' in est_date:
                est_date = est_date.replace("+", "")
                days_later = timezone.now() + datetime.timedelta(days=int(est_date))
                qs = qs.filter(project_completion__gte=today, project_completion__lte=days_later,
                               project_completion__isnull=False)
            elif est_date == '0':
                qs = qs.filter(project_completion__gte=timezone.now().replace(hour=0, minute=0, second=0),
                               project_completion__lte=timezone.now().replace(hour=23, minute=59, second=59),
                               project_completion__isnull=False)
            elif est_date == "custom":
                if completion_start_date and completion_end_date:
                    qs = qs.filter(project_completion__gte=completion_start_date,
                                   project_completion__lte=completion_end_date, project_completion__isnull=False)
            else:
                est_date = est_date.replace("-", "")
                days_ago = timezone.now() - datetime.timedelta(days=int(est_date))
                qs = qs.filter(project_completion__gte=days_ago, project_completion__lte=today,
                               project_completion__isnull=False)

        if created_start_date and created_end_date:
            qs = qs.filter(created_date__gte=created_start_date, created_date__lte=created_end_date)
        elif created_start_date:
            qs = qs.filter(created_date__gte=created_start_date)
        elif created_end_date:
            qs = qs.filter(created_date__lte=created_end_date)

        if updated_start_date and updated_end_date:
            qs = qs.filter(last_modified_date__gte=updated_start_date, last_modified_date__lte=updated_end_date)
        elif updated_start_date:
            qs = qs.filter(last_modified_date__gte=updated_start_date)
        elif updated_end_date:
            qs = qs.filter(last_modified_date__lte=updated_end_date)

        if bid_due_start_date and bid_due_end_date:
            qs = qs.filter(bid_due_date__gte=bid_due_start_date, bid_due_date__lte=bid_due_end_date)
        elif bid_due_start_date:
            qs = qs.filter(bid_due_date__gte=bid_due_start_date)
        elif bid_due_end_date:
            qs = qs.filter(bid_due_date__lte=bid_due_end_date)

        if completion_start_date and completion_end_date:
            qs = qs.filter(project_completion__gte=completion_start_date, project_completion__lte=completion_end_date)
        elif completion_start_date:
            qs = qs.filter(project_completion__gte=completion_start_date)
        elif completion_end_date:
            qs = qs.filter(project_completion__lte=completion_end_date)

        if project_name_or_city:
            text = project_name_or_city
            text_arr = text.split(',')
            text_search = f" {text_arr[1]}" if len(text_arr) > 1 else text
            if len(text_arr) > 1:
                qs = qs.annotate(
                    search=SearchVector(
                        "city",
                        "state_short",
                        "state"
                    )
                ).filter(Q(search=text_arr[0]) | Q(search=text_arr[1]))
            else:
                qs = qs.annotate(
                    search=SearchVector(
                        "city",
                        "state_short",
                        "state"
                    )
                ).filter(search=text_search)

        if state:
            qs = qs.filter(state_short__iexact=state)

        if size:
            if size == "blank":
                qs = qs.filter(Q(sf_size=0) | Q(sf_size=None))
            elif size == "underTen":
                qs = qs.filter(sf_size__lte=10000).exclude(sf_size=0)
            elif size == "btw10And30":
                qs = qs.filter(sf_size__gte=10000, sf_size__lte=30000)
            elif size == "btw30And60":
                qs = qs.filter(sf_size__gte=30000, sf_size__lte=60000)
            elif size == "btw60And100":
                qs = qs.filter(sf_size__gte=60000, sf_size__lte=100000)
            elif size == "btw100And200":
                qs = qs.filter(sf_size__gte=100000, sf_size__lte=200000)
            elif size == "200AndAbove":
                qs = qs.filter(sf_size__gte=200000)

        if project_type:
            qs = qs.filter(project_type__icontains=project_type)

        if show_filter:
            if show_filter == 'hot_projects':
                days_ago = timezone.now() - datetime.timedelta(days=14)
                qs = qs.filter(last_modified_date__gte=days_ago, last_modified_date__lte=today,
                               project_quality_tier='PQ1', status='A').exclude(contact_roles__isnull=True)
        if status:
            days_ago_14 = less_today - datetime.timedelta(days=14)
            days_later_14 = less_today + datetime.timedelta(days=14)
            days_ago_30 = less_today - datetime.timedelta(days=30)
            days_later_30 = less_today + datetime.timedelta(days=30)
            if status == 'Bidding all trades':
                qs = qs.filter(Q(bid_due_date__gt=days_ago_14) & Q(bid_due_date__lte=days_later_14) |
                               Q(est_break_ground_date__gt=days_ago_30) & Q(est_break_ground_date__lte=days_later_30),
                               status='A')

            if status == "Work in progress":
                qs = qs.filter(Q(est_break_ground_date__lt=days_later_30)
                               | Q(project_completion__gt=days_later_30),
                               Q(status='A')
                               )

            elif status == "Cleanup and closeout":
                qs = qs.filter(stage_name__icontains="90% contracts purchased")

        if drawings:
            qs = qs.exclude(plan_drawings__isnull=True).exclude(plan_drawings__exact='None')

        if wage:
            qs = qs.exclude(davis_bacon_prevailing_wage_detail__isnull=True).exclude(
                davis_bacon_prevailing_wage_detail__exact='None')

        if union:
            qs = qs.exclude(laborer_union=False)

        if suggestion:
            qs = qs.filter(sf_size__isnull=False).exclude(sf_size=0)

        if coordinates:
            latitude, longitude = coordinates.split(',')
            qs = qs.filter(longitude=longitude, latitude=latitude)

        return qs.order_by('-last_modified_date')

    def moving_activities(self, **kwargs):
        qs = self.get_queryset()

        account = kwargs.get('account', None)
        if account:
            if account.usersprojects:
                qs = qs.exclude(id__in=account.usersprojects.archive_projects())

        project_name_or_city = kwargs.get('project_name_or_city', None)
        state = kwargs.get('state', None)
        size = kwargs.get('size', None)
        project_type = kwargs.get('project_type', None)
        status = kwargs.get('status', None)
        drawings = kwargs.get('drawings', None)
        wage = kwargs.get('wage', None)
        union = kwargs.get('union', None)
        suggestion = kwargs.get('suggestion', None)
        coordinates = kwargs.get('coordinates', None)
        show_filter = kwargs.get('show_filter', None)
        less_today = timezone.now().replace(hour=23, minute=59, second=59)
        today = timezone.now().replace(hour=0, minute=0, second=0)

        if project_name_or_city:
            text = project_name_or_city
            text_arr = text.split(',')
            text_search = f" {text_arr[1]}" if len(text_arr) > 1 else text
            if len(text_arr) > 1:
                qs = qs.annotate(
                    search=SearchVector(
                        "city",
                        "state_short",
                        "state"
                    )
                ).filter(Q(search=text_arr[0]) | Q(search=text_arr[1]))
            else:
                qs = qs.annotate(
                    search=SearchVector(
                        "city",
                        "state_short",
                        "state"
                    )
                ).filter(search=text_search)

        if state:
            qs = qs.filter(state_short__iexact=state)

        if size:
            if size == "blank":
                qs = qs.filter(Q(sf_size=0) | Q(sf_size=None))
            elif size == "underTen":
                qs = qs.filter(sf_size__lte=10000).exclude(sf_size=0)
            elif size == "btw10And30":
                qs = qs.filter(sf_size__gte=10000, sf_size__lte=30000)
            elif size == "btw30And60":
                qs = qs.filter(sf_size__gte=30000, sf_size__lte=60000)
            elif size == "btw60And100":
                qs = qs.filter(sf_size__gte=60000, sf_size__lte=100000)
            elif size == "btw100And200":
                qs = qs.filter(sf_size__gte=100000, sf_size__lte=200000)
            elif size == "200AndAbove":
                qs = qs.filter(sf_size__gte=200000)

        if project_type:
            qs = qs.filter(project_type__icontains=project_type)

        if show_filter:
            if show_filter == 'hot_projects':
                days_ago = timezone.now() - datetime.timedelta(days=14)
                qs = qs.filter(last_modified_date__gte=days_ago, last_modified_date__lte=today,
                               project_quality_tier='PQ1', status='A').exclude(contact_roles__isnull=True)
        if status:
            days_ago_14 = less_today - datetime.timedelta(days=14)
            days_later_14 = less_today + datetime.timedelta(days=14)
            days_ago_30 = less_today - datetime.timedelta(days=30)
            days_later_30 = less_today + datetime.timedelta(days=30)
            if status == 'Bidding all trades':
                qs = qs.filter(Q(bid_due_date__gt=days_ago_14) & Q(bid_due_date__lte=days_later_14) |
                               Q(est_break_ground_date__gt=days_ago_30) & Q(est_break_ground_date__lte=days_later_30),
                               status='A')

            if status == "Work in progress":
                qs = qs.filter(Q(est_break_ground_date__lt=days_later_30)
                               | Q(project_completion__gt=days_later_30),
                               Q(status='A')
                               )

            elif status == "Cleanup and closeout":
                qs = qs.filter(stage_name__icontains="90% contracts purchased")

        if drawings:
            qs = qs.exclude(plan_drawings__isnull=True).exclude(plan_drawings__exact='None')

        if wage:
            qs = qs.exclude(davis_bacon_prevailing_wage_detail__isnull=True).exclude(
                davis_bacon_prevailing_wage_detail__exact='None')

        if union:
            qs = qs.exclude(laborer_union=False)

        if suggestion:
            qs = qs.filter(sf_size__isnull=False).exclude(sf_size=0)

        if coordinates:
            latitude, longitude = coordinates.split(',')
            qs = qs.filter(longitude=longitude, latitude=latitude)

        return qs

    def api_filter_by(self, kwargs, user):
        qs = self.get_queryset()
        if user is not None and user.profile:
            UserEmail = apps.get_model('emails', 'UserEmail')  # Replace 'app_name' with the name of your app

            # Subquery to get the count of emails sent per opportunity
            email_count_subquery = (
                UserEmail.objects.filter(
                    opportunity=OuterRef('pk'),
                    user=user  # Filtering by user
                )
                .values('opportunity')
                .annotate(email_count=Count('id'))
                .values('email_count')[:1]
            )


            # Subquery to get the date of the last email sent per opportunity
            last_email_subquery = (
                UserEmail.objects.filter(
                    opportunity=OuterRef('pk'),
                    user=user  # Filtering by user
                )
                .order_by('-time_sent')
                .values('time_sent')[:1]
            )

            qs = (
                qs.annotate(
                    # no_of_contacts=Count('contact_roles__id', distinct=True),
                    no_of_email_sent=Coalesce(Subquery(email_count_subquery), 0),
                    # last_email_sent=Subquery(last_email_subquery)
                )
            )
        # print(f"QUERY {qs.query}")
        qs = qs.annotate(no_of_contacts=Count('contact_roles__id', distinct=True))

        created_start_date = kwargs.get('created_start_date', None)
        created_end_date = kwargs.get('created_end_date', None)
        updated_start_date = kwargs.get('updated_start_date', None)
        updated_end_date = kwargs.get('updated_end_date', None)
        bid_due_start_date = kwargs.get('bid_due_start_date', None)
        bid_due_end_date = kwargs.get('bid_due_end_date', None)
        completion_start_date = kwargs.get('completion_start_date', None)
        completion_end_date = kwargs.get('completion_end_date', None)
        project_name_or_city = kwargs.get('project_name_or_city', None)
        state = kwargs.get('state', None)
        size = kwargs.get('size', None)
        sizes = kwargs.get('sizes', None)
        project_types = kwargs.get('project_types', None)
        status = kwargs.get('status', None)
        drawings = kwargs.get('drawings', None)
        wage = kwargs.get('wage', None)
        union = kwargs.get('union', None)
        suggestion = kwargs.get('suggestion', None)
        sort = kwargs.get('sort', None)
        phases = kwargs.get('phases', None)
        building_types = kwargs.get('building_types', None)
        coordinates = kwargs.get('coordinates', None)
        user_location = kwargs.get('user_location', None)

        if phases == "Historical":
            qs = qs.filter(Q(status="NA") | Q(status="A"))
        else:
            qs = qs.filter(status="A")
        if created_start_date and created_end_date:
            qs = qs.filter(created_date__gte=created_start_date, created_date__lte=created_end_date)
        elif created_start_date:
            qs = qs.filter(created_date__gte=created_start_date)
        elif created_end_date:
            qs = qs.filter(created_date__lte=created_end_date)

        if updated_start_date and updated_end_date:
            qs = qs.filter(last_modified_date__gte=updated_start_date, last_modified_date__lte=updated_end_date)
        elif updated_start_date:
            qs = qs.filter(last_modified_date__gte=updated_start_date)
        elif updated_end_date:
            qs = qs.filter(last_modified_date__lte=updated_end_date)

        if bid_due_start_date and bid_due_end_date:
            qs = qs.filter(bid_due_date__gte=bid_due_start_date, bid_due_date__lte=bid_due_end_date)
        elif bid_due_start_date:
            qs = qs.filter(bid_due_date__gte=bid_due_start_date)
        elif bid_due_end_date:
            qs = qs.filter(bid_due_date__lte=bid_due_end_date)

        if completion_start_date and completion_end_date:
            qs = qs.filter(project_completion__gte=completion_start_date, project_completion__lte=completion_end_date)
        elif completion_start_date:
            qs = qs.filter(project_completion__gte=completion_start_date)
        elif completion_end_date:
            qs = qs.filter(project_completion__lte=completion_end_date)

        if project_name_or_city:
            text = project_name_or_city
            qs = qs.annotate(
                search=SearchVector(
                    "name",
                    "city",
                    "state_short",
                    "state",
                    "description",
                    "project_type",
                    "status_update_1",
                    "status_update_2",
                    "status_update_3",
                    "status_update_4",
                    "hot_lead_trade_scope",
                )
            ).filter(search=text)

        if state:
            qs = qs.filter(state_short__iexact=state)

        if size:
            if size == "blank":
                qs = qs.filter(Q(sf_size=0) | Q(sf_size=None))
            elif size == "extra_small":
                qs = qs.filter(sf_size__gte=1, sf_size__lte=4000, status='A')
            elif size == "small":
                qs = qs.filter(sf_size__gt=4000, sf_size__lte=31000, status='A')
            elif size == "medium":
                qs = qs.filter(sf_size__gt=31000, sf_size__lte=150000, status='A')
            elif size == "large":
                qs = qs.filter(sf_size__gte=150000, sf_size__lte=500000, status='A')
            elif size == "extra_large":
                qs = qs.filter(sf_size__gt=500000, sf_size__lte=3800000, status='A')

        if sizes not in (None, ''):
            or_query = Q()

            for size in sizes.split(','):
                if size == "blank":
                    or_query = Q(sf_size=0) | Q(sf_size=None)
                elif size == "underTen":
                    or_query |= Q(sf_size__lte=10000)
                elif size == "btw10And30":
                    or_query |= Q(sf_size__gte=10000, sf_size__lte=30000)
                elif size == "btw30And60":
                    or_query |= Q(sf_size__gte=30000, sf_size__lte=60000)
                elif size == "btw60And100":
                    or_query |= Q(sf_size__gte=60000, sf_size__lte=100000)
                elif size == "btw100And200":
                    or_query |= Q(sf_size__gte=100000, sf_size__lte=200000)
                elif size == "200AndAbove":
                    or_query |= Q(sf_size__gte=200000)
            qs = qs.filter(or_query)

        if phases not in (None, ''):
            or_query = Q()

            for phase in phases.split(','):
                if phase == 'Historical':
                    continue

                else:
                    or_query |= Q(stage_name__icontains=phase)
                    qs = qs.filter(or_query)
        if project_types not in (None, ''):
            or_query = Q()

            for project_type in project_types.split(','):
                or_query |= Q(project_type__icontains=project_type)
            qs = qs.filter(or_query)

        if status:
            if status == "A":
                qs = qs.filter(status="A")
            elif status == "NA":
                qs = qs.filter(status="NA")
            else:
                qs = qs.filter(stage_name__icontains=status)

        if drawings:
            qs = qs.exclude(plan_drawings__isnull=True).exclude(plan_drawings__exact='None')

        if wage:
            qs = qs.exclude(davis_bacon_prevailing_wage_detail__isnull=True).exclude(
                davis_bacon_prevailing_wage_detail__exact='None')

        if union:
            qs = qs.exclude(laborer_union=False)

        if suggestion:
            qs = qs.filter(sf_size__isnull=False).exclude(sf_size=0)
        if coordinates != "undefined":
            try:
                jdata = json.loads(json.loads(coordinates))
                qs = qs.filter(longitude__range=(jdata['west'], jdata['east']),
                               latitude__range=(jdata['south'], jdata['north']))
            except:
                pass
        if user_location:
            ##### http://andilabs.github.io/django/devops/tools/postgres/postgis/2015/01/31/postgis-geodjango-english.html
            radius = float(100000)
            user_locations = user_location.split(',')
            if len(user_locations) == 2:
                current_latitude = user_locations[0]
                current_longitiude = user_locations[1]
                finder_location = Point(float(current_longitiude), float(current_latitude))
                desired_radius = {'m': radius}
                qs = qs.filter(
                    point__distance_lte=(finder_location, D(**desired_radius)))
        if sort == 'bid_due_date':
            return qs.exclude(bid_due_date=None).order_by("-bid_due_date")
        if sort == 'plan_drawings':
            return qs.exclude(plan_drawings__isnull=True).exclude(plan_drawings__exact='None')
        if sort == 'sf_size':
            return qs.exclude(sf_size=0).order_by("-sf_size")
        if sort == 'public_works':
            return qs.filter(Q(davis_bacon_prevailing_wage_detail__isnull=False) | Q(laborer_union=True))
        if sort == 'project_completion':
            return qs.exclude(project_completion=None).order_by("project_completion")
        if sort == 'created_date':
            return qs.order_by("-created_date")


        else:
            return qs.order_by('-last_modified_date')

    def show_all_fields_filled(self):
        qs = self.get_queryset()

        qs = qs.exclude(state_short__iexact='None') \
            .exclude(sf_size__iexact='None') \
            .exclude(sf_size=0) \
            .exclude(status_update_1__iexact='None') \
            .exclude(status_update_1_date__iexact='None') \
            .exclude(status_update_2__iexact='None') \
            .exclude(status_update_2_date__iexact='None') \
            .exclude(status_update_3__iexact='None') \
            .exclude(status_update_3_date__iexact='None') \
            .exclude(status_update_4__iexact='None') \
            .exclude(status_update_4_date__iexact='None') \
            .exclude(city__iexact='None') \
            .exclude(address__iexact='None') \
            .exclude(project_type__iexact='None') \
            .exclude(plan_drawings__iexact='None') \
            .exclude(stage_name__iexact='None')

        return qs

    def filter_by_project_type(self, project_type=None):
        qs = self.get_queryset()
        if project_type is not None:
            qs = qs.filter(project_type__iexact=project_type) \
                .exclude(project_type__iexact='None') \
                .values('name', 'city', 'state_short', 'url_slug', 'sf_size', 'last_modified_date_simple')
        return qs

    def get_recent_audit_logs(self, hour_later, this_hour):
        qs = self.get_queryset()
        qs = qs.extra(select={
            'changes': "SELECT  changes FROM auditlog_logentry "
                       f"WHERE projects_opportunity.id = auditlog_logentry.object_id AND timestamp BETWEEN '{hour_later}' AND '{this_hour}'"
                       "AND auditlog_logentry.content_type_id=9 AND auditlog_logentry.action=1 "
                       "ORDER BY auditlog_logentry.timestamp DESC LIMIT 1 "})
        return qs

    def get_similar_projects(self, state_short, project_type, project_id, user_profile):
        qs = self.get_queryset()
        if user_profile:
            qs = qs.exclude(id__in=user_profile.project_archives.all())
        qs = qs.filter(state_short=state_short,
                       project_type=project_type, status='A').exclude(id=project_id)
        qs = qs.extra(select={
            'company_id': "SELECT  id FROM projects_companyaccount"
                          f" WHERE projects_opportunity.company_account_id = projects_companyaccount.account_id ",
            'company_name': "SELECT  name FROM projects_companyaccount"
                            f" WHERE projects_opportunity.company_account_id = projects_companyaccount.account_id "})
        return qs.values('name', 'url_slug', 'company_name', 'company_id')

    def get_projects(self, state_short, project_type, project_id, user_profile):
        qs = self.get_queryset()
        if user_profile:
            qs = qs.exclude(id__in=user_profile.project_archives.all())
        qs = qs.filter(state_short=state_short,
                       project_type=project_type, status='A').exclude(id=project_id)
        qs = qs.extra(select={
            'company_id': "SELECT  id FROM projects_companyaccount"
                          f" WHERE projects_opportunity.company_account_id = projects_companyaccount.account_id ",
            'company_name': "SELECT  name FROM projects_companyaccount"
                            f" WHERE projects_opportunity.company_account_id = projects_companyaccount.account_id "})
        return qs.values('name', 'url_slug', 'company_name', 'company_id')

    def fetch_related_data(self, opportunity_id):
        try:
            opportunity = self.get(id=opportunity_id)
            contact_roles = ContactRole.objects.filter(opportunity_id=opportunity_id)
            company_account = CompanyAccount.objects.get(account_id=opportunity.company_account_id)
        except (self.model.DoesNotExist, CompanyAccount.DoesNotExist, Exception) as e:
            # Log the exception or handle it appropriately
            return None  # or return None, None, None or handle it in other ways

        return opportunity, contact_roles, company_account


class AbstractOpportunityBase(models.Model):
    objects = OpportunityManager()

    class Meta:
        abstract = True


class Opportunity(models.Model):
    oppid = models.CharField(max_length=90, unique=True, db_index=True)
    name = models.CharField(max_length=1000, db_index=True, null=True)
    address = models.CharField(max_length=1000, db_index=True, null=True, verbose_name='Street')
    city = models.CharField(max_length=90, db_index=True, null=True)
    state_short = models.CharField(max_length=60, null=True)
    state = models.CharField(max_length=100, db_index=True, null=True)
    zip_code = models.CharField(max_length=20, null=True)
    account_name = models.CharField(max_length=100, db_index=True, null=True)
    description = models.TextField(verbose_name='Description', null=True)
    opportunity_package = models.CharField(max_length=100, null=True)
    plan_drawings = models.CharField(max_length=10485760, verbose_name='Plans/Drawings', null=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True, verbose_name='Created date',
                                        null=True)
    last_modified_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True, null=True
    )
    when_c = models.CharField(max_length=10485760, null=True)
    bid_due_date = models.DateField(null=True, verbose_name='Pre construction bid due date')
    units = models.CharField(max_length=100, verbose_name='Number of rooms/Units', null=True)
    sf_size = models.IntegerField(default=0, db_index=True, verbose_name='Sq Ft', null=True)
    stage_name = models.CharField(max_length=100, db_index=True, verbose_name='Phase', null=True)
    project_type = models.CharField(max_length=1000, null=True)
    send_partner_details = models.CharField(max_length=1000, null=True)
    close_date = models.CharField(max_length=20, null=True)
    pipdcmkr_approval = models.CharField(max_length=10485760, null=True)
    account_formula_name = models.CharField(max_length=1000, null=True)
    account_billing_address = models.CharField(max_length=1000, null=True)
    account_phone = models.CharField(max_length=90, null=True)
    account_website = models.CharField(max_length=1000, null=True)
    account_prequalification_application = models.CharField(max_length=10485760, null=True)
    account_linkedin = models.CharField(max_length=1000, null=True)
    account_facebook = models.CharField(max_length=1000, null=True)
    account_twitter = models.CharField(max_length=1000, null=True)
    status_update_1 = models.CharField(max_length=10485760, db_index=True, null=True)
    status_update_1_date = models.CharField(max_length=90, null=True)
    status_update_2 = models.CharField(max_length=10485760, db_index=True, null=True)
    status_update_2_date = models.CharField(max_length=90, null=True)
    status_update_3 = models.CharField(max_length=10485760, db_index=True, null=True)
    status_update_3_date = models.CharField(max_length=90, null=True)
    status_update_4 = models.CharField(max_length=10485760, db_index=True, null=True)
    status_update_4_date = models.CharField(max_length=90, null=True)
    status_update_5 = models.CharField(max_length=10485760, db_index=True, null=True)
    status_update_5_date = models.CharField(max_length=90, null=True)
    last_modified_date_simple = models.CharField(max_length=90, null=True)
    hot_lead_trade_scope = models.CharField(max_length=300, null=True)
    negative_scope = models.CharField(max_length=300, null=True)
    url_slug = models.CharField(max_length=1000, unique=True, db_index=True)
    country = models.CharField(null=True, max_length=3000)
    company_account_id = models.CharField(null=True, max_length=100)
    project_completion = models.DateField(null=True, verbose_name='Project Completion')
    ACTIVE = 'A'
    NOT_ACTIVE = 'NA'
    PROJECT_STATUS = (
        (ACTIVE, 'Active'),
        (NOT_ACTIVE, 'Not Active'),
    )
    status = models.CharField(max_length=10, choices=PROJECT_STATUS, db_index=True)
    laborer_union = models.BooleanField(null=True)
    davis_bacon_prevailing_wage_detail = models.TextField(null=True)
    primary_contact_name = models.CharField(max_length=100, null=True, verbose_name='Primary Contact Name')
    primary_contact_phone = models.CharField(max_length=100, null=True, verbose_name='Primary Contact Phone')
    primary_contact_email = models.CharField(max_length=100, null=True, verbose_name='Primary Contact Email')
    site_contact_name = models.CharField(max_length=100, null=True, verbose_name='Site Contact Name')
    site_contact_phone = models.CharField(max_length=100, null=True, verbose_name='Site Contact Phone')
    site_contact_email = models.CharField(max_length=100, null=True, verbose_name='Site Contact Email')
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=False, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Longitude', null=True, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Latitude', null=True, db_index=True)
    pq_score = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    project_quality_tier = models.CharField(max_length=100, null=True)
    est_break_ground_date = models.DateField(null=True, verbose_name='Est. Break Ground Date')
    point = models.PointField(null=True)

    objects = OpportunityManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/projectboard/{self.url_slug}"

    @property
    def opportunity(self):
        return self.comments.first()

    @property
    def new_opportunity(self):
        if self.last_modified_date:
            delta = datetime.date.today() - self.last_modified_date.date()
            return delta.days <= 7

    class Meta:
        app_label = 'projects'


class ContactRoleManager(models.Manager):
    def filter_by(self, account_id=""):
        qs = self.get_queryset()
        if account_id:
            qs = qs.filter(account_id__iexact=account_id) \
                .order_by('-created')

        return qs

    def get_email_counts_by_opportunity(self, user, opportunity):
        qs = self.get_queryset()
        qs = qs.annotate(
            num_of_emails=Count('user_emails', distinct=True,
                                filter=Q(user_emails__user=user, user_emails__email_type='PB'), ), ). \
            annotate(max_date=Max('user_emails__time_sent',
                                  filter=Q(user_emails__user=user, user_emails__email_type='PB'), ), ). \
            filter(opportunity_id=opportunity.oppid, )
        return qs

    def get_contact_roles_by_project(self, project_id, user):
        qs = self.get_queryset()
        if project_id:
            qs = qs.filter(opportunity_id=project_id) \
                .exclude(email__isnull=False) \
                .exclude(user_emails__user=user).exclude(html_email_count__isnull=True) \
                .order_by('-html_email_count').extra(
                select={
                    'account_id': 'SELECT projects_companyaccount.id  FROM projects_companyaccount WHERE '
                                  'projects_contact.company_account_id = projects_companyaccount.account_id',
                    'company_name': 'SELECT projects_companyaccount.name  FROM projects_companyaccount WHERE '
                                    'projects_contact.company_account_id = projects_companyaccount.account_id',
                }).first()
        return qs

    def get_contactroles_by_project_id(self, opportunity_id, user_id, project_id):
        return self.get_queryset().filter(opportunity_id=opportunity_id).extra(
            select={
                'title': 'SELECT title FROM "projects_contact" '
                         'WHERE "projects_contact".contact_id = "projects_contactrole".contact_id',
                'user_project_activities': f"SELECT COUNT(*) FROM emails_useremail WHERE "
                                           f"emails_useremail.contact_id = projects_contactrole.id "
                                           f"AND emails_useremail.user_id = '{user_id}'"
                                           f" AND emails_useremail.opportunity_id = '{project_id}'",
                'user_total_system_activities': f"SELECT COUNT(*) FROM emails_useremail WHERE "
                                                f"emails_useremail.user_id = '{user_id}' "
                                                f"AND projects_contactrole.id = emails_useremail.contact_id ",
                'last_date':                    f"SELECT time_sent FROM emails_useremail WHERE "
                                                f"emails_useremail.user_id = '{user_id}' "
                                                f" AND emails_useremail.opportunity_id = '{project_id}'"
                                                f"AND projects_contactrole.id = emails_useremail.contact_id "
                                                f"ORDER BY  time_sent DESC LIMIT 1",
                'company_id': f"SELECT id FROM projects_companyaccount WHERE "
                              f" projects_contactrole.account_id = projects_companyaccount.account_id ",
            })


class ContactRole(TimestampedModel):
    opportunityid = models.ForeignKey('Opportunity', on_delete=models.CASCADE, null=True, related_name='contact_roles')
    contact_role_id = models.CharField(max_length=300, unique=True, db_index=True)
    contact_id = models.CharField(max_length=300, null=True)
    name = models.CharField(max_length=500, null=True, db_index=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    role = models.CharField(max_length=1000, null=True)
    opportunity_id = models.CharField(max_length=100, null=True)
    account_id = models.CharField(max_length=100, null=True)
    account_name = models.CharField(max_length=100, null=True, db_index=True)
    slug = models.SlugField(max_length=3000, null=True, db_index=True)

    def latest_email(self):
        return ''
        return UserEmail.objects.values('time_sent').filter(contact=self).order_by('-time_sent')[0]

    # def user_email_count(self):
    #     return UserEmail.objects.values('user').filter(contact=self).count()

    objects = ContactRoleManager()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'projects'


class CompanyAccountManager(models.Manager):
    def get_company(self, company_slug):
        qs = self.get_queryset()
        if company_slug:
            qs = qs.get(slug__iexact=company_slug)
        return qs

    def api_filter_by(self, kwargs, user_profile):

        qs = self.get_queryset()
        region = kwargs.get('region', None)
        plan_room = kwargs.get('plan_room', None)
        pre_qual = kwargs.get('pre_qual', None)

        if plan_room:
            if region:
                regions = region.split(';')
                or_query = Q()

                for item in regions:
                    or_query |= Q(market_working_region__contains=item)
                qs = qs.filter(or_query)
            qs = qs.filter(planroom_link__isnull=False)
            qs = qs.annotate(
                max_date_visited=Max('plan_rooms__date_visited',
                                     filter=Q(plan_rooms__user_profile=user_profile), ), ) \
                .annotate(max_note=Max('plan_rooms__note', filter=Q(plan_rooms__user_profile=user_profile), ), )


        if pre_qual:
            qs = qs.filter(prequalification_application__isnull=False)
            if region:
                regions = region.split(';')
                or_query = Q()

                for item in regions:
                    or_query |= Q(market_working_region__contains=item)
                qs = qs.filter(or_query)
            qs = qs.annotate(
                max_upload=Max('pre_qualify__upload', filter=Q(pre_qualify__user_profile=user_profile), ), ) \
                .annotate(max_note=Max('pre_qualify__note', filter=Q(pre_qualify__user_profile=user_profile), ), )

        return qs.order_by("name")

    def get_company_by_search(self, city_slug, pre_qualification, building_type, bidding_page, bidding_source,
                              socials, public_work):
        qs = self.get_queryset()
        if city_slug:
            qs = qs.filter(market_working_region__icontains=city_slug).extra(select={
                'contacts': 'SELECT COUNT(*) AS count FROM projects_contact WHERE projects_contact.company_account_id = projects_companyaccount.account_id',
                'active_projects': 'SELECT COUNT(*) AS count FROM projects_opportunity WHERE projects_opportunity.company_account_id = projects_companyaccount.account_id'
            })
        if pre_qualification and pre_qualification == 'Yes':
            qs = qs.filter(prequalification_application__isnull=False)
        if building_type:
            if building_type == 'All':
                qs = qs
            else:
                qs = qs.filter(planroom_opptype__icontains=building_type)
        if bidding_page:
            qs = qs.filter(planroom_link__isnull=False)
        if bidding_source:
            qs = qs.filter(opportunity_source__icontains=bidding_source)
        if socials:
            if socials == 'Twitter':
                qs = qs.filter(twitter__isnull=False)
            elif socials == 'Facebook':
                qs = qs.filter(facebook_page__isnull=False)
            elif socials == 'LinkedIn':
                qs = qs.filter(linkedin__isnull=False)
            elif socials == 'Youtube':
                qs = qs.filter(youtube__isnull=False)
        if public_work:
            if public_work == 'Union':
                qs = qs.filter(signatory_to_union=True)
            elif public_work == 'Davis Bacon Prevailing Wage':
                qs = qs.filter(prevailing_wage=True)
        return qs

    def get_company_by_region(self, region):
        qs = self.get_queryset()
        if region:
            qs = qs.filter(market_working_region__icontains=region) \
                .extra(select={
                'contacts': 'SELECT COUNT(*) AS count FROM projects_contact WHERE projects_contact.company_account_id = '
                            'projects_companyaccount.account_id',
                'active_projects': 'SELECT COUNT(*) AS count FROM projects_opportunity WHERE '
                                   'projects_opportunity.company_account_id = projects_companyaccount.account_id '
            })
        return qs.count(), qs

    def filter_by(self, planroom_opptype=""):
        qs = self.get_queryset()
        if planroom_opptype:
            qs = qs.filter(planroom_opptype__icontains=planroom_opptype) \
                .annotate(office_location=F('market_working_region')) \
                .extra(
                select={
                    'contacts': 'SELECT COUNT(*) FROM projects_contact WHERE projects_contact.company_account_id = projects_companyaccount.account_id',
                    'active_projects': "SELECT COUNT(*) FROM projects_opportunity \
                            WHERE projects_opportunity.company_account_id = projects_companyaccount.account_id"
                },
            ) \
                .values('contacts', 'active_projects', 'office_location', 'name', 'id', 'slug') \
                .exclude(planroom_opptype__iexact='None')

        return qs

    def get_prequalication_by_company(self, account, region, select_type):
        qs = self.get_queryset()
        qs = qs.annotate(max_date_began_application_process=Max('prequalifications__began_application_process',
                                                                filter=Q(prequalifications__account=account), ), ). \
            annotate(max_date_confirm_on_bid_list=Max('prequalifications__confirm_on_bid_list',
                                                      filter=Q(prequalifications__account=account), ), ). \
            annotate(recent_id=Max('prequalifications__id',
                                   filter=Q(prequalifications__account=account), ), )
        qs = qs.filter(billing_state__in=region, prequalification_application__isnull=False) \
            if select_type == "custom" else qs.filter(
            billing_state=region, prequalification_application__isnull=False)
        return qs

    def get_plan_rooms_by_company(self, user_profile, region, select_type):
        qs = self.get_queryset()
        qs = qs.annotate(
            max_date_visited=Max('plan_rooms_date_visited', filter=Q(plan_rooms__user_profile=user_profile), ), ). \
            annotate(recent_id=Max('plan_rooms__id',
                                   filter=Q(plan_rooms__user_profile=user_profile), ), )
        qs = qs.filter(
            market_working_region__in=region, plan_room_link__isnull=False)
        return qs


class CompanyAccount(models.Model):
    account_id = models.CharField(max_length=90, unique=True, db_index=True)
    name = models.CharField(max_length=500, null=True, db_index=True)
    billing_address = models.TextField(null=True, db_index=True, blank=True)
    billing_street = models.TextField(null=True, db_index=True, blank=True)
    billing_city = models.CharField(null=True, max_length=300, db_index=True, blank=True)
    billing_state = models.CharField(null=True, max_length=300, db_index=True, blank=True)
    billing_postal_code = models.CharField(null=True, max_length=300, blank=True)
    billing_country = models.CharField(null=True, max_length=300, blank=True)
    phone = models.CharField(max_length=1000, null=True, blank=True)
    fax = models.CharField(max_length=1000, null=True, blank=True)
    website = models.CharField(max_length=500, null=True, blank=True)
    industry = models.CharField(max_length=1000, null=True, blank=True)
    market_working_region = models.TextField(max_length=1000, null=True, db_index=True, blank=True)
    planroom_link = models.CharField(max_length=1000, null=True, blank=True)
    opportunity_source = models.CharField(max_length=1000, null=True, blank=True)
    opportunity_source_stage_type = models.CharField(max_length=1000, null=True, blank=True)
    no_planroom_confirmed = models.CharField(max_length=1000, null=True, blank=True)
    planroom_opptype = models.CharField(max_length=1000, null=True, blank=True)
    no_itb_sending_confirmed = models.CharField(max_length=1000, null=True, blank=True)
    twitter = models.CharField(max_length=1000, null=True, blank=True)
    facebook_page = models.CharField(max_length=1000, null=True, blank=True)
    linkedin = models.CharField(max_length=1000, null=True, blank=True)
    youtube = models.CharField(max_length=1000, null=True, blank=True)
    prequalification_application = models.CharField(max_length=10485760, null=True, blank=True)
    confirmed_no_prequal_application = models.CharField(max_length=1000, null=True, blank=True)
    no_of_contacts_with_email_address = models.IntegerField(null=True, blank=True)
    open_opportunities = models.IntegerField(null=True, blank=True)
    signatory_to_union = models.CharField(max_length=1000, null=True, blank=True)
    prevailing_wage = models.CharField(max_length=1000, null=True, blank=True)
    internal_cleaning_reason = models.CharField(max_length=1000, null=True, blank=True)
    enr_top_contractors_1_100 = models.BooleanField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    slug = models.SlugField(max_length=3000, null=False, db_index=True)
    last_modified_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True
    )
    status = models.CharField(max_length=2, null=True, blank=True)
    multiple_offices_text = models.TextField(null=True, blank=True)
    prequal_application_submit_instruction = models.TextField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    french_speaking = models.BooleanField(null=True, blank=True)
    contact_html_email_count = models.IntegerField(null=True, blank=True)
    organizational_score = models.IntegerField(null=True, blank=True)
    average_project_size = models.IntegerField(null=True, blank=True)
    linkedin_head_count = models.IntegerField(null=True, blank=True)
    facebook_followers = models.IntegerField(null=True, blank=True)
    instagram_followers = models.IntegerField(null=True, blank=True)
    twitter_followers = models.IntegerField(null=True, blank=True)
    youtube_subscribers = models.IntegerField(null=True, blank=True)
    linked_in_followers = models.IntegerField(null=True, blank=True)
    number_of_offices = models.IntegerField(null=True, blank=True)
    all_opportunities = models.IntegerField(null=True, blank=True)
    founded = models.CharField(null=True, max_length=255, blank=True)
    naics_code = models.CharField(null=True, max_length=255, blank=True)
    sic = models.CharField(null=True, max_length=255, blank=True)
    top_overall_contact = models.CharField(null=True, max_length=255, blank=True)
    top_estimating = models.CharField(null=True, max_length=255, blank=True)
    top_project_manager = models.CharField(null=True, max_length=255, blank=True)
    top_superintendent = models.CharField(null=True, max_length=255, blank=True)
    top_human_resource = models.CharField(null=True, max_length=255, blank=True)
    twitter_bio = models.TextField(null=True, blank=True)
    youtube_bio = models.TextField(null=True, blank=True)
    facebook_bio = models.TextField(null=True, blank=True)
    instagram_bio = models.TextField(null=True, blank=True)
    linked_in_bio = models.TextField(null=True, blank=True)
    intelconstruct_url = models.CharField(null=True, max_length=255, blank=True)
    intelconstruct_company_id = models.CharField(null=True, max_length=255, blank=True)
    latitude = models.CharField(null=True, max_length=255, blank=True)
    longitude = models.CharField(null=True, max_length=255, blank=True)
    top_c_level = models.CharField(null=True, max_length=255, blank=True)
    is_archive = models.BooleanField(null=False, default=False, verbose_name='Archive', blank=True)
    social_network_tier = models.CharField(null=True, max_length=255, blank=True)
    organizational_tier = models.CharField(null=True, max_length=255, blank=True)

    objects = CompanyAccountManager()

    def first_letter(self):
        return self.name and self.name[0] or ''

    def get_absolute_url(self):
        return f"/general-contractor-intelligence/company-profiles/{self.slug}"

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'projects'


class HotScope(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.CharField(max_length=20, null=True, unique=True)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'projects'


class ContactManager(models.Manager):
    def filter_by(self, company_account_id="", user_id=""):
        qs = self.get_queryset()
        if company_account_id:
            qs = qs.filter(company_account_id__iexact=company_account_id)
        if user_id:
            qs = qs.annotate(
                num_of_emails=Count('user_emails', distinct=True,
                                    filter=Q(user_emails__user_id=user_id, user_emails__email_type='GC'), ), ). \
                annotate(max_date=Max('user_emails__time_sent',
                                      filter=Q(user_emails__user_id=user_id, user_emails__email_type='GC'), ), )
        qs = qs.order_by('-created_date')

        return qs

    def emails_to_contact(self, user_id):
        qs = self.get_queryset()
        qs = qs.annotate(
            num_of_emails=Count('user_emails', distinct=True,
                                filter=Q(user_emails__user_id=user_id, user_emails__email_type='GC'), ), ). \
            annotate(max_date=Max('user_emails__time_sent',
                                  filter=Q(user_emails__user_id=user_id, user_emails__email_type='GC'), ), )

        return qs

    def get_other_key_records(self, query):
        result = {}
        if query:
            result = {
                'estimating': query.filter(key_estimating_project_stage_knowledge=True).count(),
                'human_resources': query.filter(hiring_person=True).count(),
                'superintendents': query.filter(title__icontains='superintendent').count(),
                'project_managers': query.filter(
                    Q(title__icontains='project manager') | Q(title__icontains='pm')).count(),
                'c_level_owners': query.filter(
                    Q(title__icontains='ceo') | Q(title__icontains='chief') | Q(title__icontains='president') | Q(
                        title__icontains='owner')).count(),
            }

        return result

    def get_next_prev(self, company_account_id, name_slug):
        result = None, None
        if company_account_id and name_slug:
            qs = self.get_queryset()
            contact = qs.filter(company_account_id__iexact=company_account_id).order_by('name')

            previous = next_ = None
            l = len(contact)
            for index, item in enumerate(contact):
                if item.slug == name_slug:
                    result = contact[index + 1].slug if index < (l - 1) else None, contact[
                        index - 1].slug if index > 0 else None
                    break
        return result

    def get_opportunity_by_contact_id(self, query):
        result = []
        if query:
            with connection.cursor() as cursor:
                sql = 'SELECT name, city, state_short, url_slug, sf_size, last_modified_date_simple FROM (SELECT projects_contactrole.contact_id, projects_contactrole.opportunity_id, search_opportunity.* FROM projects_contactrole INNER JOIN search_opportunity ON search_opportunity.oppid = projects_contactrole.opportunity_id WHERE projects_contactrole.contact_id = %s) AS opp GROUP BY (opp.name, opp.city, opp.state_short, opp.url_slug, opp.sf_size, opp.last_modified_date_simple)'
                cursor.execute(sql, [query.contact_id])
                result = dictfetchall(cursor)
        return result

    def phone_clean_up(self, phone):
        if phone:
            return phone.replace('Phone:', '').replace('.', '').replace('(', '').replace(')', '').replace(' ',
                                                                                                          '').replace(
                '-', '')
        return None

    def get_other_key_records_individual(self, query):
        result = {}
        if query:
            # contact_phone = phone_clean_up(query.phone) if query.phone else phone_clean_up(query.company_phone)
            # phone_number = phonenumbers.parse(contact_phone, 'US') if contact_phone else None
            # region = geocoder.description_for_number(phone_number, "en") if phone_number and phonenumbers.is_possible_number(phone_number) and phonenumbers.is_valid_number(phone_number) else None

            result = {
                'estimating': True if query.key_estimating_project_stage_knowledge == True else False,
                'human_resources': True if query.hiring_person == True else False,
                'accounting': True if query.accounting == True else False,
                'project_managers': True if (
                    'project manager' in query.title.lower() or 'pm' in query.title.lower() if query.title else False) else False,
                'key_compliance': True if query.key_compliance == True else False,
                'region': 0  # self.get_region_not_city(region)
            }

        return result

    def get_region_not_city(self, state):
        if state and ',' in state:
            state_value = state.split(', ')[1]
            for x in list(chain(us, ca, uk)):
                if x['abbreviation'] == state_value:
                    return x['name']
        return state

    def get_contacts_by_region(self, region):
        qs = self.get_queryset()
        if region:
            if region == 'District of Columbia':
                region = 'Washington D.C.'
            qs = qs.filter(region__iexact=region) \
                .extra(select={
                'company_slug': 'SELECT slug FROM projects_companyaccount WHERE projects_contact.company_account_id = projects_companyaccount.account_id',
                'company_name': 'SELECT name FROM projects_companyaccount WHERE projects_contact.company_account_id = projects_companyaccount.account_id',
            })
        return qs.count(), qs

    def get_key_contacts_by_region(self, region):
        qs = self.get_queryset()
        if region:
            qs = Contact.objects.filter(region=region). \
                exclude(email__isnull=True).distinct('company_account_id').order_by('company_account_id')

            contacts = qs.values("company_account_id").annotate(
                html_email_count=Max('html_email_count'))
            qs = qs.distinct('com`pany_account_id').filter(company_account_id__in=contacts.values('company_account_id'),
                                                           user_emails__contact__account_id__isnull=True).extra(
                select={
                    'account_id': 'SELECT projects_companyaccount.id  FROM projects_companyaccount WHERE '
                                  'projects_contact.company_account_id = projects_companyaccount.account_id',
                })

        return qs.count(), qs

    def get_companies_by_region(self, region):
        qs = self.get_queryset()
        if region:
            qs = Contact.objects.filter(region=region). \
                exclude(email__isnull=True).distinct('company_account_id').order_by('company_account_id').extra(
                select={
                    'account_id': 'SELECT projects_companyaccount.id  FROM projects_companyaccount WHERE '
                                  'projects_contact.company_account_id = projects_companyaccount.account_id AND is_archive=False',
                })

        return qs

    def get_contacts_by_company(self, company_account_id, region, user):
        qs = self.get_queryset()
        if company_account_id:
            qs = qs.filter(company_account_id=company_account_id, region=region) \
                .exclude(email__isnull=True).exclude(html_email_count__isnull=True) \
                .exclude(user_emails__is_mass_email=True, user_emails__user=user).exclude(html_email_count__isnull=True) \
                .exclude(html_email_count__isnull=True) \
                .order_by('-html_email_count').extra(
                select={
                    'account_id': 'SELECT projects_companyaccount.id  FROM projects_companyaccount WHERE '
                                  'projects_contact.company_account_id = projects_companyaccount.account_id',
                    'company_name': 'SELECT projects_companyaccount.name  FROM projects_companyaccount WHERE '
                                    'projects_contact.company_account_id = projects_companyaccount.account_id',
                }).first()
        return qs

    def get_region_contacts(self, contact_list):
        qs = self.get_queryset()
        qs = qs.filter(id__in=contact_list).extra(
            select={
                'account_id': 'SELECT projects_companyaccount.id  FROM projects_companyaccount WHERE '
                              'projects_contact.company_account_id = projects_companyaccount.account_id'
            })
        return qs

    def get_special_list(self, keyword, company_account_id, user_id):
        qs = self.get_queryset()
        if keyword:
            qs = qs.filter(company_account_id__iexact=company_account_id)
            if keyword == 'estimating':
                qs = qs.filter(key_estimating_project_stage_knowledge=True)
            elif keyword == 'project_managers':
                qs = qs.filter(Q(title__icontains='project manager') | Q(title__icontains='pm'))
            elif keyword == 'c_level_owner':
                qs = qs.filter(
                    Q(title__icontains='ceo') | Q(title__icontains='chief') | Q(title__icontains='president') | Q(
                        title__icontains='owner'))
            elif keyword == 'superintendents':
                qs = qs.filter(title__icontains='superintendent')
            elif keyword == 'human_resources':
                qs = qs.filter(hiring_person=True)
            elif keyword == 'key_compliance':
                qs = qs.filter(key_compliance=True)
            elif keyword == 'accounting':
                qs = qs.filter(accounting=True)
            qs = qs.annotate(
                num_of_emails=Count('user_emails', distinct=True,
                                    filter=Q(user_emails__user_id=user_id, user_emails__email_type='GC'), ), ). \
                annotate(max_date=Max('user_emails__time_sent',
                                      filter=Q(user_emails__user_id=user_id, user_emails__email_type='GC'), ), )
        return qs.count(), qs

    def normalize_query(self, query_string,
                        findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                        normspace=re.compile(r'\s{2,}').sub):
        ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
            and grouping quoted words together.
            Example:

            # normalize_query('  some random  words "with   quotes  " and   spaces')
            ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

        '''
        return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]

    def search(self, query_string):
        qs = self.get_queryset()
        ''' Returns a query, that is a combination of Q objects. That combination
            aims to search keywords within a model by testing the given search fields.

        '''
        query = None  # Query to search for every search term
        terms = self.normalize_query(query_string)
        search_fields = ['name', 'phone', 'title', 'email']
        for term in terms:
            or_query = None  # Query to search for a given term in each field
            for field_name in search_fields:
                q = Q(**{"%s__search" % field_name: term})
                if or_query is None:
                    or_query = q
                else:
                    or_query = or_query | q
            if query is None:
                query = or_query
            else:
                query = query | or_query
            return qs.filter(query).values('name', 'phone', 'title', 'email', 'company_account_id').extra(select={
                'company_slug': 'SELECT slug FROM projects_companyaccount WHERE projects_contact.company_account_id = projects_companyaccount.account_id',
                'company_name': 'SELECT name FROM projects_companyaccount WHERE projects_contact.company_account_id = projects_companyaccount.account_id',
            })


class Contact(models.Model):
    contact_id = models.CharField(max_length=90, unique=True, db_index=True)
    name = models.CharField(max_length=500, null=True, db_index=True)
    phone = models.CharField(max_length=1000, null=True)
    email = models.EmailField(max_length=100, null=True)
    title = models.CharField(max_length=1000, null=True, db_index=True)
    key_estimating_project_stage_knowledge = models.BooleanField()
    key_compliance = models.BooleanField()
    accounting = models.BooleanField()
    hiring_person = models.BooleanField()
    confirmed_no_email = models.BooleanField()
    no_bid_knowledge = models.BooleanField()
    no_longer_employed = models.BooleanField()
    created_date = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    last_modified_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, blank=True
    )
    company_account_id = models.CharField(max_length=100)
    slug = models.SlugField(max_length=3000, null=True, db_index=True)
    region = models.CharField(max_length=1000, null=True)
    status = models.CharField(max_length=2, null=True)
    html_email_count = models.DecimalField(max_digits=8, decimal_places=2, null=True)

    objects = ContactManager()

    def first_letter(self):
        return self.name and self.name[0] or ''

    def __str__(self):
        return self.name

    def get_company_slug(self):
        return CompanyAccount.objects.get(account_id=self.company_account_id).slug

    def get_absolute_url(self):
        state_short = self.slug

        return f"/general-contractor-intelligence/company-profiles/{self.get_company_slug()}/contacts/{self.slug}"

    class Meta:
        app_label = 'projects'


class SavedSearch(models.Model):
    name = models.CharField(max_length=50)
    params = models.CharField(max_length=200)
    projects_count = models.IntegerField()