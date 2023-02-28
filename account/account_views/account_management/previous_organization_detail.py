from account.account_views.dependencies.basic_functions import *

    
class PreviousOrganizationDetail(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        user_id = request.user.id
        
        redirect_url = is_profile_complete(user_id)
        
        if  redirect_url == "previous_organization_details":
            
            organisation_details = PreviousOrganisationDetail.objects.filter(emp_user_id=user_id)
            
            context = {
        
            'organisation_details1' : PreviousOrganisationDetail.objects.get(emp_user_id=user_id, id = organisation_details[0].id )
            
            }
                
            return render(request, "account/profile_complete/previous_organization_detail.html", context)
        else:
            return redirect(redirect_url)
        
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        user_id = request.user.id
        
        if_second_company_check = request.POST.get('if_second_company_check')
        if_third_company_check = request.POST.get('if_third_company_check')
        
        requests = request.POST
    
        organisation_details = PreviousOrganisationDetail.objects.filter(emp_user_id=user_id)
        
        organisation_details1 = PreviousOrganisationDetail.objects.get(emp_user_id=user_id, id = organisation_details[0].id )
        
        
        organisation_details1.experience_in_years = requests["experience_in_years"]
        organisation_details1.previous_organisation = requests["previous_organisation"]
        organisation_details1.previous_organisation_designation = requests["previous_organisation_designation"]
        organisation_details1.is_completed_previous_organisation_details = True
        organisation_details1.save()
        
        # Upload Docs - Experience Letter, Relieving Letter, Offer Letter and Payslips
        
        # Experience Letter
        experience_letter_first = request.FILES.get('experience_letter_first', None)
        experience_letter_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="First Experience Letter")
        if experience_letter_doc.count() != 0:
            experience_letter_doc[0].doc_file = experience_letter_first
            experience_letter_doc[0].save()
        else:
            UserDocument.objects.create(emp_user_id=user_id, doc_name="First Experience Letter", doc_file=experience_letter_first)
            
        # Relieving Letter
        relieving_letter_first = request.FILES.get('relieving_letter_first', None)
        relieving_letter_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="First Relieving Letter")
        if relieving_letter_doc.count() != 0:
            relieving_letter_doc[0].doc_file = relieving_letter_first
            relieving_letter_doc[0].save()
        else:
            UserDocument.objects.create(emp_user_id=user_id, doc_name="First Relieving Letter", doc_file=relieving_letter_first)
            
        # Offer Letter
        offer_letter_first = request.FILES.get('offer_letter_first', None)
        offer_letter_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="First Offer Letter")
        if offer_letter_doc.count() != 0:
            offer_letter_doc[0].doc_file = offer_letter_first
            offer_letter_doc[0].save()
        else:
            UserDocument.objects.create(emp_user_id=user_id, doc_name="First Offer Letter", doc_file=offer_letter_first)
            
        # Payment Slip - 1
        salary_slip_first_one = request.FILES.get('salary_slip_first_one', None)
        salary_slip_one_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Salary Slip First One")
        if salary_slip_one_doc.count() != 0:
            salary_slip_one_doc[0].doc_file = salary_slip_first_one
            salary_slip_one_doc[0].save()
        else:
            UserDocument.objects.create(emp_user_id=user_id, doc_name="Salary Slip First One", doc_file=salary_slip_first_one)
        
        # Payment Slip - 2
        salary_slip_first_two = request.FILES.get('salary_slip_first_two', None)
        salary_slip_two_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Salary Slip First Two")
        if salary_slip_two_doc.count() != 0:
            salary_slip_two_doc[0].doc_file = salary_slip_first_two
            salary_slip_two_doc[0].save()
        else:
            UserDocument.objects.create(emp_user_id=user_id, doc_name="Salary Slip First Two", doc_file=salary_slip_first_two)
            
        # Payment Slip - 3
        salary_slip_first_three = request.FILES.get('salary_slip_first_three', None)
        salary_slip_three_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Salary Slip First Three")
        if salary_slip_three_doc.count() != 0:
            salary_slip_three_doc[0].doc_file = salary_slip_first_three
            salary_slip_three_doc[0].save()
        else:
            UserDocument.objects.create(emp_user_id=user_id, doc_name="Salary Slip First Three", doc_file=salary_slip_first_three)
             
        
        
            
        if if_second_company_check == 'True':
        
            
            if organisation_details.count() == 1:
               organisation_details2 = PreviousOrganisationDetail.objects.create(emp_user_id = user_id, experience_in_years= requests['experience_in_years2'], previous_organisation = requests['previous_organisation2'], previous_organisation_designation = requests['previous_organisation_designation2'], is_completed_previous_organisation_details = True)
            
            elif organisation_details.count()>1:
                organisation_details2 = PreviousOrganisationDetail.objects.get(emp_user_id=user_id, id = organisation_details[1].id )
                organisation_details2.experience_in_years = requests['experience_in_years2']
                organisation_details2.previous_organisation = requests['previous_organisation2']
                organisation_details2.previous_organisation_designation = requests['previous_organisation_designation2']
                organisation_details2.is_completed_previous_organisation_details = True
                organisation_details2.save()
                
            # Upload Docs - Experience Letter, Relieving Letter, Offer Letter and Payslips
        
            # Experience Letter
            experience_letter_second = request.FILES.get('experience_letter_second', None)
            experience_letter_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Second Experience Letter")
            if experience_letter_doc.count() != 0:
                experience_letter_doc[0].doc_file = experience_letter_second
                experience_letter_doc[0].save()
            else:
                UserDocument.objects.create(emp_user_id=user_id, doc_name="Second Experience Letter", doc_file=experience_letter_second)

            # Relieving Letter
            relieving_letter_second = request.FILES.get('relieving_letter_second', None)
            relieving_letter_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Second Relieving Letter")
            if relieving_letter_doc.count() != 0:
                relieving_letter_doc[0].doc_file = relieving_letter_second
                relieving_letter_doc[0].save()
            else:
                UserDocument.objects.create(emp_user_id=user_id, doc_name="Second Relieving Letter", doc_file=relieving_letter_second)

            # Offer Letter
            offer_letter_second = request.FILES.get('offer_letter_second', None)
            offer_letter_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Second Offer Letter")
            if offer_letter_doc.count() != 0:
                offer_letter_doc[0].doc_file = offer_letter_second
                offer_letter_doc[0].save()
            else:
                UserDocument.objects.create(emp_user_id=user_id, doc_name="Second Offer Letter", doc_file=offer_letter_second)

            # Payment Slip - 1
            salary_slip_second_one = request.FILES.get('salary_slip_second_one', None)
            salary_slip_one_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Salary Slip Second One")
            if salary_slip_one_doc.count() != 0:
                salary_slip_one_doc[0].doc_file = salary_slip_second_one
                salary_slip_one_doc[0].save()
            else:
                UserDocument.objects.create(emp_user_id=user_id, doc_name="Salary Slip Second One", doc_file=salary_slip_second_one)

            # Payment Slip - 2
            salary_slip_second_two = request.FILES.get('salary_slip_second_two', None)
            salary_slip_two_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Salary Slip Second Two")
            if salary_slip_two_doc.count() != 0:
                salary_slip_two_doc[0].doc_file = salary_slip_second_two
                salary_slip_two_doc[0].save()
            else:
                UserDocument.objects.create(emp_user_id=user_id, doc_name="Salary Slip Second Two", doc_file=salary_slip_second_two)

            # Payment Slip - 3
            salary_slip_second_three = request.FILES.get('salary_slip_second_three', None)
            salary_slip_three_doc = UserDocument.objects.filter(emp_user_id=user_id, doc_name="Salary Slip Second Three")
            if salary_slip_three_doc.count() != 0:
                salary_slip_three_doc[0].doc_file = salary_slip_second_three
                salary_slip_three_doc[0].save()
            else:
                UserDocument.objects.create(emp_user_id=user_id, doc_name="Salary Slip Second Three", doc_file=salary_slip_second_three)
                
        if if_third_company_check == "True":

            if organisation_details.count() == 2:
               organisation_details3 = PreviousOrganisationDetail.objects.create(emp_user_id = user_id, experience_in_years= requests['experience_in_years3'], previous_organisation = requests['previous_organisation3'], previous_organisation_designation = requests['previous_organisation_designation3'], is_completed_previous_organisation_details = True)
            
            elif organisation_details.count()>2:
                organisation_details3 = PreviousOrganisationDetail.objects.get(emp_user_id=user_id, id = organisation_details[2].id )
                organisation_details3.experience_in_years = requests['experience_in_years3']
                organisation_details3.previous_organisation = requests['previous_organisation3']
                organisation_details3.previous_organisation_designation = requests['previous_organisation_designation3']
                organisation_details3.is_completed_previous_organisation_details = True
                organisation_details3.save()
            
            
            

            
        messages.success(request,"Organisation Details added successfully")

        return redirect(is_profile_complete(user_id))
        
        
        