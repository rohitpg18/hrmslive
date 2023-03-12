from account.account_views.dependencies.basic_functions import *
from account.resources import *
from account.resources import *
from django.contrib import messages
from tablib import Dataset
from django.contrib.auth.hashers import make_password



def Upload(request):    
    if request.method == "POST":
        user_resouce = UserResouce()
        user_basic_resouce = UserBasicDetailsResouce()
        designation_resouce = DesignationResouce()
        department_resouce = DepartmentResouce()
        user_shift_resource = UserShiftDetailsResouce()
        dataset = Dataset()

        detail = request.FILES['myfile']
    

        imported_data = dataset.load(detail.read(), format='xlsx')


        for data in imported_data:
            
            username = data[0]         

            if User.objects.filter(username=username).exists():
                messages.warning(request, f"User {username} already exists")

            else:               
                user = User()
                user.username = data[0]
                user.password = make_password(data[9])
                user.first_name = data[1]
                user.last_name = data[2]
                user.save()

                username = data[0]
                password = data[9]
                designation = data[4]
                salary = data[8]
                department = data[3]
                experience = data[5]
                joining = data[7]
                shift_details = data[6]
                
                other_detail = UserBasicDetails.objects.get(emp_user__username= username)
                other_detail.designation_id    = designation
                other_detail.department_id     = department
                other_detail.experience_status = experience
                other_detail.date_of_joining   = joining
                other_detail.shift_details_id  = shift_details
                other_detail.salary            = salary
                other_detail.save()
            
                messages.success(request, f"Account Created sucessfully.\n Your Username is {username} and Password is {password}")
                      
    return render(request, "payroll/emp_management/upload.html")

class UserSignUp(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        
        user_id = request.user.id
        
        permission = EmployeePermissions.objects.get(emp_user_id=user_id)
        
        if permission is not None and permission.can_manage_employee:
            
        
            data={
                "designations": Designation.objects.all(),
                "departments" : Department.objects.all(),
                "shifts"      : UserShiftDetails.objects.all(),
                "emp_no"      : User.objects.all().count()
            }
                
        
            return render(request, "payroll/emp_management/create_account.html",data)
        
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

