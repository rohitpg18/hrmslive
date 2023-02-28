from account.account_views.dependencies.basic_functions import *


class TeamLeaderDashboard(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        print(EmployeePermissions.is_team_leader(request))
    
        return render(request, 'payroll/admin_dashboards/team_leader_dashboard.html')
    
class HREMSDashboard(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
    
        return render(request, 'payroll/admin_dashboards/ems_dashboard.html')
    
class HRLeavesDashboard(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
    
        return render(request, 'payroll/admin_dashboards/leaves_dashboard.html')
    
class HRAttendanceDashboard(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
    
        return render(request, 'payroll/admin_dashboards/attendance_dashboard.html')

class HRPayrollDashboard(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
    
        return render(request, 'payroll/admin_dashboards/payroll_dashboard.html')