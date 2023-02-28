from account.account_views.dependencies.basic_functions import *



class HrAnalytics(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        data=[]
        
        users= User.objects.all()
        
        
        salaries= UserBasicDetails.objects.values_list("emp_user","salary")
        
        
        emp_names= []
        emp_salary= []
        
        
        
        for user in users:
            
            print(user.user_basics.salary)
            
            emp_names.append(user.get_full_name())
            
            if user.user_basics.salary is None:
                
                emp_salary.append(0)
                
            else:
                emp_salary.append(float(user.user_basics.salary))
            
            
            
        
        users= users.count()
        
        attendance = DailyAttendance.objects.filter(date= datetime.today(),is_present=True).count()
        leave = DailyLeave.objects.filter(date= datetime.today()).count()
        
        
        show= {
            "total":users,
            "present":attendance,
            "leave":leave,
            'absent':users - (attendance + leave),
            'data':[attendance,leave,users - (attendance + leave)],
            'emp_names':emp_names,
            'emp_salary':emp_salary
        }
        
        
        
        
        
        return render(request,'payroll/hr_analytics/hr_analytics.html',show)


def data(request):
    
    data=[]
        
    users= User.objects.all()
        
        
    salaries= UserBasicDetails.objects.values_list("emp_user","salary")
    
    
    emp_names= []
    emp_salary= []
    
    
    
    for user in users:
        
        print(user.user_basics.salary)
        
        emp_names.append(user.get_full_name())
        
        if user.user_basics.salary is None:
            
            emp_salary.append(0)
            
        else:
            emp_salary.append(float(user.user_basics.salary))
        
        
        
    
    users= users.count()
    
    attendance = DailyAttendance.objects.filter(date= datetime.today(),is_present=True).count()
    leave = DailyLeave.objects.filter(date= datetime.today()).count()
    
    
    show= {
        "total":users,
        "present":attendance,
        "leave":leave,
        'absent':users - (attendance + leave),
        'data':[attendance,leave,users - (attendance + leave)],
        'emp_names':emp_names,
        'emp_salary':emp_salary
    }

    return JsonResponse({'data':show})