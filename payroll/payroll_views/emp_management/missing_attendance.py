from account.account_views.dependencies.basic_functions import *

class MissingAttendanceApplications(View):
    
    def get(self, request):
        
        user_id = request.user.id
                
        is_permission = request.user.employee_permissions_user.can_approve_leaves
        
        print(is_permission)    
        
        if is_permission:
            
            applications= MissingAttendance.objects.filter(is_requested=True)
            
            return render(request, "payroll/emp_management/missing_attendance.html",{'applications': applications})
            
            
        else:
            return redirect('self-details')
        
        