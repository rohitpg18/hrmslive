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
        'hr_salary' : user_department.filter(department__department_name = "Human Resource").aggregate(Sum('salary'))["salary__sum"]
        }
        
        
        return render(request, "payroll/emp_management/department_based_salary.html", context)
    
class TimeBasedSalary(View):
    
    def get(self, request, *args, **kwargs):
        
        salary_paid_till_date_salaried = Salary.objects.filter(emp_user__user_basics__is_salaried = True).exclude(month=get_month_year()).aggregate(Sum('gross_salary'))["gross_salary__sum"]
        
        salary_paid_till_date_intern = Salary.objects.filter(emp_user__user_basics__is_salaried = False).exclude(month=get_month_year()).aggregate(Sum('net_salary'))["net_salary__sum"]
        
        total_salary_paid = salary_paid_till_date_salaried + salary_paid_till_date_intern
        
        department_name = request.GET.get('department')
        

        department_wise_salary_paid_till_date_salaried = Salary.objects.filter(emp_user__user_basics__is_salaried = True, emp_user__user_basics__department__department_name = "Back End Development").exclude(month=get_month_year()).aggregate(Sum('gross_salary'))["gross_salary__sum"]
        
        department_wise_salary_paid_till_date_intern = Salary.objects.filter(emp_user__user_basics__is_salaried = False, emp_user__user_basics__department__department_name = "Back End Development").exclude(month=get_month_year()).aggregate(Sum('net_salary'))["net_salary__sum"]
        
        if department_name:
            
            department_wise_salary_paid_till_date_salaried = Salary.objects.filter(emp_user__user_basics__is_salaried = True, emp_user__user_basics__department__department_name = department_name ).exclude(month=get_month_year()).aggregate(Sum('gross_salary'))["gross_salary__sum"]
            if department_wise_salary_paid_till_date_salaried is None:
                department_wise_salary_paid_till_date_salaried = 0
                
            department_wise_salary_paid_till_date_intern = Salary.objects.filter(emp_user__user_basics__is_salaried = False, emp_user__user_basics__department__department_name = department_name).exclude(month=get_month_year()).aggregate(Sum('net_salary'))["net_salary__sum"]
            if department_wise_salary_paid_till_date_intern is None:
                department_wise_salary_paid_till_date_intern = 0
                
        total_salary_paid_to_department = department_wise_salary_paid_till_date_salaried + department_wise_salary_paid_till_date_intern
        
        context = {
            "total_salary_paid": total_salary_paid,
            "departments": Department.objects.all(),
            "total_salary_paid_to_department": total_salary_paid_to_department,
        }
        
        return render (request, "payroll/emp_management/time_based_salary.html", context)
    
class SalariesPaidTillDate(View):
    
    def get(self, request, *args, **kwargs):
        
        
        emp_users = User.objects.all()
        
        users_total_paid_salary = []
        
        for emp_user in emp_users:

            data = {
                "emp_user" : emp_user,
                "paid_salary" : 0
            }
            
            salaries = Salary.objects.all()
            
            if salaries.filter(emp_user = emp_user, emp_user__user_basics__is_salaried = True):
                
                data['paid_salary'] = Salary.objects.filter(emp_user = emp_user, emp_user__user_basics__is_salaried = True).exclude(month=get_month_year()).aggregate(Sum('gross_salary'))["gross_salary__sum"]
                
            elif salaries.filter(emp_user = emp_user, emp_user__user_basics__is_salaried = False):
                
                data['paid_salary'] = Salary.objects.filter(emp_user=emp_user, emp_user__user_basics__is_salaried = False).exclude(month=get_month_year()).aggregate(Sum('net_salary'))["net_salary__sum"]
            
            if data['paid_salary'] == 0:
                continue
                
            users_total_paid_salary.append(data)
            
        context = {            
            "users_total_paid_salary": users_total_paid_salary,
        }
            
        return render (request, "payroll/emp_management/total_salaries_paid_list.html", context)
       
            
        
        
        
        
    

                                                        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


class Policy(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, *args, **kwargs):
        
        return render(request, 'payroll/emp_management/policy.html')
    


    
        