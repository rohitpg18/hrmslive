from account.account_views.dependencies.basic_functions import *


class EmployeeList(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):

        department_name = request.GET.get('department_name')

        employees = User.objects.all()

        if department_name:
            employees = employees.filter(
                user_basics__department__department_name__icontains=department_name)

        context = {
            "employees": employees,
            "departments": Department.objects.all()
        }

        return render(request, 'payroll\emp_management\employee_list.html', context)

