from account.account_views.dependencies.basic_functions import *


class AdminDashboard(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        return render(request, 'payroll/admin_dashboards/admin_dashboard.html')