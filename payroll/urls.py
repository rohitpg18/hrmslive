from django.urls import path
from payroll.views import *



urlpatterns = [
    # leaves
    path("leave-applications/",LeaveApplications.as_view(),name="leave_applications"),
    path("leave-applications/<int:pk>",ApproveLeaves.as_view(),name="approve_leaves"),
    path("employee-leave-history/", EmployeeLeavesHistory.as_view(), name="employee_leave_history"),
    
    # attendance
    path("missing-attendance-applications/", MissingAttendanceApplications.as_view(), name = "missing_attendance_applications"),
    path("missing-attendance-history/", MissingAttendanceApplicationsHistory.as_view(), name = "missing_attendance_application_history"),
    path("attendance-applications/",ApproveAttendance.as_view(),name="attendance_applications"),
    path("attendance-list/", AttendanceList.as_view(), name="attendance_list"),
    path("emp-attendance-history/<str:pk>/", AttendanceHistoryEmp.as_view(), name="emp_attendance_history"),
    path("today-attendance-list/", TodayAttendanceList.as_view(), name="today_attendance_list"),
    
    # employees
    path("all-users/", EmployeeList.as_view(), name = 'all_users'),
    path("update-employee/<int:pk>",UpdateEmployee.as_view(), name="update_employee" ),
    path("verify-details/",VerifyDetails.as_view(),name="verify_details"),
    
    # payroll
    path("payroll/", PayrollData.as_view(), name = "payroll"),
    
    # other
    path("department/", DepartmentDetails.as_view(),name="department"),
    path("designation/", DesignationDetails.as_view(),name="designation"),
    path("shift/", Shift.as_view(), name="shift"),
    
    # teams
    path("teams/", Team.as_view(),name="teams"),
    path('add-team/', AddTeam.as_view(), name = "add_team"),
    path("update-team/<int:id>/", UpdateTeam.as_view(), name="update_team"),
    path("delete-team/<int:id>/", DeleteTeam.as_view(), name="delete_team"),
    path("team-members/", TeamMembers.as_view(),name="team_members"),
    
    # policy
    path("policy/", Policy.as_view(), name="policy"),
    
    # dashboards
    path("team-leader-dashboard/", TeamLeaderDashboard.as_view(), name = "team_leader_dashboard"),
    path("ems-dashboard/", HREMSDashboard.as_view(), name = "ems_dashboard"),
    path("leaves-dashboard/", HRLeavesDashboard.as_view(), name='leaves_dashboard'),
    path("attendance-dashboard/", HRAttendanceDashboard.as_view(), name='attendance_dashboard'),
    
    # NR
    path('emp-activate/<int:emp_id>/', EmpActivate, name="emp_activate"),
    path('emp-deactivate/<int:emp_id>/', EmpDeactivate, name="emp_deactivate"),   
]