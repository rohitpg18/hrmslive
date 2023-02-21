from account.account_views.dependencies.basic_functions import *


class ApproveAttendance(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):

        user_id = request.user.id
        date = datetime.today().date()

        teams = Teams.objects.filter(leader_name_id=user_id)

        if not teams.exists():
            messages.warning(request, 'team does not exists')
            return redirect('self_details')
        else:
            teams = Teams.objects.filter(leader_name_id=user_id)

        team_employees = set()

        for team in teams:
            team_employees = team_employees.union(
                team.employees.values_list('id', flat=True))

        emp_list = set()

        for emp_id in team_employees:
            emp_list=emp_list.union(DailyAttendance.objects.filter(emp_user_id=emp_id,is_requested=True))
            
            
        if len(emp_list) <= 0:
            messages.warning(request, "Daily attendance applications not available")
            return redirect('admin_dashboard')
        
        data={
            'employees':emp_list,
            'employees_count': len(emp_list)
        }

        return render(request, 'payroll/emp_management/approve_attendance.html', data)

    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        application_id = request.POST.get('application_id')
        daily_attendance = DailyAttendance.objects.filter(
            id=application_id).exists()
        if daily_attendance:
            application = DailyAttendance.objects.get(id=application_id)
            application.approved_by_id = request.user.id
            application.is_present = True
            application.is_requested = False
            application.save()
            messages.success(request, "daily attendance approved successfully")
        else:
            messages.error(request, 'daily attendance application not found')
        return redirect('attendance_applications')
