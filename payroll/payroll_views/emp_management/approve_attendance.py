from account.account_views.dependencies.basic_functions import *

class ApproveAttendance(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        user_id = request.user.id
        date = datetime.today().date()
        
        team = Teams.objects.filter(leader_name_id=user_id)
        
        if not team.exists():
            messages.warning(request, 'team does not exists')
            return redirect('self_details')
        else:
            team = Teams.objects.get(leader_name_id=user_id)
        team_employees =team.employees.all()
        
        emps_list=[]
        
        for emp in team_employees:
            if DailyAttendance.objects.filter(emp_user=emp,is_requested=True,date=date).exists():
                emps_list.append(DailyAttendance.objects.get(emp_user=emp,date=date))
        
        data={
            'employees':emps_list,
            'employees_count': len(emps_list)
            }
        
        
        
        return render(request,'payroll/emp_management/approve_attendance.html',data)
    
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        application_id = request.POST.get('application_id')
        daily_attendance= DailyAttendance.objects.filter(id=application_id).exists()
        if daily_attendance:
            application=DailyAttendance.objects.get(id=application_id)
            application.approved_by_id= request.user.id
            application.is_present=True
            application.is_requested=False
            application.save()
            messages.success(request, "daily attendance approved successfully") 
        else:
            messages.error(request, 'daily attendance application not found')
        return redirect('attendance_applications')