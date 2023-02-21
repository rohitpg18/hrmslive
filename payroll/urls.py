from django.urls import path
from payroll.views import *
from account.views import SalarySlip


urlpatterns = [
    path("leave-applications/",LeaveApplications.as_view(),name="leave_applications"),
    path("leave-applications/<int:pk>",ApproveLeaves.as_view(),name="approve_leaves"),
    
    path("attendance-applications/",ApproveAttendance.as_view(),name="attendance_applications"),
    path("department/",DepartmentDetails.as_view(),name="department"),
    path("designation/",DesignationDetails.as_view(),name="designation"),
    path("teams/",Team.as_view(),name="teams"),
    path("team-members/",TeamMembers.as_view(),name="team_members"),
    path("payroll/", PayrollData.as_view(), name = "payroll"),
    path("missing-attendance-applications/", MissingAttendanceApplications.as_view(), name = "missing_attendance_applications"),
    path("all-users/", EmployeeList.as_view(), name = 'all_users'),
    path('emp-activate/<int:emp_id>/', EmpActivate, name="emp_activate"),
    path('emp-deactivate/<int:emp_id>/', EmpDeactivate, name="emp_deactivate"),
    path("shift/", Shift.as_view(), name="shift"),
    path("update-employee/<int:pk>",UpdateEmployee.as_view(), name="update_employee" ),
    
    path("admin-dashboard/", AdminDashboard.as_view(), name = "admin_dashboard"),
]   