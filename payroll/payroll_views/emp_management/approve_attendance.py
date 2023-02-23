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
            
            
        if len(emp_list) < 1:
            messages.warning(request, "Daily attendance applications not available")
            
            return redirect('team_leader_dashboard')    
        
        data={
            'employees':emp_list,
            'employees_count': len(emp_list)
        }

        return render(request, 'payroll/emp_management/approve_attendance.html', data)

    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        application_id = request.POST.get('application_id')
        daily_attendance = DailyAttendance.objects.filter(id=application_id).exists()
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

#Attendance List of all Users, shows only to HR

class AttendanceList(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):

        department_name = request.GET.get('department_name')

        employees = User.objects.all()

        if department_name:
            employees = employees.filter(
                user_basics_departmentdepartment_name_icontains=department_name)

        context = {
            "employees": employees,
            "departments": Department.objects.all()
        }

        return render(request, 'payroll/emp_management/attendanceList_allUsers.html', context)


class AttendanceHistoryEmp(View):
    @method_decorator(login_required(login_url='login'))
    def get (self, request, pk):
       
        month_format = str(get_month_year())
        month_name = month_format[0:-4] + ' ' +  month_format[-4:]
        
    
        months = {month: index for index, month in enumerate(month_abbr) if month}
        month = int(months[month_format[0:3]])
        year = int(month_format[-4:])
        end_date = get_end_date_of_month(year, month)
        first_date = end_date.replace(day = 1).date()
        
        
        monthly_data= []
        
        date_range= pd.date_range(first_date,end_date)
        current_date= datetime.today().date()
        
        for date in date_range:
        
            if date.date() > current_date:
                break
        
            
            data= {
                'date': date.strftime("%d-%m-%Y"),
                'day':date.strftime("%a"),
                'status' :None,
                'login_time':None,
                'logout_time':None,
            }
            
            
            if Holiday.objects.filter(date=date).exists():
                
                data["status"]="H"
                data["login_time"]="-"
                data["logout_time"]="-"
                
            
            elif data["day"]== "Sat" or data["day"]== "Sun":
                data["status"]="WO"
                data["login_time"]="-"
                data["logout_time"]="-"

            else:
                leave = DailyLeave.objects.filter(emp_user__username = pk, date=date)
                attendance = DailyAttendance.objects.filter(emp_user__username = pk, date=date, is_present=True)
                print(f"{attendance} today ")
                if  leave.exists() and attendance.exists():
                    
                    if leave[0].date_is_half == True:
                        
                        if leave[0].date_is_first_half== True and attendance[0].is_second_half== True:
                            data["status"]="FHL SHP"
                            data["login_time"]= attendance[0].login_time
                            data["logout_time"]= attendance[0].logout_time
                            
                        
                        if leave[0].date_is_second_half== True and attendance[0].is_first_half== True:
                            data["status"]="FHP SHL"
                            data["login_time"]= attendance[0].login_time
                            data["logout_time"]= attendance[0].logout_time
            
                    else:
                        data["status"]="L"
                        data["login_time"]="-"
                        data["logout_time"]="-"
                        
                        
                elif leave.exists():
                    
                    if leave[0].date_is_half== True:
                        
                        if leave[0].date_is_first_half== True:
                            data["status"]="FHL SHA"
                        
                        elif leave[0].date_is_second_half== True:
                            data["status"]="FHA SHL"
                            
                    else:
                        data["status"]="L"
                        data["login_time"]="-"
                        data["logout_time"]="-"
            
                    
                elif attendance.exists():
                    
                    if attendance[0].is_half_day == True:
                    
                        if attendance[0].is_first_half== True:
                            data["status"]="FHP SHA"
                            data["login_time"]= attendance[0].login_time
                            data["logout_time"]= attendance[0].logout_time
                        
                        if attendance[0].is_second_half== True:
                            data["status"]="FHA SHP"
                            data["login_time"]= attendance[0].login_time
                            data["logout_time"]= attendance[0].logout_time
                        
                    else:
                        data["status"]="P"
                        data["login_time"]= attendance[0].login_time
                        data["logout_time"]= attendance[0].logout_time
                            
                                    
                else:
                    
                    
                    data["status"]="AB"
                    data["login_time"]="-"
                    data["logout_time"]="-"
                        
                
            
            monthly_data.append(data)
            
    
        
        return render (request, "payroll/emp_management/emp_attendance_history.html", {'monthly_data':monthly_data, 'month':month_name})
    
    
class TodayAttendanceList(View):
    
    def get(self, request, *args, **kwargs):

        department_name = request.GET.get('department_name')
      

        present_users = DailyAttendance.objects.all()
        
        present_users = present_users.filter(date = datetime.now().date())

        if department_name:
            present_users = present_users.filter(emp_user__user_basics__department__department_name__icontains=department_name)

        context = {
            "present_users" : present_users,
            "departments" : Department.objects.all(),
        }

        return render(request, 'payroll/emp_management/today_attendance_list.html', context)