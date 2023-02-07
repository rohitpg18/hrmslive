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
    salary = models.DecimalField(max_digits=7, decimal_places=2, null=True)
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
    experience_in_years = models.IntegerField()
    previous_organisation = models.CharField(max_length=255)
    previous_organisation_designation = models.CharField(max_length=100)
    is_completed_previous_organisation_details = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username +' '+ self.previous_organisation
    
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
    profile_photo = models.FileField(upload_to='userprofile', null=True, default='default_profile_pic.png')
    is_requested = models.BooleanField(default=False) 
    is_completed_additional_details = models.BooleanField(default=False)  # this will become True if mandatory fields are filled by employee after verification by HR
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return self.emp_user.username
    
class UserBankDetail(models.Model):
    emp_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_bank_details')
    bank_name = models.CharField(max_length=255, null=True)
    branch_name = models.CharField(max_length=100)
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
    doc_file = models.FileField(upload_to='media/userdocs')
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
    
    
    def __str__ (self):
        return self.emp_user.username   
    

@receiver(post_save, sender=User)
def update_sal_signal(sender, instance, created, **kwargs):
    if created:
        UserBasicDetails.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def update_sal_signal(sender, instance, created, **kwargs):
    if created:
        UserAdditionalDetail.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def update_sal_signal(sender, instance, created, **kwargs):
    if created:
        UserBankDetail.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def update_sal_signal(sender, instance, created, **kwargs):
    if created:
        UserEducationDetails.objects.create(emp_user=instance).save()
        
@receiver(post_save, sender=User)
def update_sal_signal(sender, instance, created, **kwargs):
    if created:
        EmployeePermissions.objects.create(emp_user=instance).save()


