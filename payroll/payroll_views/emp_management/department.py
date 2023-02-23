from account.account_views.dependencies.basic_functions import *



class DepartmentDetails(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
    
        departments= Department.objects.all()
        return render(request,'payroll/emp_management/department.html',{'departments': departments})

    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        
        data=request.POST
        
        if data['type'] == "create":
            if Department.objects.filter(department_name=data['dept_name']).exists():
                messages.warning(request, 'department all ready exists')
                return redirect('department')
            else:
            
                Department.objects.create(department_name= data['dept_name'])
                messages.success(request, 'department added successfully')
                return redirect('department')
            
        elif data['type'] == "update":
            
            if Department.objects.filter(department_name=data['dept_name']).exists():
                messages.warning(request, 'department all ready exists')
                return redirect('department')
            else:
            
                dept =Department.objects.filter(id=data['dept_id'])
            
                if dept.exists():
                    
                   
                    dept = Department.objects.get(id=data['dept_id'])
                    dept.department_name= data['dept_name']
                    dept.save()
                    
                    messages.success(request, 'department updated successfully')
                    return redirect('department')
                
                else:
                    messages.error(request, 'department not found')
                    return redirect('department')
            
        elif data['type'] == 'delete':
            
            dept =Department.objects.get(id=data['dept_id'])
            
            if dept is not None:
                dept.delete()
                
                messages.success(request, 'department deleted successfully')
                return redirect('department')
            
            else:
                messages.error(request, 'department not found')
                return redirect('department')
        else:
            messages.error(request, 'department not found')
            return redirect('department')
        
        return redirect('department')