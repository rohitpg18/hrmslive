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

                    day= DailyAttendance.objects.filter(emp_user_id= user_id,date=date)
                    month = get_month_year()

                    if not day.exists():
                        DailyAttendance.objects.create(emp_user_id=user_id,month=month,login_time=date.time(),is_present=True)

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
        month = get_month_year
        if day.exists():
            DailyAttendance.objects.filter(emp_user_id= user_id,date=date).update(logout_time=date.time())
        


        auth.logout(request)
        messages.success(request, "Successfully logged out")
        return redirect("login")