from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from account.models import *
from django.contrib.auth import authenticate,logout
from django.contrib import auth
from django.contrib import messages


def user_details(user_id,is_detail_required = False,detail=0,**kwargs):
    
    
    if User.objects.filter(id=user_id).exists() == False:
        return None
        

    if is_detail_required:
        if detail == 0:
            
            basic_detail= UserBasicDetails.objects.get(emp_user_id= user_id)
            additional_detail= UserAdditionalDetail.objects.get(emp_user_id= user_id)
            bank_detail= UserBankDetail.objects.get(emp_user_id= user_id)
            education_detail= UserEducationDetails.objects.get(emp_user_id= user_id)
            
            if basic_detail is None:
                basic_detail= UserBasicDetails.objects.create(emp_user_id= user_id)
        
            if additional_detail is None:
                additional_detail= UserAdditionalDetail.objects.create(emp_user_id= user_id)

            if bank_detail is None:
                bank_detail = UserBankDetail.objects.create(emp_user_id= user_id)

            if education_detail is None:
                education_detail= UserEducationDetails.objects.filter(emp_user_id= user_id)
            
            return {"basic_detail":basic_detail,"additional_detail":additional_detail,"bank_detail":bank_detail,"education_detail":education_detail}
            
        elif detail == 1:
            basic_detail= UserBasicDetails.objects.get(emp_user_id= user_id)
            if basic_detail is None:
                basic_detail= UserBasicDetails.objects.create(emp_user_id= user_id)
                
            return basic_detail
        
        
        elif detail == 2:
            additional_detail= UserAdditionalDetail.objects.get(emp_user_id= user_id)
            
            if additional_detail is None:
                additional_detail= UserAdditionalDetail.objects.create(emp_user_id= user_id)

            return additional_detail
        
        
        elif detail == 3:
            bank_detail= UserBankDetail.objects.get(emp_user_id= user_id)
            
            if bank_detail is None:
                bank_detail = UserBankDetail.objects.create(emp_user_id= user_id)

            
            return bank_detail
        
        
        elif detail == 4:
            education_detail= UserEducationDetails.objects.get(emp_user_id= user_id)
            
            if education_detail is None:
                education_detail= UserEducationDetails.objects.filter(emp_user_id= user_id)
            
            return education_detail
        
        else:
            return None
    
    
    

def is_profile_complete(user_id,**kwargs):
        
    
    user_detail= user_details(user_id,True,0)
    
    if user_detail is not None:
        
        if user_detail["basic_detail"].is_verify or user_detail["basic_detail"].is_requested:
            
            return 'self_details'

        
        else:
                    
            if user_detail["additional_detail"].is_completed_additional_details == False:
                
                return 'additional_details'

            
            elif user_detail["bank_detail"].is_completed_bank_details == False:
                
                return 'bank_details'
            
            elif user_detail["education_detail"].is_completed_academics == False:
                return 'educational_details'
            
            else:
                return 'self_details'
        
    return 'login'



class TryPage(View):
    
    # @method_decorator(login_required(login_url='login'))
    def get(self,request):
        
        # return render(request, "try_pages/user_form.html")
        return render(request, "try_pages/user_create_form.html")


class UserLogin(View):

    def get(self,request):
        return render(request,"account/auth/login.html")

    def post(self,request):
        
        username= request.POST['username']
        password= request.POST['password']

        if username and password is not None:
            emp_user = authenticate(username=username, password=password)
            
            if emp_user is not None:
                
                if emp_user.is_active:
                    auth.login(request,emp_user)

                    user_id = request.user.id

                    return redirect(is_profile_complete(user_id))
                    
                else:
                    messages.add_message(request, messages.INFO, 'Your account is not active.\n Please contact administrative')
                    return redirect('login')

            else:
                messages.add_message(request, messages.INFO, 'Invalid username or password',extra_tags='Login')
                return redirect('login')
            
        else:
            
            messages.add_message(request, messages.INFO, 'Invalid username or password',extra_tags='Login')
            return redirect('login')
        


class UserSignUp(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        
        user_id = request.user.id
        
        permission = EmployeePermissions.objects.get(emp_user_id=user_id)
        
        if permission is not None and permission.can_manage_employee:
            
        
            data={
                "designations":Designation.objects.all(),
                "departments":Department.objects.all(),
                "shifts":UserShiftDetails.objects.all(),
                "emp_no": User.objects.all().count()
            }
                
        
            return render(request, "account/profile_complete/basic_details.html",data)
        
        else:
            return HttpResponse("sorry you don't have permission")
        
        


    @method_decorator(login_required(login_url='login'))
    def post(self ,request):
        
        user_id = request.user.id
        
        permission = EmployeePermissions.objects.get(emp_user_id=user_id)
        
        if permission is not None and permission.can_manage_employee:
        
            
            emp_no= int(request.POST.get('emp_no'))+1
            username= "EP" + str(emp_no).zfill(5)
            password = request.POST['password']
            
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            
            designation= request.POST['designation']
            department= request.POST['department']
            shift_details= request.POST['shift_details']
            
            
            date_of_joining= request.POST['date_of_joining']
            salary= request.POST['salary']
            
            experience_status= request.POST['experience_status']
            is_salaried= request.POST['is_salaried']
            
            
            can_approve_attendance= request.POST.get('can_approve_attendance')
            can_approve_leaves= request.POST.get('can_approve_leaves')
            can_manage_employee= request.POST.get('can_manage_employee')
            can_manage_teams= request.POST.get('can_manage_teams')
            can_manage_holiday= request.POST.get('can_manage_holiday')
            can_manage_salary= request.POST.get('can_manage_salary')
            can_verify_emp_details= request.POST.get('can_verify_emp_details')
            can_manage_shifts= request.POST.get('can_manage_shifts')
            
            if User.objects.filter(username=username).exists():
                return redirect('signup')
        
            emp_user = User.objects.create_user(username=username, password=password)
            emp_user.first_name = first_name
            emp_user.last_name = last_name
            emp_user.save()
            

            user_basic_details= UserBasicDetails.objects.get(emp_user_id=emp_user.id)
    
            
            user_basic_details.designation = Designation.objects.get(id=designation)
            user_basic_details.department = Department.objects.get(id=department)
            
            user_basic_details.shift_details = UserShiftDetails.objects.get(id=shift_details)
            
            
            user_basic_details.date_of_joining= date_of_joining
            user_basic_details.salary= salary
            user_basic_details.experience_status= experience_status
            
            if is_salaried == "True":
                user_basic_details.is_salaried= True
            else:
                user_basic_details.is_salaried= False
                
            user_basic_details.created_by_id= user_id
            
            
            
            
            user_permissions= EmployeePermissions.objects.get(emp_user=emp_user.id)
            
            if user_permissions is None:
                user_permissions= EmployeePermissions.objects.create(emp_user=emp_user.id)
                
            
            if user_permissions is not None:
                
                print("yes it will run successfully")
            
                if can_approve_attendance == "True":
                    user_permissions.can_approve_attendance = True
                    user_permissions.save()
                    
                    
                if can_approve_leaves == "True":
                    
                    user_permissions.can_approve_leaves= True
                    user_permissions.save()
                    
                    
                if can_manage_employee == "True":
                    user_permissions.can_manage_employee= True
                    user_permissions.save()
                    
                    
                if can_manage_teams == "True":
                    user_permissions.can_manage_teams= True
                    user_permissions.save()
                    
                    
                if can_manage_holiday == "True":
                    user_permissions.can_manage_holiday= True
                    user_permissions.save()
                    
                if can_manage_salary == "True":
                    user_permissions.can_manage_salary= True
                    user_permissions.save()
                    
                    
                if can_verify_emp_details == "True":
                    user_permissions.can_verify_emp_details= True
                    user_permissions.save()
                    
                if can_manage_shifts == "True":
                    user_permissions.can_manage_shifts= True
                    user_permissions.save()
                    
            user_basic_details.is_completed_basic_details = True
            
            user_basic_details.save()
            
            

            messages.success(request, f"Account Created sucessfully.\n Your Username is {username} and Password is {password}")
            
            return redirect('signup')
            
        
        else:
            messages.warning(request, "Sorry, you don't have permission")
            return HttpResponse("Sorry, you don't have permission")




class AdditionalDetail(View):
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        
        user_id = request.user.id
        
        redirect_url = is_profile_complete(user_id)
        
        if  redirect_url == "additional_details":
                
            return render(request, "account/profile_complete/additional_details.html")
        else:
            return redirect(redirect_url)
    
    @method_decorator(login_required(login_url='login'))
    def post(self ,request):

        user_id= request.user.id

        user_additional_detail= UserAdditionalDetail.objects.get(emp_user_id=user_id)

        profile_pic= request.FILES.get('profile_photo')

        additional_details= request.POST

        if profile_pic is not None and profile_pic != '':
            user_additional_detail.profile_photo= profile_pic

        user_additional_detail.gender=additional_details["gender"]

        user_additional_detail.mobile_no=additional_details["mobile_no"]

        user_additional_detail.date_of_birth=additional_details["date_of_birth"]

        user_additional_detail.pan_number=additional_details["pan_number"]

        user_additional_detail.aadhaar_number=additional_details["aadhaar_number"]

        user_additional_detail.permanent_address=additional_details["permanent_address"]
        
        if additional_details["is_address_same"]== "True":
            user_additional_detail.current_address=additional_details["permanent_address"]
        else:
            if additional_details["current_address"] is not None and additional_details["current_address"]!='':
                user_additional_detail.current_address=additional_details["current_address"]
        
        user_additional_detail.marital_status=additional_details["marital_status"]

        if additional_details["passport_no"] is not None and additional_details["passport_no"]!='':
            user_additional_detail.passport_no=additional_details["passport_no"]

        user_additional_detail.father_name=additional_details["father_name"]
        user_additional_detail.mother_name=additional_details["mother_name"]
        user_additional_detail.nationality=additional_details["nationality"]

        if additional_details["emergency_contact_no"] is not None and additional_details["emergency_contact_no"]!='':
            user_additional_detail.emergency_contact_no=additional_details["emergency_contact_no"]

        
        user_additional_detail.blood_group=additional_details["blood_group"]
        
        user_additional_detail.is_completed_additional_details = True

        user_additional_detail.save()
        
        messages.add_message(request, messages.SUCCESS, 'additional details added successfully')
        
        return redirect(is_profile_complete(user_id))
        

    
class BankDetail(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        user_id = request.user.id
        
        redirect_url = is_profile_complete(user_id)
        
        if  redirect_url == "bank_details":
                
            return render(request, "account/profile_complete/bank_details.html")
        else:
            return redirect(redirect_url)
        
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        user_id = request.user.id
        
        bank_name = request.POST.get('bank_name')
        branch_name = request.POST.get('branch_name')
        account_type = request.POST.get('account_type')
        ifsc_code = request.POST.get('ifsc_code')
        account_number = request.POST.get('account_number')
        
        bank_details = UserBankDetail.objects.get(emp_user_id=user_id)
        
        if bank_details is None:
            bank_details = UserBankDetail.objects.create(emp_user_id=user_id)
        
        bank_details.bank_name = branch_name
        bank_details.branch_name = branch_name
        bank_details.account_type = account_type
        bank_details.ifsc_code = ifsc_code
        bank_details.account_number = account_number
        bank_details.is_completed_bank_details = True
        
        bank_details.save()
        
        return HttpResponse("Bank Details added successfully")
        


class EducationalDetail(View):
    
    @method_decorator(login_required(login_url='login'))
    def get (self, request):
        user_id = request.user.id
                
        redirect_url = is_profile_complete(user_id)
        
        if  redirect_url == "educational_details":
                
            return render (request, 'account/profile_complete/education_details.html')
        else:
            return redirect(redirect_url)
    
    
    @method_decorator(login_required(login_url='login'))
    def post (self, request, *args, **kwargs):
        user_id = request.user.id
        
        e_details= request.POST
        
        emp_ssc_check = request.POST.get('emp_ssc_check')
        emp_hsc_check = request.POST.get('emp_hsc_check')
        emp_diploma_check = request.POST.get('emp_diploma_check')
        emp_graduation_check = request.POST.get('emp_graduation_check')
        emp_pg_check = request.POST.get('emp_pg_check')

        education_detail = UserEducationDetails.objects.get(emp_user_id = user_id)
        
        if education_detail is None:
            education_detail = UserEducationDetails.objects.create(emp_user_id = user_id)
            
        if education_detail is not None:
            
            education_detail.ssc_board_name = e_details["ssc_board_name"]
            education_detail.ssc_school_name = e_details["ssc_school_name"]
            education_detail.ssc_percentage = e_details["ssc_percentage"]
            education_detail.ssc_passing_yr = e_details["ssc_passing_yr"]
            
            
            ssc_doc_file = request.FILES.get('ssc_doc_file')
            
            if ssc_doc_file is not None:
                
                user_document= UserDocument.objects.filter(emp_user_id=user_id,doc_name = "SSC Marksheet")
                
                if user_document is None:
                    user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "SSC Marksheet", doc_file = ssc_doc_file)
                else:
                    user_document.doc_file= ssc_doc_file
                    user_document.save()
            
            
            if emp_hsc_check == "True":
                
                education_detail.hsc_board_name = e_details["hsc_board_name"]
                education_detail.hsc_school_name =e_details["hsc_school_name"]
                education_detail.hsc_percentage = e_details["hsc_percentage"]
                education_detail.hsc_passing_yr = e_details["hsc_passing_yr"]
                education_detail.hsc_stream =     e_details["hsc_stream"]
                education_detail.save()
                
                hsc_doc_file = request.FILES.get('hsc_doc_file')
            
                if hsc_doc_file is not None:
                
                    user_document= UserDocument.objects.filter(emp_user_id=user_id,doc_name = "HSC Marksheet")
                
                    if user_document is None:
                        user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "HSC Marksheet", doc_file = hsc_doc_file)
                    else:
                        user_document.doc_file= hsc_doc_file
                        user_document.save()

            
            if emp_diploma_check == "True":
                
                education_detail.diploma_university =    e_details["diploma_university"]
                education_detail.diploma_college =       e_details["diploma_college"]
                education_detail.diploma_branch =        e_details["diploma_branch"]
                education_detail.diploma_admission_yr =  e_details["diploma_admission_yr"]
                education_detail.diploma_passout_yr =    e_details["diploma_passout_yr"]
                education_detail.diploma_percentage =    e_details["diploma_percentage"]
                education_detail.save()
                
                
                diploma_doc_file = request.FILES.get('diploma_doc_file')
            
                if diploma_doc_file is not None:
                
                    user_document= UserDocument.objects.filter(emp_user_id=user_id,doc_name = "Diploma Marksheet")
                
                    if user_document is None:
                        user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Diploma Marksheet", doc_file = diploma_doc_file)
                    else:
                        user_document.doc_file= diploma_doc_file
                        user_document.save()
                        
            
            if emp_graduation_check == "True":
                
                education_detail.graduation_university =     e_details["graduation_university"]
                education_detail.graduation_college =        e_details["graduation_college"]
                education_detail.graduation_branch =         e_details["graduation_branch"]
                education_detail.graduation_admission_yr =   e_details["graduation_admission_yr"]
                education_detail.graduation_passout_yr =     e_details["graduation_passout_yr"]
                education_detail.graduation_percentage =     e_details["graduation_percentage"]
                education_detail.save()
                
                
                graduation_doc_file = request.FILES.get('graduation_doc_file')
            
                if graduation_doc_file is not None:
                
                    user_document= UserDocument.objects.filter(emp_user_id=user_id,doc_name = "Graduation Marksheet")
                
                    if user_document is None:
                        user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Graduation Marksheet", doc_file = graduation_doc_file)
                    else:
                        user_document.doc_file= graduation_doc_file
                        user_document.save()
                
            
            if emp_pg_check == "True":
                
                education_detail.pg_university =     e_details["pg_university"]
                education_detail.pg_college =        e_details["pg_college"]
                education_detail.pg_branch =         e_details["pg_branch"]
                education_detail.pg_admission_yr =   e_details["pg_admission_yr"]
                education_detail.pg_passout_yr =     e_details["pg_passout_yr"]
                education_detail.pg_percentage =     e_details["pg_percentage"]
                education_detail.save()
                
                
                pg_doc_file = request.FILES.get('pg_doc_file')
            
                if pg_doc_file is not None:
                
                    user_document= UserDocument.objects.filter(emp_user_id=user_id,doc_name = "Post Graduation Marksheet")
                
                    if user_document is None:
                        user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Post Graduation Marksheet", doc_file = pg_doc_file)
                    else:
                        user_document.doc_file= pg_doc_file
                        user_document.save()
                
            education_detail.is_completed_academics= True
            education_detail.save()  
            messages.success(request,"data added successfully")
                        
            return redirect('self_details')
        
        
        return render (request, self.template_name)
    



























class SelfDetail(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        user_id = request.POST.get('user')
        is_profile_complete(user_id)
        
        
        user_id = request.user.id
        
        data= {
            "basic_detail": UserBasicDetails.objects.get(emp_user_id=user_id),
            "additional_detail":UserAdditionalDetail.objects.get(emp_user_id=user_id),
            "educational_details": UserEducationDetails.objects.get(emp_user_id=user_id),
            "bank_detail": UserBankDetail.objects.get(emp_user_id=user_id),
            
            
        }
        
        return render(request,'account/profile/self_details.html',data)
    

