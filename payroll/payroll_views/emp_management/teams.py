from account.account_views.dependencies.basic_functions import *
from django.shortcuts import get_object_or_404
from payroll.forms import TeamsForm

class Team(View):
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        
        teams= Teams.objects.all()
        if not teams.exists():
            messages.warning(request, 'Teams Not Exists')
            return redirect('admin_dashboard')
        
        teams = list(teams)
                
        return render(request,'payroll/emp_management/teams.html',{'teams': teams})
    
    
class AddTeam(View):
    template_name = "payroll/emp_management/add_team.html"
    @method_decorator(login_required(login_url='login'))
    def get(self ,request):

        user_id = request.user.id
        
        current_user = EmployeePermissions.objects.get(emp_user_id=user_id)
        
        if current_user is not None and current_user.can_manage_teams:

            team_leaders = UserBasicDetails.objects.filter(designation__designation_name__iendswith='Leader')

            team_members = User.objects.all()

            context = {
                'team_leaders': team_leaders ,
                'team_members' : team_members ,
            }
            print(context["team_leaders"])
            return render (request, self.template_name , context)

        else:
             return HttpResponse("sorry you don't have permission")


    def post(self, request):
       
        name_of_team = request.POST.get("team_name")
        name_of_tl = request.POST.get('tl_name')
        print(f"this will get from post {name_of_tl}")
        
        name_of_team_members = [x.username for x in User.objects.all()]
        print(f'name = {name_of_team_members}')
        
        emp_ids = []
        for x in name_of_team_members:
            emp_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        print(emp_ids)

        create_team = Teams.objects.create(team_name = name_of_team,leader_name_id = name_of_tl)
        for x in emp_ids:
            create_team.employees.add(User.objects.get(id = x))
        return redirect('teams')
    






class UpdateTeam(View):
    
    def get(self, request, id):
        

        data={
            "team": Teams.objects.get(id=id),
            'employees':User.objects.all()
        }
    
        return render(request, 'payroll/emp_management/update_team.html',data) 
        
    def post(self, request, id):
        
        data = request.POST
        
        team = Teams.objects.filter(id=id)
        
        if data['is_active'] == "Activate":
            active = True
        else:
            active = False
        
        team.update(team_name= data['team_name'],leader_name=data['leader_name'],is_active=active)

        

        if not team.exists():
            messages.error(request,'Team not found')
            return redirect('teams')
        
        for emp in team[0].employees.all():
            team[0].employees.remove(emp)
        
        
        for key, value in data.items():
        
            
            if data[key] == "True":
                a = User.objects.get(username=key)
                team[0].employees.add(a)
        messages.success(request,'Team Update successfully')
        
        return redirect('teams')