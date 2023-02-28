from account.account_views.dependencies.basic_functions import *



class ApplyLeave(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        
        user_id = request.user.id
        
        leave_count=monthly_leave_count(user_id)
        if leave_count is None:
            return redirect('self_leave')
            
        data={
            "current_month": (str(create_month_year_formate())[0:-4] + ' ' + str(create_month_year_formate())[-4:]),
            "leave_count":leave_count
        }
        
        return render(request,'account/self_services/self_leave.html',data)
    
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request, *args, **kwargs):
        user_id = request.user.id 
        
        leave_data = request.POST
        
        
        number_of_days = request.POST.get('no_of_days')
        leave_type = request.POST.get("type")
        
        
        leave_application = LeaveApplication.objects.filter(start_date__gte=leave_data["start_date"], start_date__lte=leave_data["end_date"],end_date__gte=leave_data["start_date"], end_date__lte=leave_data["end_date"])
            
            
        if not leave_application.exists() :
            
            leave= LeaveApplication.objects.create(emp_user_id = user_id,start_date = leave_data["start_date"],end_date = leave_data["end_date"],no_of_days = number_of_days,type = leave_type,reason = leave_data["reason"])
            
            if leave_data["start_date_is_half"] == "True":
                leave.start_date_is_half = True
                
                if leave_data["start_date_is_first_half"] == "True":
                    leave.start_date_is_first_half = True
                else:
                    leave.start_date_is_first_half = False
                
                if leave_data["start_date_is_first_half"] == "False":
                    leave.start_date_is_second_half = True
                else:
                    leave.start_date_is_second_half = False
                    
            else:
                leave.start_date_is_half = False
                
                
            if leave_data["end_date_is_half"] == "True":
                leave.end_date_is_half = True
                
                if leave_data["end_date_is_first_half"]== "True":
                    leave.end_date_is_first_half = True
                else:
                    leave.end_date_is_first_half = False
                
                if leave_data["end_date_is_first_half"] == "False":
                    leave.end_date_is_first_half = True
                else:
                    leave.end_date_is_first_half = False
                    
            else:
                leave.end_date_is_half = False
                
            attachment_doc= request.FILES.get("attachment_doc")
            
            if attachment_doc is not None:
                leave.attachment_doc = attachment_doc
                
            leave_count = LeaveCount.objects.filter(month=get_month_year(), emp_user_id=user_id)
            
            if leave_type == 'SL':
                sl_count = leave_count[0].sl_count - float(number_of_days) 
                leave_count.update(sl_count=sl_count)
            elif leave_type == 'CL':
                cl_count = leave_count[0].cl_count - float(number_of_days)
                leave_count.update(cl_count=cl_count)
            elif leave_type == 'PL':
                pl_count = leave_count[0].pl_count - float(number_of_days)
                leave_count.update(pl_count=pl_count)
            leave.save()
            
            messages.success(request, "your leave application submitted successfully")
            
        else:
            messages.warning(request, "You have already\n applied for leave between these dates")
        
        return redirect('self_leave')
    
class LeavesHistory(View):
    
    @method_decorator(login_required(login_url='login'))
    def get (self, request, *args, **kwargs):
        
        user_id = request.user.id 
        
        leave_history = LeaveApplication.objects.filter(emp_user_id = user_id)
        
        context = {
            'leave_history':leave_history
        }
        
        
        return render (request, 'account/self_services/leave_history.html', context)
