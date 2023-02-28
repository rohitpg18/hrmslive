from account.account_views.dependencies.basic_functions import *



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
                
                if user_document.exists():
                    user_document[0].doc_file= ssc_doc_file
                    user_document[0].save()
                    
                else:
                    user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "SSC Marksheet", doc_file = ssc_doc_file)
            
            
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
                
                    if user_document.exists():
                        user_document[0].doc_file= hsc_doc_file
                        user_document[0].save()
                    else:
                        user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "HSC Marksheet", doc_file = hsc_doc_file)
                        

            
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
                
                    if user_document.exists():
                        user_document[0].doc_file= diploma_doc_file
                        user_document[0].save()
                    else:
                        user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Diploma Marksheet", doc_file = diploma_doc_file)
                        
                        
            
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
                
                    if user_document.exists():
                        user_document[0].doc_file= graduation_doc_file
                        user_document[0].save()     
                    else:
                        user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Graduation Marksheet", doc_file = graduation_doc_file)
                        
                
            
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
                
                    if user_document.exists():
                        user_document[0].doc_file= pg_doc_file
                        user_document[0].save()
                    else:
                        user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Post Graduation Marksheet", doc_file = pg_doc_file)
                
            education_detail.is_completed_academics= True
            education_detail.save()  
            messages.success(request,"data added successfully")
                        
            return redirect('self_details')
        
        
        return render (request, self.template_name)
    

