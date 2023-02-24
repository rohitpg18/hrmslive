from account.account_views.dependencies.basic_functions import *



class HrAnalytics(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        data=[85,10,5]
        
        users= User.objects.all().count()
        
        attendance = DailyAttendance.objects.filter(date= datetime.today(),is_present=True).count()
        leave = DailyLeave.objects.filter(date= datetime.today()).count()
        
        data[0]= attendance
        data[1]= leave
        data[2]= users - (attendance+ leave)
        
        
        
        
        return render(request,'payroll/hr_analytics/hr_analytics.html',{'data':data})
