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
        
        bankname = request.POST.get('bank_name')
        branchname = request.POST.get('branch_name')
        accounttype = request.POST.get('account_type')
        ifsccode = request.POST.get('ifsc_code')
        accountnumber = request.POST.get('account_number')
        bank_docs = request.FILES.get('bank_docs')
            
        if bank_docs is not None:
                
            user_document= UserDocument.objects.filter(emp_user_id=user_id,doc_name = "Bank Document")
        
            if user_document.exists():
                user_document[0].doc_file= bank_docs
                user_document[0].save()
                
            else:
                user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Bank Document", doc_file = bank_docs)
        
        bank_details = UserBankDetail.objects.filter(emp_user_id=user_id)
        
        print(bank_details)
        
        if bank_details.count() != 0:
            bank_details.update(emp_user_id=user_id, bank_name=bankname, branch_name=branchname, account_type= accounttype, ifsc_code=ifsccode, account_number=accountnumber, is_completed_bank_details = True)
            
        else:
            bank_details = UserBankDetail.objects.create(emp_user_id=user_id, bank_name=bankname, branch_name=branchname, account_type= accounttype, ifsc_code=ifsccode, account_number=accountnumber, is_completed_bank_details = True)
        

        
        messages.success(request,"Bank Details added successfully")

        return redirect(is_profile_complete(user_id))
        
        
        