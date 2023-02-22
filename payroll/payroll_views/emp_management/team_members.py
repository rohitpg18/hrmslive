from account.account_views.dependencies.basic_functions import *

class TeamMembers(View):
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        
        teams = EmployeePermissions.is_team_leader(request)
        if  teams == False:
            messages.warning(request, 'Teams Not Exists')
            return redirect('team_leader_dashboard')
        print(teams)
        team_employees=set()
        
        for team in teams:
            team_employees=team_employees.union(team.employees.all())
            
        print(team_employees)
    
        
        data={
            'members':team_employees,
            'members_count': len(team_employees)
            }
                
        return render(request,'payroll/emp_management/team_members.html',data)