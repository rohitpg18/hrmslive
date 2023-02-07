from account.account_views.dependencies.basic_functions import *


class SelfDetail(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user_id = request.POST.get('user')
        is_profile_complete(user_id)
        
        
        user_id = request.user.id
        
        data= {
            "basic_detail": UserBasicDetails.objects.get(emp_user_id=user_id),
            "additional_detail":UserAdditionalDetail.objects.get(emp_user_id=user_id),
            "educational_details": UserEducationDetails.objects.get(emp_user_id=user_id),
            "bank_detail": UserBankDetail.objects.get(emp_user_id=user_id),
            
            
        }
        
        return render(request,'account/self_services/self_details.html',data)
    