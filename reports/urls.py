from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_test_case, name='add_test_case'),
    path('cases/', views.view_test_cases, name='view_test_cases'),
    path('summary/add/', views.add_summary, name='add_summary'),
    path('summary/', views.view_summary, name='view_summary'),
]