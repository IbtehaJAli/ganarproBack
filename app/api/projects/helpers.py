from django.db.models import Q, When, Value, Case, F, CharField, IntegerField


def get_project_board_filters(qs):
    project_types = [
        {
            'name': 'Military',
            'value': 'Military',
            'count': qs.filter(project_type__icontains='Military', status='A').count()
        },
        {
            'name': 'Police-Fire Station',
            'value': 'Police-Fire Station',
            'count': qs.filter(project_type__icontains='Police-Fire Station', status='A').count()
        },
        {
            'name': 'Recreation Center',
            'value': 'Recreation Center',
            'count': qs.filter(project_type__icontains='Recreation Center', status='A').count()
        },
        {
            'name': 'Bank',
            'value': 'Bank',
            'count': qs.filter(project_type__icontains='Bank', status='A').count()
        },
        {
            'name': 'Data center',
            'value': 'Data center',
            'count': qs.filter(project_type__icontains='Data center', status='A').count()
        },
        {
            'name': 'Worship',
            'value': 'Worship',
            'count': qs.filter(project_type__icontains='Worship', status='A').count()
        },
        {
            'name': 'Theatre',
            'value': 'Theatre',
            'count': qs.filter(project_type__icontains='Theatre', status='A').count()
        },
        {
            'name': 'Athletic',
            'value': 'Athletic',
            'count': qs.filter(project_type__icontains='Athletic', status='A').count()
        },
        {
            'name': 'Medical-Dental',
            'value': 'Medical-Dental',
            'count': qs.filter(project_type__icontains='Medical-Dental', status='A').count()
        },
        {
            'name': 'Fitness',
            'value': 'Fitness',
            'count': qs.filter(project_type__icontains='Fitness', status='A').count()
        },
        {
            'name': 'Gas Station',
            'value': 'Gas Station',
            'count': qs.filter(project_type__icontains='Gas Station', status='A').count()
        },
        {
            'name': 'Auto Office-Bay',
            'value': 'Auto Office-Bay',
            'count': qs.filter(project_type__icontains='Auto Office-Bay', status='A').count()
        },
        {
            'name': 'Grocery',
            'value': 'Grocery',
            'count': qs.filter(project_type__icontains='Grocery', status='A').count()
        },
        {
            'name': 'Library',
            'value': 'Library',
            'count': qs.filter(project_type__icontains='Library', status='A').count()
        },
        {
            'name': 'Car dealership',
            'value': 'Car dealership',
            'count': qs.filter(project_type__icontains='Car dealership', status='A').count()
        },
        {
            'name': 'Industrial',
            'value': 'Industrial',
            'count': qs.filter(project_type__icontains='Industrial', status='A').count()
        },
        {
            'name': 'Restaurant',
            'value': 'Restaurant',
            'count': qs.filter(project_type__icontains='Restaurant', status='A').count()
        },
        {
            'name': 'Retail',
            'value': 'Retail',
            'count': qs.filter(project_type__icontains='Retail', status='A').count()
        },
        {
            'name': 'Multi-family residential',
            'value': 'Multi-family residential',
            'count': qs.filter(project_type__icontains='Multi-family residential',
                               status='A').count()
        },
        {
            'name': 'Interior tenant fit out',
            'value': 'Interior tenant fit out',
            'count': qs.filter(project_type__icontains='Interior tenant fit out',
                               status='A').count()
        },
        {
            'name': 'Education',
            'value': 'Education',
            'count': qs.filter(project_type__icontains='Education', status='A').count()
        },
        {
            'name': 'WWTP',
            'value': 'WWTP',
            'count': qs.filter(project_type__icontains='WWTP', status='A').count()
        },
        {
            'name': 'Senior living Retirement',
            'value': 'Senior living Retirement',
            'count': qs.filter(project_type__icontains='Senior living Retirement',
                               status='A').count()
        },
        {
            'name': 'Community / Public',
            'value': 'Community / Public',
            'count': qs.filter(project_type__icontains='Community / Public', status='A').count()
        },
        {
            'name': 'Mixed Use',
            'value': 'Mixed Use',
            'count': qs.filter(project_type__icontains='Mixed Use', status='A').count()
        },
        {
            'name': 'Parking',
            'value': 'Parking',
            'count': qs.filter(project_type__icontains='Parking', status='A').count()
        },
        {
            'name': 'Corporate',
            'value': 'Corporate',
            'count': qs.filter(project_type__icontains='Corporate', status='A').count()
        },
        {
            'name': 'Airport',
            'value': 'Airport',
            'count': qs.filter(project_type__icontains='Airport', status='A').count()
        },
        {
            'name': 'Renovation Addition',
            'value': 'Renovation Addition',
            'count': qs.filter(project_type__icontains='Renovation Addition', status='A').count()
        },
        {
            'name': 'Zoo',
            'value': 'Zoo',
            'count': qs.filter(project_type__icontains='Zoo', status='A').count()
        },
        {
            'name': 'Transit station',
            'value': 'Transit station',
            'count': qs.filter(project_type__icontains='Transit station', status='A').count()
        },
        {
            'name': 'Residential Home',
            'value': 'Residential Home',
            'count': qs.filter(project_type__icontains='Residential Home', status='A').count()
        },

    ]
    statuses = [
        {
            'name': 'Pre-construction',
            'value': 'Pre-construction',
            'count': qs.filter(stage_name__icontains='Pre-construction').count()
        },
        {
            'name': 'Work in progress',
            'value': 'Work in progress',
            'count': qs.filter(stage_name__icontains='Work in progress').count()
        },
        {
            'name': '90% contracts purchased',
            'value': '90% contracts purchased',
            'count': qs.filter(stage_name__icontains='90% contracts purchased').count()
        },
        {
            'name': 'Historical',
            'value': 'Historical',
            'count': "Not active"
        },
    ]

    sizes = [
        {
            'name': 'No size (blank square foot)',
            'value': 'blank',
            'count': qs.filter(Q(sf_size=0) | Q(sf_size=None), status='A').count()
        },
        {
            'name': 'Extra Small',
            'value': 'extra_small',
            'count': qs.filter(sf_size__gte=1, sf_size__lte=4000, status='A').exclude(sf_size=0).count()
        },
        {
            'name': 'small',
            'value': 'small',
            'count': qs.filter(sf_size__gt=4000, sf_size__lte=31000, status='A').count()
        },
        {
            'name': 'Medium',
            'value': 'medium',
            'count': qs.filter(sf_size__gt=31000, sf_size__lte=150000, status='A').count()
        },
        {
            'name': 'Large',
            'value': 'large',
            'count': qs.filter(sf_size__gte=150000, sf_size__lte=500000, status='A').count()
        },
        {
            'name': 'Extra Large',
            'value': 'extra_large',
            'count': qs.filter(sf_size__gt=500000, sf_size__lte=3800000, status='A').count()
        },
    ]

    price_suggestion = {
        'name': 'Yes',
        'value': 'yes',
        'count': qs.filter(sf_size__isnull=False, status='A').exclude(sf_size=0).count()
    }

    blueprint_drawing = {
        'name': 'Yes',
        'value': 'yes',
        'count': qs.filter(status='A').exclude(plan_drawings__isnull=True, status='A').exclude(
            plan_drawings__exact='None').count()
    }

    laborer_union = {
        'name': 'Yes',
        'value': 'yes',
        'count': qs.filter(status='A').exclude(laborer_union=False, status='A').count()
    }

    prevailing_wage = {
        'name': 'Yes',
        'value': 'yes',
        'count': qs.filter(status='A').exclude(davis_bacon_prevailing_wage_detail__isnull=True)
            .exclude(davis_bacon_prevailing_wage_detail__exact='None').count()
    }

    return project_types, statuses, sizes


def project_research_query(query):

    query = query.annotate(
        sf_size_str=Case(
            When(Q(sf_size=0) | Q(sf_size=None), then=Value(" ")),
            When(Q(sf_size__gte=1) & Q(sf_size__lte=4000), then=Value("Extra Small")),
            When(Q(sf_size__gt=4000) & Q(sf_size__lte=31000), then=Value("Small")),
            When(Q(sf_size__gt=31000) & Q(sf_size__lte=150000), then=Value("Medium")),
            When(Q(sf_size__gt=150000) & Q(sf_size__lte=500000), then=Value("Large")),
            When(Q(sf_size__gt=500000) & Q(sf_size__lte=3800000), then=Value("Extra Large")),
            output_field=CharField()
        )
    )
    return query
