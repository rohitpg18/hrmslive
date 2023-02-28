from account.account_views.dependencies.basic_functions import *



class VerifyDetails(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        if request.user.employee_permissions_user.can_verify_emp_details == False:
            messages.warning(request, "You don't have permission")
            return redirect('ems_dashboard')
        
        verify_emp_list = UserBasicDetails.objects.filter(is_requested=True,is_verify=False)
        if verify_emp_list.count() < 0:
            messages.warning(request, 'applications not found')
            return redirect('ems_dashboard')
        

        
                
        return render(request,'payroll/emp_management/verify_details.html',{'verify_emp_list':verify_emp_list})
    
    @method_decorator(login_required(login_url='login'))
    def post(self,request):
        
        
        user_id = request.POST.get('user_id')
        
        if user_id is None:
            messages.warning(request, 'applications not found')
            return redirect('verify_details')
        
        user_details= UserBasicDetails.objects.get(emp_user_id=user_id)

        
        if user_details is None:
            messages.warning(request, 'applications not found')
            return redirect('verify_details')
        
        user_details.is_requested= False
        
        user_details.is_verify= True
        user_details.is_approved= True
        user_details.is_active= True
        user_details.approved_by= request.user
        user_details.save()
        
        messages.success(request, 'User details verified successfully')
        return redirect('verify_details')
        
        
        
            