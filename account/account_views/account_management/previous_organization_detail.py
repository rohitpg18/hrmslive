from account.account_views.dependencies.basic_functions import *

    
class PreviousOrganizationDetail(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        user_id = request.user.id
        
        redirect_url = is_profile_complete(user_id)
        
        if  redirect_url == "previous_organization_details":
                
            return render(request, "account/profile_complete/previous_organization_detail.html")
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
        
        previous_organization_docs1 = request.FILES.get('previous_organization_docs', None)
        
        previous_organization_doc = UserDocument.objects.filter(emp_user_id = user_id, doc_name = "Previous Organisation Docs")
        
        
        if previous_organization_doc.count() != 0:
            
            previous_organization_doc[0].doc_file = previous_organization_docs1
            
            previous_organization_doc[0].save()
            
        else:
            
            UserDocument.objects.create(emp_user_id = user_id, doc_name = "Previous Organisation Docs", doc_file = previous_organization_docs1 )
            
        if if_second_company_check == 'True':
            
            organisation_details2 = PreviousOrganisationDetail.objects.get(emp_user_id=user_id, id = organisation_details[1].id )
            
            organisation_details2.experience_in_years = requests['experience_in_years2']
            organisation_details2.previous_organisation = requests['previous_organisation2']
            organisation_details2.previous_organisation_designation = requests['previous_organisation_designation2']
            organisation_details2.is_completed_previous_organisation_details = True
            organisation_details2.save()
            
            previous_organization_docs2 = request.FILES.get('previous_organization_docs', None)
            
            previous_organization_doc2 = UserDocument.objects.filter(emp_user_id = user_id, doc_name = "Previous Organisation Docs 2")
        
        if previous_organization_doc2.count() != 0:
            
            previous_organization_doc2[0].doc_file = previous_organization_docs2
            
            previous_organization_doc2[0].save() 
            
        else:
            
            UserDocument.objects.create(emp_user_id = user_id, doc_name = "Previous Organisation Docs 2", doc_file = previous_organization_docs2 )
            
        messages.success(request,"Organisation Details added successfully")

        return redirect(is_profile_complete(user_id))
        
        
        