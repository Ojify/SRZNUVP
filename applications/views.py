from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Q
from .models import Application
from projects.models import Project

def applications(request):
    qs = Application.objects.select_related('project', 'user', 'status').all()

    status_filter = request.GET.get('status')
    if status_filter:
        qs = qs.filter(status__code=status_filter)

    search_query = request.GET.get('q', '').strip()
    if search_query:
        qs = qs.filter(
            Q(user__name__icontains=search_query) | 
            Q(project__name__icontains=search_query)
        )

    sort = request.GET.get('sort', 'date_desc')
    if sort == 'date_asc':
        qs = qs.order_by('created_at')
    elif sort == 'project':
        qs = qs.order_by('project__name')
    else:
        qs = qs.order_by('-created_at')

    paginator = Paginator(qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    from .models import Status
    statuses = Status.objects.all()

    return render(request, 'applications/application_list.html', {
        'applications_list': page_obj,
        'page_obj': page_obj,
        'statuses': statuses,
        'status_filter': status_filter,
        'search_query': search_query,
        'sort': sort,
    })

def application_detail(request, application_id):
    app = get_object_or_404(Application.objects.select_related('project', 'user', 'status'), pk=application_id)
    return render(request, 'applications/application_detail.html', {'application': app})

def statistics(request):
    total_apps = Application.objects.aggregate(total=Count('id'))['total']
    
    active_apps = Application.objects.filter(status__code='active').count()
    cancelled_apps = Application.objects.exclude(status__code='active').exclude(status__code='approved').count()

    project_stats = Project.objects.annotate(apps_count=Count('applications')).order_by('-apps_count')

    return render(request, 'applications/statistics.html', {
        'total_apps': total_apps,
        'active_apps': active_apps,
        'cancelled_apps': cancelled_apps,
        'project_stats': project_stats,
    })
