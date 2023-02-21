from account.account_views.dependencies.basic_functions import *


class UpdateEmployee(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request, pk):

        user_id = request.user.id

        permission = EmployeePermissions.objects.get(emp_user_id=user_id)

        if permission is not None and permission.can_manage_employee:

            data = {
                "designations": Designation.objects.all(),
                "departments": Department.objects.all(),
                "shifts": UserShiftDetails.objects.all(),
                "emp_user": User.objects.get(id=pk),

            }

            return render(request, "payroll/emp_management/update_employee.html", data)

        else:
            return HttpResponse("sorry you don't have permission")

    @method_decorator(login_required(login_url='login'))
    def post(self, request, pk):

        user_id = request.user.id

        permission = EmployeePermissions.objects.get(emp_user_id=user_id)

        if permission is not None and permission.can_manage_employee:

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']

            designation = request.POST['designation']
            print(f"designation - {designation}")
            department = request.POST['department']
            print()
            shift_details = request.POST['shift_details']

            date_of_joining = request.POST['date_of_joining']
            salary = request.POST['salary']

            experience_status = request.POST['experience_status']
            is_salaried = request.POST['is_salaried']

            can_approve_attendance = request.POST.get('can_approve_attendance')
            can_approve_leaves = request.POST.get('can_approve_leaves')
            can_manage_employee = request.POST.get('can_manage_employee')
            can_manage_teams = request.POST.get('can_manage_teams')
            can_manage_holiday = request.POST.get('can_manage_holiday')
            can_manage_salary = request.POST.get('can_manage_salary')
            can_verify_emp_details = request.POST.get('can_verify_emp_details')
            can_manage_shifts = request.POST.get('can_manage_shifts')
            completed_bank_details = request.POST.get('is_completed_bank_details')
            is_active_employee = request.POST.get('is_active_employee')
            # completed_educational_details = request.POST.get('is_completed_academics')
            # completed_organisation_details = request.POST.get('is_completed_previous_organisation_details')
            # completed_additional_details = request.POST.get('is_completed_additional_details')
            

            emp_user = User.objects.get(id=pk)

            emp_user.first_name = first_name
            emp_user.last_name = last_name
            
            if is_active_employee == "True":
                emp_user.is_active = True
            else:
                emp_user.is_active = False
            emp_user.save()

            user_basic_details = UserBasicDetails.objects.get(emp_user_id=emp_user.id)

            user_basic_details.designation = Designation.objects.get(id=designation)
            user_basic_details.department = Department.objects.get(id=department)
            user_basic_details.shift_details = UserShiftDetails.objects.get(id=shift_details)

            user_basic_details.date_of_joining = date_of_joining
            user_basic_details.salary = salary
            user_basic_details.experience_status = experience_status

            if is_salaried == "True":
                user_basic_details.is_salaried = True
            else:
                user_basic_details.is_salaried = False

            user_basic_details.created_by_id = user_id

            user_permissions = EmployeePermissions.objects.get(emp_user=emp_user.id)

            if user_permissions is None:
                user_permissions = EmployeePermissions.objects.create(emp_user=emp_user.id)

            if user_permissions is not None:

                if can_approve_attendance == "True":
                    user_permissions.can_approve_attendance = True
                else:
                    user_permissions.can_approve_attendance = False
                user_permissions.save()

                if can_approve_leaves == "True":
                    user_permissions.can_approve_leaves = True
                else:
                    user_permissions.can_approve_leaves = False
                user_permissions.save()

                if can_manage_employee == "True":
                    user_permissions.can_manage_employee = True
                else:
                    user_permissions.can_manage_employee = False
                user_permissions.save()

                if can_manage_teams == "True":
                    user_permissions.can_manage_teams = True
                else:
                    user_permissions.can_manage_teams = False
                user_permissions.save()

                if can_manage_holiday == "True":
                    user_permissions.can_manage_holiday = True
                else:
                    user_permissions.can_manage_holiday = False
                user_permissions.save()

                if can_manage_salary == "True":
                    user_permissions.can_manage_salary = True
                else:
                    user_permissions.can_manage_salary = False
                user_permissions.save()

                if can_verify_emp_details == "True":
                    user_permissions.can_verify_emp_details = True
                else:
                    user_permissions.can_verify_emp_details = False
                user_permissions.save()

                if can_manage_shifts == "True":
                    user_permissions.can_manage_shifts = True
                else:
                    user_permissions.can_manage_shifts = False
                user_permissions.save()

            user_basic_details.is_completed_basic_details = True
            user_basic_details.save()

            user_bank_details = UserBankDetail.objects.get(emp_user_id=emp_user.id)

            if completed_bank_details == "True":
                user_bank_details.is_completed_bank_details = True
            else:
                user_bank_details.is_completed_bank_details = False
            user_bank_details.save()

            # user_additional_details = UserAdditionalDetail.objects.get(emp_user_id=emp_user.id)
            # user_educational_details = UserEducationDetails.objects.get(emp_user_id=emp_user.id)
            # user_organisation_details = PreviousOrganisationDetail.objects.filter(emp_user_id=emp_user.id)

            # if completed_additional_details == "True":
            #     user_additional_details.is_completed_additional_details = True

            # else:
            #     user_additional_details.is_completed_additional_details = False
            #     user_additional_details.save()

            # if completed_educational_details == "True":
            #     user_educational_details.is_completed_academics = True

            # else:
            #     user_educational_details.is_completed_academics = False
            #     user_educational_details.save()

            # if completed_organisation_details == "True":
            #     user_organisation_details[0].is_completed_previous_organisation_details = True

            # else:
            #     user_organisation_details[0].is_completed_previous_organisation_details = False
            #     user_organisation_details[0].save()

            messages.success(request, "Employee Updated Successfully")

            return redirect("all_users")

        else:
            messages.warning(request, "Sorry, you don't have permission")
            return HttpResponse("Sorry, you don't have permission")
