from django.contrib import admin
from payroll.models import *

# Register your models here.

admin.site.register(Month)
admin.site.register(MonthAttendanceCounter)
admin.site.register(Holiday)
admin.site.register(DailyAttendance)
admin.site.register(MissingAttendance)
admin.site.register(LeaveApplication)
admin.site.register(DailyLeave)
admin.site.register(LeaveCount)
admin.site.register(Salary)
