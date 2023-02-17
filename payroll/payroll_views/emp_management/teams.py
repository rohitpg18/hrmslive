from account.account_views.dependencies.basic_functions import *

class Team(View):
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        
        teams= Teams.objects.all()
        if not teams.exists():
            messages.warning(request, 'Teams Not Exists')
            return redirect('admin_dashboard')
        
        teams = list(teams)
                
        return render(request,'payroll/emp_management/teams.html',{'teams': teams})