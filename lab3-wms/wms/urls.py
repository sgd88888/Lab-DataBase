from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('login', views.login, name = 'login'),
    # redirect to login
    path('', RedirectView.as_view(url = 'login')),
    path('index', views.index, name = 'index'),
    path('department', views.department, name = 'department'),
    path('department-create', views.department_create, name = 'department-create'),
    path('department-update', views.department_update, name = 'department-update'),
    path('department-delete', views.department_delete, name = 'department-delete'),
    path('department-search', views.department_search, name = 'department-search'),
    path('department-report', views.department_report, name = 'department-report'),
    path('staff', views.staff, name = 'staff'),
    path('staff-create', views.staff_create, name = 'staff-create'),
    path('staff-update', views.staff_update, name = 'staff-update'),
    path('staff-delete', views.staff_delete, name = 'staff-delete'),
    path('staff-search-scode', views.staff_search_scode, name = 'staff-search-scode'),
    path('staff-search-sname', views.staff_search_sname, name = 'staff-search-sname'),
    path('attendance', views.attendance, name = 'attendance'),
    path('attendance-create', views.attendance_create, name = 'attendance-create'),
    path('attendance-update', views.attendance_update, name = 'attendance-update'),
    path('attendance-delete', views.attendance_delete, name = 'attendance-delete'),
    path('wage', views.wage, name = 'wage'),
    path('yearending', views.yearending, name = 'yearending'),
    path('wage-report', views.wage_report, name = 'wage-report'),
]