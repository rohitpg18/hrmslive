from account.account_views.dependencies.basic_functions import *


class Shift(View):
    def get(self, request):
        Shift = UserShiftDetails.objects.all()
        return render(request,'payroll/emp_management/shift.html',{'Shift':Shift})


    def post(self, request):
        data = request.POST
        
        if data['type'] == 'create' :
            if UserShiftDetails.objects.filter(shift_name = data['sh_name']).exists():
                messages.warning(request, 'shift already exists')
                return redirect('shift')
            else:
                UserShiftDetails.objects.create(
                    shift_name = data['sh_name'],
                    in_time =data['in_time'],
                    out_time =data['out_time'],
                    )
                messages.success(request, 'shift added successfully')
                return redirect('shift')


        if data['type'] == 'update':
            if UserShiftDetails.objects.filter(shift_name = data['sh_name']).exists():
                messages.warning(request, 'shift already exists')
                return redirect('shift')
            else:
                shifts = UserShiftDetails.objects.filter(id=data['des_id'])
                if shifts.exists():
                    shifts = UserShiftDetails.objects.get(id=data['des_id'])
                    shifts.shift_name = data['sh_name']
                    shifts.save()
                    messages.success(request, 'shift added successfully')
                    return redirect('shift')
                
        if data['type'] == 'delete':
            shifts = UserShiftDetails.objects.filter(id=data['des_id'])
            if shifts is not None:
                shifts.delete()
                messages.success(request,'shift is deleted')
                return redirect('shift')
            else:
                messages.warning(request,'shift not found')
                return redirect('shift')









