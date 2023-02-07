from django.db import models
from django.contrib.auth.models import User

class Month(models.Model):
    month_name = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.month_name
    

class MonthAttendanceCounter(models.Model):
    emp_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='month_attendance_counter_user')
    month = models.ForeignKey(Month,on_delete=models.CASCADE, related_name='month_attendance_counter_month')

    present_days = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)
    absent_days = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)

    week_offs = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)

    paid_leaves = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)
    non_paid_leaves = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)

    paid_holiday = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)
    sand_witched_days = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)
    total_paid_days = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)
    over_time_hours = models.DecimalField(default=0.0, max_digits=4, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username + " " + self.month.month_name
    

class Holiday(models.Model):
    month = models.ForeignKey(Month,on_delete=models.CASCADE, related_name='holiday_month', null=True)
    title = models.CharField(max_length=50)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.title + ' ' + str(self.date)

class DailyAttendance(models.Model):
    emp_user = models.ForeignKey(User,
    on_delete=models.CASCADE, related_name='daily_attendance_user')
    date = models.DateField(auto_now=True)

    month = models.ForeignKey(Month,on_delete=models.CASCADE, related_name='daily_attendance_month')

    approved_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name='daily_attend_approved_by',null=True)

    login_time = models.TimeField(auto_now_add=True)
    logout_time = models.TimeField(null=True)
    working_hours = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)

    is_half_day = models.BooleanField(default=False)
    is_first_half = models.BooleanField(default=False)
    is_second_half = models.BooleanField(default=False)

    is_requested = models.BooleanField(default=False)
    is_present = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.emp_user.username + ' ' + str(self.date)
    
    
    
class MissingAttendance(models.Model):
    emp_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='missing_attendance_users')

    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_attendance_approved_by')
    
    date = models.DateField(auto_now=True)
    description = models.TextField(default="Attendance disappeared for some reason")

    is_half_day = models.BooleanField(default=False)
    is_first_half = models.BooleanField(default=False)
    is_second_half = models.BooleanField(default=False)

    is_requested = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.emp_user.username + ' ' + str(self.date)
    

class LeaveApplication (models.Model):
    emp_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='leave_application_users')
    date_of_apply = models.DateField(auto_now=True)
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    no_of_days = models.DecimalField(default=0.0, max_digits=5, decimal_places=1)
    type = models.CharField(max_length=100)
    reason = models.CharField(max_length=255)
    attachment_doc = models.FileField(upload_to='leave_docs', null=True)

    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='leave_application_approved_by',null=True)
    
    start_date_is_half = models.BooleanField(default=False)
    start_date_is_first_half = models.BooleanField(default=False)
    start_date_is_second_half = models.BooleanField(default=False)
    
    is_requested = models.BooleanField(default=True)
    
    end_date_is_half = models.BooleanField(default=False)
    end_date_is_first_half = models.BooleanField(default=False)
    end_date_is_second_half = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def total_applications():
        return LeaveApplication.objects.all().count()



    def __str__(self):
        return self.emp_user.username + ' ' + self.reason


class DailyLeave (models.Model):
    emp_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='daily_leave_users')
    leave_application = models.ForeignKey(LeaveApplication,on_delete=models.CASCADE,related_name='daily_leave_users')
    # month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name='daily_leave_month')
    date = models.DateField()
    date_is_half = models.BooleanField(default=False)
    date_is_first_half = models.BooleanField(default=False)
    date_is_second_half = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.emp_user.username + ' ' + str(self.date)


class LeaveCount (models.Model):
    emp_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='leave_count_users')
    month = models.ForeignKey(Month,on_delete=models.CASCADE,related_name='leave_count_month')
    sl_count = models.IntegerField(default=0)
    pl_count = models.IntegerField(default=0)
    cl_count = models.IntegerField(default=0)
    lop_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return self.emp_user.username 


class Salary(models.Model):
    emp_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='salary_users')
    month = models.ForeignKey(Month,on_delete=models.CASCADE,related_name='salary_months')
    current_month_ctc = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    basic_salary = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    house_rent_allowance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    conveyance_allowance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    utility_allowance = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bonus = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    pf_employer = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    pf_employee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    profession_tax = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    epf_employer = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    eps_employer = models.DecimalField(max_digits=8,decimal_places=2, default=0)
    ot_pay = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    gross_salary = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__ (self):
        return self.emp_user.username + ' ' + self.month.month_name + ' ' + str(self.net_salary)