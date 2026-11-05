from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Project

def projects(request):
    projects_list = Project.objects.annotate(num_apps=Count('applications')).all()
    return render(request, 'projects/project_list.html', {'projects_list': projects_list})

def project_detail(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    
    applications = project.applications.select_related('user', 'status').all()
    
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'applications': applications
    })
