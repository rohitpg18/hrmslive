from django.urls import path
from payroll.views import *


urlpatterns = [
    path("leave-applications/",LeaveApplications.as_view(),name="leave_applications"),
    path("leave-applications/<int:pk>",ApproveLeaves.as_view(),name="approve_leaves"),
    path("attendance-applications/",ApproveAttendance.as_view(),name="attendance_applications"),
    path("department/",DepartmentDetails.as_view(),name="department"),
    path("designation/",DesignationDetails.as_view(),name="designation"),
    path("payroll/", PayrollData.as_view(), name = "payroll"),
    path("filter-salary/", filter_salary, name = "filter_salary"),
]   