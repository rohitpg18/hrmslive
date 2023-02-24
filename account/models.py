from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

class Designation(models.Model):
    designation_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.designation_name
    
class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.department_name
    
class UserShiftDetails(models.Model):
    shift_name = models.CharField(max_length=100, unique=True)
    in_time = models.TimeField()
    out_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.shift_name

class UserBasicDetails(models.Model):
    emp_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_basics')
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, to_field='designation_name',related_name='user_designation_details', null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='department_name',related_name='user_department_details', null=True)
    shift_details = models.ForeignKey(UserShiftDetails, on_delete=models.CASCADE, to_field='shift_name',related_name='user_shift_details', null=True)
    date_of_joining = models.DateField(auto_now=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    uan_number = models.BigIntegerField(null=True)
    pf_number = models.CharField(max_length=10, null=True)
    experience_status = models.CharField (choices=(("Fresher", "Fresher"), ("Experienced", "Experienced")), max_length=50, null=True)
    is_salaried = models.BooleanField(default=True)   #if salaried is True deduction part for employee will be calculated eg. PF.
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    is_requested = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_created_by', null=True)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee_approved_by', null=True)
    is_completed_basic_details = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username
    
class PreviousOrganisationDetail(models.Model):
    emp_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_previous_details')
    experience_in_years = models.IntegerField(null=True)
    previous_organisation = models.CharField(max_length=255, null=True)
    previous_organisation_designation = models.CharField(max_length=100, null=True)
    is_completed_previous_organisation_details = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username
    
class UserAdditionalDetail(models.Model):
    emp_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_additional_details')
    gender = models.CharField(choices=(('Male' , 'Male'), ('Female', 'Female')), max_length=55, null=True)
    mobile_no = models.BigIntegerField(null=True)
    date_of_birth = models.DateField(null=True)
    pan_number = models.CharField(max_length=10, null=True)
    aadhaar_number = models.BigIntegerField(null=True)
    permanent_address = models.TextField(null=True)
    current_address = models.TextField(null=True)
    marital_status = models.CharField(choices=(('Single', 'Single'), ('Married', 'Married')), max_length=55, null=True)
    passport_no = models.CharField(max_length=9, null=True)
    father_name = models.CharField(max_length=255, null=True)
    mother_name = models.CharField(max_length=255, null=True)
    nationality = models.CharField(max_length=50, null=True)
    emergency_contact_no = models.BigIntegerField(null=True)
    blood_group = models.CharField(max_length=3, null=True)
    profile_photo = models.ImageField(upload_to='userprofile', null=True, default='default_profile_pic.png')
    is_requested = models.BooleanField(default=False) 
    is_completed_additional_details = models.BooleanField(default=False)  # this will become True if mandatory fields are filled by employee after verification by HR
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username
    
class UserBankDetail(models.Model):
    emp_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_bank_details')
    bank_name = models.CharField(max_length=255, null=True)
    branch_name = models.CharField(max_length=100, null=True)
    account_type = models.CharField(choices=(('Current', 'Current'), ('Saving', 'Saving')), max_length=25, null=True)
    ifsc_code = models.CharField(max_length=11, null=True)
    account_number = models.BigIntegerField(null=True)
    is_completed_bank_details = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.emp_user.username
    
class UserDocument(models.Model):
    emp_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_docs")
    doc_name = models.CharField(max_length=200, default='document')
    doc_file = models.FileField(upload_to='userdocs')
    is_completed_docs = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username + ' ' + self.doc_name
    
class DocumentRemark(models.Model):
    emp_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_docs_remark')
    remark = models.TextField()
    is_full_filled = models.BooleanField(default=False) # if there is any issue in uploaded docs by user HR will add remark to replace those docs & this field will True docs are ok 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username+ ' ' + self.remark
    
class UserEducationDetails(models.Model):
    emp_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_academics')
    ssc_board_name = models.CharField(max_length=255, null=True)
    ssc_school_name = models.CharField(max_length=255, null=True)
    ssc_percentage = models.IntegerField(default=0, null=True)
    ssc_passing_yr = models.IntegerField(default=0,null=True)
    hsc_board_name = models.CharField(max_length=255, null=True)
    hsc_school_name = models.CharField(max_length=255, null=True)
    hsc_percentage = models.IntegerField(default=0,null=True)
    hsc_passing_yr = models.IntegerField(default=0,null=True)
    hsc_stream = models.CharField(choices=(('Science', 'Science'), ('Arts', 'Arts'), ('Commerce', 'Commerce')), max_length=55, null=True)
    diploma_university = models.CharField(max_length=255, null=True)
    diploma_college = models.CharField(max_length=255, null=True)
    diploma_branch = models.CharField(max_length=100, null=True)
    diploma_admission_yr = models.IntegerField(default=0,null=True)
    diploma_passout_yr = models.IntegerField(default=0,null=True)
    diploma_percentage = models.IntegerField(default=0,null=True)
    graduation_university = models.CharField(max_length=255, null=True)
    graduation_college = models.CharField(max_length=255, null=True)
    graduation_branch = models.CharField(max_length=100, null=True)
    graduation_admission_yr = models.IntegerField(default=0,null=True)
    graduation_passout_yr = models.IntegerField(default=0,null=True)
    graduation_percentage = models.IntegerField(default=0,null=True)
    pg_university = models.CharField(max_length=255, null=True)
    pg_college = models.CharField(max_length=255, null=True)
    pg_branch = models.CharField(max_length=100,null=True)
    pg_admission_yr = models.IntegerField(default=0,null=True)
    pg_passout_yr = models.IntegerField(default=0,null=True)
    pg_percentage = models.IntegerField(default=0,null=True)
    is_completed_academics = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.first_name+ ' ' + self.emp_user.last_name +' '+ self.emp_user.username

class Teams(models.Model):
    team_name = models.CharField(max_length= 100)
    employees = models.ManyToManyField(User)
    leader_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_leader_name')
    is_completed_teams = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.team_name
    
class EmployeePermissions(models.Model):
    emp_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_permissions_user')
    can_approve_attendance = models.BooleanField(default=False)
    can_approve_leaves = models.BooleanField(default=False)
    can_manage_employee = models.BooleanField(default=False)
    can_manage_teams = models.BooleanField(default=False)
    can_manage_holiday = models.BooleanField(default=False)
    can_manage_salary = models.BooleanField(default=False)
    can_verify_emp_details = models.BooleanField(default=False)
    can_manage_shifts = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # for senior hr all permissions
    # for tl can approve attendance permission
    # for junior hr can manage teams, can manage holiday, can verify emp details.
    
    def is_team_leader (request):
        team_leader_permissions = EmployeePermissions.objects.get(emp_user = request.user)
        teams = Teams.objects.filter(leader_name_id = request.user.id)
        
        if team_leader_permissions is None:
            return False
        
        elif team_leader_permissions.can_approve_attendance == True and teams.count()>0:
            return teams
        
        else:
            return False
        
    def is_senior_hr (request):
        hr_permissions = EmployeePermissions.objects.get(emp_user = request.user)
        is_hr = UserBasicDetails.objects.filter(emp_user = request.user, department__department_name__icontains = 'Human')
        
        if hr_permissions is None:
            return False
        
        elif hr_permissions.can_approve_attendance == True and hr_permissions.can_approve_leaves == True and hr_permissions.can_manage_employee == True and hr_permissions.can_manage_teams == True and hr_permissions.can_manage_holiday == True and hr_permissions.can_manage_salary == True and hr_permissions.can_manage_shifts == True and hr_permissions.can_verify_emp_details == True and is_hr.count()>0 :
            return True

        else:
            return False
        
    def is_junior_hr (request):
        hr_permissions = EmployeePermissions.objects.get(emp_user = request.user)
        is_hr = UserBasicDetails.objects.filter(emp_user = request.user, department__department_name__icontains = 'Human')
        
        if hr_permissions is None:
            return False
        
        if hr_permissions.can_approve_attendance == False and hr_permissions.can_approve_leaves == False and hr_permissions.can_manage_employee == False and hr_permissions.can_manage_teams == True and hr_permissions.can_manage_holiday == True and hr_permissions.can_manage_salary == False and hr_permissions.can_verify_emp_details == True and hr_permissions.can_manage_shifts == True and is_hr.count()>0:
            return True
        
        else:
            return False
    
    def __str__ (self):
        return self.emp_user.username
    
class Notification(models.Model):
    emp_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notifications')  
    title = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    notification_date = models.DateField(auto_now_add=True)
    notification_time = models.TimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username + ' ' + self.title
        
    
@receiver(post_save, sender=User)
def create_signal(sender, instance, created, **kwargs):
    if created:
        UserBasicDetails.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def create_signal(sender, instance, created, **kwargs):
    if created:
        UserAdditionalDetail.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def create_signal(sender, instance, created, **kwargs):
    if created:
        UserBankDetail.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def create_signal(sender, instance, created, **kwargs):
    if created:
        UserEducationDetails.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def create_signal(sender, instance, created, **kwargs):
    if created:
        EmployeePermissions.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def create_organisation_detail_signal(sender, instance, created, **kwargs):
    if created:
        PreviousOrganisationDetail.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def create_organisation_detail_signal(sender, instance, created, **kwargs):
    if created:
        PreviousOrganisationDetail.objects.create(emp_user=instance).save()


        



