from account.account_views.dependencies.basic_functions import *



class HrAnalytics(View):
    
    def get(self, request):
        
        
        return render(request,'payroll/hr_analytics/hr_analytics.html')
