from account.account_views.dependencies.basic_functions import *

class PayrollData(View):
    
    def get (self, request):
        
        salary = Salary.objects.all()
        
        context = {'salary':salary}
        
        return render (request, 'payroll\emp_management\payroll.html', context )
    
    
def filter_salary (request):
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        username = request.POST.get('username')
        month = request.POST.get('month')
        
        
        
        salary = Salary.objects.all()
        
        if name:
            salary = salary.filter(Q(emp_user__first_name__icontains = name) | Q(emp_user__last_name__icontains = name))
        
        if username:
            salary = salary.filter(emp_user__username__icontains = username)
            
        if month:
            salary = salary.filter(month__month_name__icontains = month)
            
        context = {
            'salary':salary,
        }
        
        print(name)
        print(username) 
        print(salary)
        
        return render (request, 'payroll\emp_management\payroll.html',context)
    
    elif request.method == 'GET':
        
        return render (request, "payroll\emp_management\salary_filter.html", {'months' : Month.objects.all()})
    
    else:
        return HttpResponse('An Exception Occurred')
    
        