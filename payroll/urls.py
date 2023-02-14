from django.urls import path
from payroll.views import *
from account.views import SalarySlip


urlpatterns = [
    path("leave-applications/",LeaveApplications.as_view(),name="leave_applications"),
    path("leave-applications/<int:pk>",ApproveLeaves.as_view(),name="approve_leaves"),
    path("attendance-applications/",ApproveAttendance.as_view(),name="attendance_applications"),
    path("department/",DepartmentDetails.as_view(),name="department"),
    path("designation/",DesignationDetails.as_view(),name="designation"),
    path("payroll/", PayrollData.as_view(), name = "payroll"),
    path("filter-salary/", filter_salary, name = "filter_salary"),
    path("payroll/<int:pk>/", SalarySlip.as_view(), name="salary_slip_payroll"),
]   