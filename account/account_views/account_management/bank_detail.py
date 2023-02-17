from account.account_views.dependencies.basic_functions import *

    
class BankDetail(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        user_id = request.user.id
        
        redirect_url = is_profile_complete(user_id)
        
        if  redirect_url == "bank_details":
                
            return render(request, "account/profile_complete/bank_details.html")
        else:
            return redirect(redirect_url)
        
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        user_id = request.user.id
        
        bank_name = request.POST.get('bank_name')
        branch_name = request.POST.get('branch_name')
        account_type = request.POST.get('account_type')
        ifsc_code = request.POST.get('ifsc_code')
        account_number = request.POST.get('account_number')
        
        bank_details = UserBankDetail.objects.get(emp_user_id=user_id)
        
        if bank_details is None:
            bank_details = UserBankDetail.objects.create(emp_user_id=user_id)
        
        bank_details.bank_name = bank_name
        bank_details.branch_name = branch_name
        bank_details.account_type = account_type
        bank_details.ifsc_code = ifsc_code
        bank_details.account_number = account_number
        bank_details.is_completed_bank_details = True
        
        bank_details.save()
        
        messages.success(request,"Bank Details added successfully")

        return redirect(is_profile_complete(user_id))
        
        
        