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
    path('day-based-salary/', DayBasedSalary.as_view(), name = "day_based_salary"),
    path('department-based-salary/', DepartmentBasedSalary.as_view(), name = "department_based_salary"),
    path('time-based-salary/', TimeBasedSalary.as_view(), name="time_based_salary"),
    path('total-paid-salary/', SalariesPaidTillDate.as_view(), name="total_paid_salary"),
    
    # other
    path("department/", DepartmentDetails.as_view(),name="department"),
    path("designation/", DesignationDetails.as_view(),name="designation"),
    path("shift/", Shift.as_view(), name="shift"),
    
    # teams
    path("teams/", Team.as_view(),name="teams"),
    path('add-team/', AddTeam.as_view(), name = "add_team"),
    path("update-team/<int:id>/", UpdateTeam.as_view(), name="update_team"),
    path("team-members/", TeamMembers.as_view(),name="team_members"),
    
    # policy
    path("policy/", Policy.as_view(), name="policy"),
    
    # dashboards
    path("team-leader-dashboard/", TeamLeaderDashboard.as_view(), name = "team_leader_dashboard"),
    path("ems-dashboard/", HREMSDashboard.as_view(), name = "ems_dashboard"),
    path("leaves-dashboard/", HRLeavesDashboard.as_view(), name='leaves_dashboard'),
    path("attendance-dashboard/", HRAttendanceDashboard.as_view(), name='attendance_dashboard'),
    path("payroll-dashboard/", HRPayrollDashboard.as_view(), name='payroll_dashboard'),
    path("create-employee-dashboard/", HRCreateEmployeeDashboard.as_view(), name='create_employee_dashboard'),
    path("hr-analytics/", HrAnalytics.as_view(), name='hr_analytics'),
    path("hr-info/", data, name='hr_info'),
    
]