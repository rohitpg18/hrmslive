# user login ,profile completion, account creation
from account.account_views.account_management.login import *
from account.account_views.account_management.create_account import *
from account.account_views.account_management.additional_detail import *
from account.account_views.account_management.bank_detail import *
from account.account_views.account_management.educational_detail import *


# user self services
from account.account_views.self_services.self_detail import *
from account.account_views.self_services.self_leave import *
from account.account_views.self_services.self_attendance import *
from account.account_views.self_services.self_salary import *


def error_404(request,exception):
    return render(request,'page_not_found.html')


