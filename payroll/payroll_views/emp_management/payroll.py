from account.account_views.dependencies.basic_functions import *


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

    


    
        