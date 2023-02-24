from django.urls import path
from account.views import *





urlpatterns = [
    # employee details forms
    path("signup/", UserSignUp.as_view(), name="signup"),
    path("additional-detail/", AdditionalDetail.as_view(), name="additional_details"),
    path("bank-detail/", BankDetail.as_view(), name="bank_details"),
    path("educational-detail/", EducationalDetail.as_view(), name="educational_details"),
    path("previous-organization-detail/", PreviousOrganizationDetail.as_view(), name="previous_organization_details"),
    
    # details view
    path("self-detail/", SelfDetail.as_view(), name="self_details"),
    
    # self leaves
    path("self-leave/", ApplyLeave.as_view(), name="self_leave"),
    path("leave-history/", LeavesHistory.as_view(), name="leave_history"),
    
    # self attendance
    path("self-attendance/", ApplyAttendance.as_view(), name="self_attendance"),
    path("attendance-history/", AttendanceHistory.as_view(), name = 'attendance_history'),
    path("missing-attendance/",MissedAttendance.as_view(),name="missing_attendance"),
    path("missing-attendance-history/",MissingAttendanceHistory.as_view(),name="missing_attendance_history"),
    
    # self salary
    path("self-salary/", SalaryMonthlyData.as_view(), name="self_salary"),
    path("self-salary/<int:pk>/", SalarySlip.as_view(), name="salary_slip"),
]