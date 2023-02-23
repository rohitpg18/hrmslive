from account.account_views.dependencies.basic_functions import *

class MissingAttendanceApplications(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        user_id = request.user.id
                
        is_permission = request.user.employee_permissions_user.can_approve_leaves
        
        print(is_permission)    
        
        if is_permission:
            
            applications= MissingAttendance.objects.filter(is_requested=True)
            
            return render(request, "payroll/emp_management/missing_attendance.html",{'applications': applications})
            
            
        else:
            return redirect('self-details')
        
        
class MissingAttendanceApplicationsHistory(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        teams = EmployeePermissions.is_team_leader(request)
        if  teams == False:
            messages.warning(request, 'Teams Not Exists')
            return redirect('admin_dashboard')
        
        team_employees=set()
        
        for team in teams:
            team_employees=team_employees.union(team.employees.values_list('id', flat=True))
            
        
        missing_applications_list=set()
        
        
        for emp_id in team_employees:
            missing_applications_list=missing_applications_list.union(MissingAttendance.objects.filter(emp_user_id=emp_id))
            
            
        if len(missing_applications_list) < 1:
            messages.warning(request, "Missing attendance applications not available")
            return redirect('team_leader_dashboard')
        
        data={
            'missing_applications_list':missing_applications_list,
            'applications_count': len(missing_applications_list)
            }
        
        
            
        return render(request, "payroll/emp_management/missing_attendace_applications_history.html",data)
        
        