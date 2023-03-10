from account.account_views.dependencies.basic_functions import *
from django.core.paginator import Paginator


class EmployeeList(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):

        department_name = request.GET.get('department_name')

        employees = User.objects.all()

        if department_name:
            employees = employees.filter(user_basics__department__department_name__icontains=department_name)
            
        paginator = Paginator(employees, per_page=10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        total_pages = page_obj.paginator.num_pages

        context = {
            "employees": page_obj,
            "departments": Department.objects.all(),
            "last_page": total_pages,
            "paginator": paginator,
        }

        return render(request, 'payroll\emp_management\employee_list.html', context)

