from django.urls import path
from account.views import *





urlpatterns = [
    path("signup/", UserSignUp.as_view(), name="signup"),
    path("additional-detail/", AdditionalDetail.as_view(), name="additional_details"),
    path("bank-detail/", BankDetail.as_view(), name="bank_details"),
    path("educational-detail/", EducationalDetail.as_view(), name="educational_details"),
    path("previous-organization-detail/", PreviousOrganizationDetail.as_view(), name="previous_organization_details"),
    
    path("self-detail/", SelfDetail.as_view(), name="self_details"),
    
    path("self-leave/", ApplyLeave.as_view(), name="self_leave"),
    path("leave-history/", LeavesHistory.as_view(), name="leave_history"),
    
    path("self-attendance/", ApplyAttendance.as_view(), name="self_attendance"),
    path("attendance-history/", AttendanceHistory.as_view(), name = 'attendance_history'),
    path("missing-attendance/",MissedAttendance.as_view(),name="missing_attendance"),
    path("missing-attendance-history/",MissingAttendanceHistory.as_view(),name="missing_attendance_history"),
    

    path("self-salary/", SalaryMonthlyData.as_view(), name="self_salary"),
    path("self-salary/<int:pk>/", SalarySlip.as_view(), name="salary_slip"),
    
]