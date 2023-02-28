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

        return render(request, 'payroll\emp_management\payroll.html', context)
    
    
class DayBasedSalary(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        employee_details = UserBasicDetails.objects.all()
        total_salary_of_employees = employee_details.aggregate(Sum('salary'))
        
        current_year = date.today().year
        current_month = datetime.now().month
        month_days = get_end_date_of_month(current_year, current_month).date().day
        
        per_salary_paid_by_company_to_employees = round((total_salary_of_employees['salary__sum']/month_days))
        
        
        department_wise_total_amount_of_salary = employee_details.filter(department__department_name__icontains = "testing").aggregate(Sum('salary'))
        
        
        department_wise_per_day_salary = round((department_wise_total_amount_of_salary['salary__sum']/month_days))
        
    
       
       
        return HttpResponse(per_salary_paid_by_company_to_employees)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


class Policy(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        
        return render(request, 'payroll\emp_management\policy.html')
    


    
        