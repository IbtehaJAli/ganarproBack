import django_filters
from django_filters import NumberFilter, BooleanFilter, CharFilter

from search.models import Opportunity


class ProjectsFilterSet(django_filters.FilterSet):
    sort = CharFilter(method='sort_by')
    project_type = CharFilter(method='sort_by', lookup_expr="icontains")

    # bid_due_date,
    def sort_by(self, queryset, field_name, value, ):
        if value in ['last_modified_date', 'bid_due_date', 'project_completion', 'created_date']:
            return queryset.order_by(f"-{value}")
        if value == 'bid_due_date':
            return queryset.order_by("-bid_due_date")
        if value == 'plan_drawings':
            return queryset.exclude(plan_drawings__isnull=True).exclude(plan_drawings__exact='None')
        if value == 'sf_size':
            return queryset.exclude(sf_size__isnull=True).exclude(sf_size__exact='None')
        if value == 'laborer_union':
            return queryset.exclude(laborer_union=False)
    # overdue = BooleanFilter(method="get_overdue", field_name="returned")
    # created_start_date = kwargs.get('created_start_date', None)
    # created_end_date = kwargs.get('created_end_date', None)
    # updated_start_date = kwargs.get('updated_start_date', None)
    # updated_end_date = kwargs.get('updated_end_date', None)
    # bid_due_start_date = kwargs.get('bid_due_start_date', None)
    # bid_due_end_date = kwargs.get('bid_due_end_date', None)
    # completion_start_date = kwargs.get('completion_start_date', None)
    # completion_end_date = kwargs.get('completion_end_date', None)
    # project_name_or_city = kwargs.get('project_name_or_city', None)
    # state = kwargs.get('state', None)
    # size = kwargs.get('size', None)
    # project_type = kwargs.get('project_type', None)
    # status = kwargs.get('status', None)
    # drawings = kwargs.get('drawings', None)
    # wage = kwargs.get('wage', None)
    # union = kwargs.get('union', None)
    # suggestion = kwargs.get('suggestion', None)

    # class Meta:
    #     model = Opportunity
    # fields = ["project_type"]
