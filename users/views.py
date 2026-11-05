from django.shortcuts import render, get_object_or_404
from .models import User

def users(request):
    users_list = User.objects.all()
    return render(request, 'users/user_list.html', {'users_list': users_list})

def user_detail(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    user_applications = user.applications.select_related('project', 'status').all()
    
    return render(request, 'users/user_detail.html', {
        'user': user,
        'user_applications': user_applications
    })
