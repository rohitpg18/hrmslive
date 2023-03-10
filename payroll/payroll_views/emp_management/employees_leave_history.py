from account.account_views.dependencies.basic_functions import *
from django.core.paginator import Paginator

class EmployeeLeavesHistory(View):
    
    @method_decorator(login_required(login_url='login'))
    def get (self, request, *args, **kwargs):
        
        all_active_users = User.objects.filter(is_active = True)
        
        for user in all_active_users:
            monthly_leave_count(user_id=user.id)
        
        leave_history = LeaveApplication.objects.all().order_by('is_approved')
        
        paginator = Paginator(leave_history, per_page=10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        total_pages = page_obj.paginator.num_pages
        
        context = {
            'leave_history':page_obj,
            "last_page": total_pages,
            "paginator": paginator,
        }
        
        
        return render (request, 'payroll/emp_management/employees_leave_history.html', context)