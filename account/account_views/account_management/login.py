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
        
        
        