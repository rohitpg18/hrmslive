from account.account_views.dependencies.basic_functions import *


class EmployeeList(View):
    
    
    def post(self, request):
        
        # department_name = request.POST.get('department_name')
        
        # employees = User.objects.all()
        
        # if department_name:
        #     employees = employees.filter(user_basics__department__department_name__icontains = department_name)
            
        # context = {
        #     "employees" : employees
        # }
            
        # return render (request, 'payroll\emp_management\employee_list.html', context)
        pass
        
    
    def get(self, request, *args, **kwargs):
        
        department_name = request.GET.get('department_name')
        
        employees = User.objects.all()
        
        if department_name:
            employees = employees.filter(user_basics__department__department_name__icontains = department_name)
            
        context = {
            "employees" : employees,
            "departments":Department.objects.all()
        }
        
        
        return render (request, 'payroll\emp_management\employee_list.html', context)



def EmpActivate(request, emp_id):
    emp = User.objects.get(id=emp_id)
    emp.is_active = True
    emp.save()
    return redirect("all_users")

def EmpDeactivate(request, emp_id):
    emp = User.objects.get(id=emp_id)
    emp.is_active = False
    emp.save()
    return redirect("all_users")