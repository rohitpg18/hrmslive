from account.account_views.dependencies.basic_functions import *

class PayrollData(View):
    def get (self, request, *args, **kwargs):
        
        salary = Salary.objects.all()
        
        return render (request, 'payroll\emp_management\payroll.html', {'sal':salary})