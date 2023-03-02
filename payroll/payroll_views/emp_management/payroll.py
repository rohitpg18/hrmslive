from account.account_views.dependencies.basic_functions import *
from django.db.models import Sum



class PayrollData(View):

    @method_decorator(login_required(login_url='login'))
    def get(self, request):

        name = request.GET.get('name')
        username = request.GET.get('username')
        month = request.GET.get('month')

        salary = Salary.objects.all()

        if name:
            salary = salary.filter(Q(emp_user__first_name__icontains=name) | Q(
                emp_user__last_name__icontains=name))

        if username:
            salary = salary.filter(emp_user__username__icontains=username)

        if month:
            salary = salary.filter(month__month_name__icontains=month)

        context = {
            'salary': salary,
            'months': Month.objects.all(),
        }

        return render(request, 'payroll/emp_management/payroll.html', context)
    
    
class DayBasedSalary(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        employee_details = UserBasicDetails.objects.all()

        current_year = date.today().year
        current_month = datetime.now().month
        month_days = get_end_date_of_month(current_year, current_month).date().day
        
        per_day_salary_paid_by_company_to_employees = round((employee_details.aggregate(Sum('salary'))['salary__sum']/month_days))
        
        department_name = request.GET.get('department')
        
        department_wise_filter = employee_details.filter(department__department_name__icontains = "back")
        
        if department_name:      
            department_wise_filter = employee_details.filter(department__department_name__icontains = department_name)
            
        
        department_wise_per_day_salary = round((department_wise_filter.aggregate(Sum('salary'))['salary__sum']/month_days))

        context = {"salary":employee_details, 
                   "month_days":month_days, 
                   "total_per_day_salary":per_day_salary_paid_by_company_to_employees, 
                   "department_wise_per_day_salary":department_wise_per_day_salary, 
                   "departments":Department.objects.all(), 
                   "dept_name":department_wise_filter[0].department.department_name, 
                   "department_wise_filter":department_wise_filter}
        
        return render (request, "payroll/emp_management/day_based_salary.html", context )
    
class DepartmentBasedSalary(View):
    
    def get(self, request):
        
        user_department = UserBasicDetails.objects.all()
        
        
        context = {
        'back_end_development_salary' : user_department.filter(department__department_name = "Back End Development").aggregate(Sum('salary'))["salary__sum"],
        'software_testing_salary' : user_department.filter(department__department_name = "Software Testing").aggregate(Sum('salary'))["salary__sum"],
        'sap_salary' : user_department.filter(department__department_name = "SAP MM").aggregate(Sum('salary'))["salary__sum"],
        'hr_salary' : user_department.filter(department__department_name = "Human Resource").aggregate(Sum('salary'))["salary__sum"]}
        
        
        return render(request, "payroll/emp_management/department_based_salary.html", context)
    
class TimeBasedSalary(View):
    
    salary_paid_till_date = Salary.objects.all().aggregate()
        
        
    

                                                        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


class Policy(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        
        return render(request, 'payroll/emp_management/policy.html')
    


    
        