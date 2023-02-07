from account.account_views.dependencies.basic_functions import *



class LeaveApplications(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        
        user_id = request.user.id
        
        permission = EmployeePermissions.objects.filter(emp_user_id=user_id)
        
        if  not permission.exists():
            return redirect('login')
        else:
            if permission[0].can_approve_leaves == False:
                return redirect('self_details')

        leave_applications= LeaveApplication.objects.filter(is_requested=True,is_approved=False)
        leave_history= LeaveApplication.objects.filter(is_requested=False,is_approved=True)
        
        data={
            "leave_applications": leave_applications,
            "total_applications": LeaveApplication.total_applications(),
            "pending_applications": leave_applications.count(),
            'leave_history':leave_history
        }
        
        
        return render(request,'payroll/emp_management/leave_application_list.html',data)
    

class ApproveLeaves(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):
        
        
        user_id = request.user.id
        
        permission = EmployeePermissions.objects.get(emp_user_id=user_id)
        if permission is None and permission.can_approve_leaves == False:
            return redirect('self_details')
        
        leave_application = LeaveApplication.objects.filter(id=pk)
        
        
        if not leave_application.exists():
            messages.error(request, 'Leave application not found')
            return redirect('leave_applications')
        else:
            leave_application = LeaveApplication.objects.get(id=pk)
        
        print(leave_application.start_date)
        
        emp_id = leave_application.emp_user     
        
        now=datetime.now()
        month_name= str(now.strftime('%B')) + str(now.year)
        
        month= Month.objects.get(month_name=month_name)
        
        if month is None:
            month= Month.objects.create(month_name=month_name)
        
        leave_count= LeaveCount.objects.get(emp_user_id=emp_id,month=month)
        

        data={
            "current_month": str(now.strftime('%B')) +" "+ str(now.year),
            "leave_count":leave_count,
            "leave_application":leave_application,
            "start_date": leave_application.start_date.strftime("%Y-%m-%d"),
            "end_date": leave_application.end_date.strftime("%Y-%m-%d")
                        
        }
        
        return render(request,'payroll/emp_management/approve_leave.html',data)
    
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request, pk):
        
        
        user_id = request.user.id 
        permission = EmployeePermissions.objects.get(emp_user_id=user_id)
        if permission is None and permission.can_approve_leaves == False:
            return redirect('self_details')
        
        leave_data = request.POST
        
        
        
        number_of_days = request.POST.get('no_of_days')
        
        
        leave = LeaveApplication.objects.get(id=pk)
            
            
        if leave is not None :
            
            leave.is_requested= False
            leave.approved_by_id= user_id
            leave.is_approved= True
            leave.save()
            
            
            daterange = pd.date_range(leave_data["start_date"], leave_data["end_date"])
            
            for single_date in daterange:
                
                start_date_is_half= False
                start_date_is_first_half= False
                start_date_is_second_half= False
                
                end_date_is_half= False
                end_date_is_first_half= False
                end_date_is_second_half= False
                
                if leave.start_date_is_half:
                    start_date_is_half= True
                    
                    if leave.start_date_is_first_half:
                        
                        start_date_is_first_half = True
                        
                    if leave.start_date_is_second_half:
                        start_date_is_second_half= True
                        
                
                if leave.end_date_is_half:
                    
                    end_date_is_half= True
                    
                    if leave.end_date_is_first_half:
                        end_date_is_first_half = True
                        
                    if leave.start_date_is_second_half:
                        end_date_is_second_half= True
                        
                
                if single_date == daterange[0] or daterange[0] == daterange[-1]:
                    DailyLeave.objects.create(emp_user=leave.emp_user,leave_application=leave,date=single_date,date_is_half=start_date_is_half,
                                            date_is_first_half=start_date_is_first_half,date_is_second_half=start_date_is_second_half)
                
                elif single_date == daterange[-1]:
                    DailyLeave.objects.create(emp_user=leave.emp_user,leave_application=leave,date=single_date,date_is_half=end_date_is_half,
                                            date_is_first_half=end_date_is_first_half,date_is_second_half=end_date_is_second_half)
                    
                else:
                    DailyLeave.objects.create(emp_user=leave.emp_user,leave_application=leave,date=single_date)
            

            messages.success(request, "leave application approved")
            return redirect('leave_applications')
            
        else:
            messages.warning(request, "Invalid Operation")
            return redirect('leave_applications')
        
        return redirect('leave_applications')
