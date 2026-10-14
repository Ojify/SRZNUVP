from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('', views.users, name='list'),
    path('<int:user_id>/', views.user_detail, name='detail'),
]