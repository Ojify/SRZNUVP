from django.urls import path

from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.applications, name='list'),
    path('<int:application_id>/', views.application_detail, name='detail'),
    path('statistics/', views.statistics, name='statistics'),
]
