from account.account_views.dependencies.basic_functions import *



class HrAnalytics(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        data=[]
        
        users= User.objects.all().count()
        
        attendance = DailyAttendance.objects.filter(date= datetime.today(),is_present=True).count()
        leave = DailyLeave.objects.filter(date= datetime.today()).count()
        
        
        show= {
            "total":users,
            "present":attendance,
            "leave":leave,
            'absent':users - (attendance + leave),
            'data':[attendance,leave,users - (attendance + leave)]
        }
        
        
        
        
        
        return render(request,'payroll/hr_analytics/hr_analytics.html',show)
