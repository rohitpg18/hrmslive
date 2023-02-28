from account.account_views.dependencies.basic_functions import *

class EmployeeLeavesHistory(View):
    
    @method_decorator(login_required(login_url='login'))
    def get (self, request, *args, **kwargs):
        
        leave_history = LeaveApplication.objects.all().order_by('is_approved')
        
        context = {
            'leave_history':leave_history
        }
        
        
        return render (request, 'payroll/emp_management/employees_leave_history.html', context)