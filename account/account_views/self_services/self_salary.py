from account.account_views.dependencies.dependencie import *
from account.account_views.dependencies.basic_functions import *

    
class SalaryMonthlyData(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user_id = request.user.id
        month_attendance_counter(user_id= user_id, month_name = 0)
        salary_slip(user_id = user_id , month_name= 0)
        
        data ={
            "salary_details": list(Salary.objects.filter(emp_user_id=user_id))[0:-1],
            "basic_details" : UserBasicDetails.objects.get(emp_user_id=user_id),
            "additional_details": UserAdditionalDetail.objects.get(emp_user_id=user_id)
              }

        return render(request, "account/self_services/self_salary.html", data)
    

class SalarySlip(View):

    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):

        month_attendance_counter(user_id=request.user.id, month_name=0)
        salary_slip(user_id=request.user.id, month_name=0)

        salary_details = Salary.objects.get(id=pk)

        emp_id = salary_details.emp_user_id

        basic_details = UserBasicDetails.objects.get(emp_user_id=emp_id)
        additional_details = UserAdditionalDetail.objects.get(
            emp_user_id=emp_id)

        user_sal = Decimal(basic_details.salary)
        month_format = salary_details.month.month_name[0:-
                                                       4] + ' ' + salary_details.month.month_name[-4:]

        gross_sal = round((user_sal/Decimal(1.12)), 2)

        if gross_sal <= 15000:
            gross_sal = gross_sal
        else:
            gross_sal = user_sal - 1800

        if basic_details.is_salaried == False:
            gross_sal = user_sal

        basic = round((Decimal(0.50) * user_sal), 2)
        hra = round((Decimal(0.20) * user_sal), 2)
        conveyance = round((Decimal(0.20) * user_sal), 2)
        utility = round((Decimal(0.10) * user_sal), 2)

        if gross_sal >= 15000:
            pf_employee_1 = round(Decimal(1800), 2)
        else:
            pf_employee_1 = round((gross_sal * Decimal(0.12)), 2)

        data = {
            "salary_details": salary_details,
            "basic_details": basic_details,
            "additional_details": additional_details,
            'basic_salary1': basic,
            'hra1': hra,
            'conveyance_allowance1': conveyance,
            'utility_allowance1': utility,
            'gross1': gross_sal,
            'pf_employee1': pf_employee_1,
            'current_month': month_format
        }

        return render(request, "account/self_services/salary_slip.html", data)
        
