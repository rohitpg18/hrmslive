from account.account_views.dependencies.basic_functions import *



class DesignationDetails(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        designation= Designation.objects.all()
        return render(request,'payroll/emp_management/designation.html',{'designations': designation})
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        
        data=request.POST
        
        if data['type'] == "create":
            if Designation.objects.filter(designation_name=data['des_name']).exists():
                messages.warning(request, 'designation all ready exists')
                return redirect('designation')
            else:
            
                Designation.objects.create(designation_name= data['des_name'])
                messages.success(request, 'designation added successfully')
                return redirect('designation')
            
        elif data['type'] == "update":
            
            if Designation.objects.filter(designation_name=data['des_name']).exists():
                messages.warning(request, 'designation all ready exists')
                return redirect('designation')
            else:
            
                des =Designation.objects.filter(id=data['des_id'])
            
                if des.exists():
                    
                    des = Designation.objects.get(id=data['des_id'])
                    des.designation_name= data['des_name']
                    des.save()
                    
                    messages.success(request, 'designation updated successfully')
                    return redirect('designation')
                
                else:
                    messages.error(request, 'designation not found')
                    return redirect('designation')
            
        elif data['type'] == 'delete':
            
            des =Designation.objects.get(id=data['des_id'])
            
            if des is not None:
                des.delete()
                
                messages.success(request, 'designation deleted successfully')
                return redirect('designation')
            
            else:
                messages.error(request, 'designation not found')
                return redirect('designation')
        else:
            messages.error(request, 'designation not found')
            return redirect('designation')
        
        return redirect('designation')