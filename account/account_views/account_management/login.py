from account.account_views.dependencies.basic_functions import *


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


                    date = datetime.today()
                    
                    month = get_month_year()

                    day= DailyAttendance.objects.get_or_create(emp_user_id= user_id,date=date, month=month)
                    
                    day[0].is_present = True
                    day[0].save()
                        
                    user_location = UserLocationDetails.objects.get_or_create(emp_user_id=user_id, attendance=day[0])
                    
                    user_location[0].country=get_location()['country']
                    user_location[0].state=get_location()['regionName']
                    user_location[0].city=get_location()['city']
                    user_location[0].latitude=get_location()['lat']
                    user_location[0].longitude=get_location()['lon']
                    user_location[0].service_provider=get_location()['org']
                    user_location[0].save()

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
        
        
        
        
class UserLogOut(View):
    @method_decorator(login_required(login_url='login'))
    def get(self, request):
        
        user_id = request.user.id


        date = datetime.today()
        day= DailyAttendance.objects.filter(emp_user_id= user_id,date=date)
        
        if day.exists():
            DailyAttendance.objects.filter(emp_user_id= user_id,date=date).update(logout_time=date.time())
        


        auth.logout(request)
        messages.success(request, "Successfully logged out")
        return redirect("login")