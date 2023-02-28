from account.account_views.dependencies.basic_functions import *



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

        
        profile_pic= request.FILES.get('img', None)
        

        additional_details= request.POST
        

        if profile_pic is not None and profile_pic != '':
            user_additional_detail.profile_photo= profile_pic

        user_additional_detail.gender=additional_details["gender"]

        user_additional_detail.mobile_no=additional_details["mobile_no"]

        user_additional_detail.date_of_birth=additional_details["date_of_birth"]

        user_additional_detail.pan_number=additional_details["pan_number"]
        
        pan_file = request.FILES.get('pan_file')
            
        if pan_file is not None:
                
            user_document= UserDocument.objects.filter(emp_user_id=user_id,doc_name = "Pan Card")
        
            if user_document.exists():
                user_document[0].doc_file= pan_file
                user_document[0].save()
                
            else:
                user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Pan Card", doc_file = pan_file)

        user_additional_detail.aadhaar_number=additional_details["aadhaar_number"]
        
        aadhar_file = request.FILES.get('aadhar_file')
            
        if aadhar_file is not None:
                
            user_document= UserDocument.objects.filter(emp_user_id=user_id,doc_name = "Aadhar Card")
        
            if user_document.exists():
                user_document[0].doc_file= aadhar_file
                user_document[0].save()
                
            else:
                user_document=UserDocument.objects.create(emp_user_id = user_id, doc_name = "Aadhar Card", doc_file = aadhar_file)
                
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
        
