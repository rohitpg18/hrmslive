from account.account_views.dependencies.basic_functions import *
from .models import User
from import_export import resources
from .models import *
from account.models import *

class UserResouce(resources.ModelResource):
    class Meta:
        models = User

class UserBasicDetailsResouce(resources.ModelResource):
    class Meta:
        models = UserBasicDetails

class DesignationResouce(resources.ModelResource):
    class Meta:
        models = Designation
        
class DepartmentResouce(resources.ModelResource):
    class Meta:
        models = Department
        
class UserShiftDetailsResouce(resources.ModelResource):
    class Meta:
        models = UserShiftDetails

