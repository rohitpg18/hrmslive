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

    def get(self ,request):

        user_id = request.user.id
        
        current_user = EmployeePermissions.objects.get(emp_user_id=user_id)
        
        if current_user is not None and current_user.can_manage_teams:

            team_leaders = UserBasicDetails.objects.filter(designation__designation_name__iendswith='Leader')

            team_members = User.objects.all()

            context = {
                'team_leaders': team_leaders ,
                'team_members' : team_members
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
    
class DeleteTeam(View):

    def get(self, request, id):
        team =Teams.objects.get(id=id)
            
        if team is not None:
                team.delete()
                
                messages.success(request, 'team deleted successfully')   
                return redirect('teams')
            
        else:
                messages.error(request, 'teams not found')
                return redirect('teams')
            
            

    
    
    
class UpdateTeam(View):

    def get(self, request, id):

        team = Teams.objects.get(id=id)

        seleted_team_members= team.employees.all()
        # print(f' members = {seleted_team_members.user_id}')

        team_leaders = UserBasicDetails.objects.filter(designation__designation_name__iendswith='Leader')

        team_members = User.objects.all()
        

        return render(request, 'payroll/emp_management/update_team.html' , {'team' : team, 'team_leaders' : team_leaders, 'team_members' : team_members,"seleted_team_members":seleted_team_members})

    def post(self, request, id):

        team = Teams.objects.get(id=id) 

        team.team_name = request.POST.get("team_name")
        team.leader_name_id = request.POST.get('tl_name')
        team.employees = [x.username for x in User.objects.all()]
        print(f'name = {team.employees}')
        emp_ids = []
        for x in team.employees:
            emp_ids.append(int(request.POST.get(x))) if request.POST.get(x) else print("")
        print(emp_ids)
        team.save()

        # create_team = Teams.objects.create(team_name = team.name_of_team,tl_name_id = team.name_of_tl)
        # for x in emp_ids:
        #     create_team.employees.add(User.objects.get(id = x))
        # print(create_team)   

        # return render(request, 'accounts/user_data/team_list.html' , {'team' : team})
        return redirect("teams")
            
# def UpdateView(request,id,*args,**kwargs):
#     context = {}
    
#     obj = get_object_or_404(Teams,id=id)
    
#     form=TeamsForm(request.POST or None,instance=obj)  
    
#     if form.is_valid():
#         form.save()
#         return HttpResponse("Save")
#     context['form'] = form
    
#     return render(request, 'payroll/emp_management/update_team.html',context)