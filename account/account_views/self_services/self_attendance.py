from account.account_views.dependencies.basic_functions import *


class ApplyAttendance(View):
    
    @method_decorator(login_required(login_url='login'))
    def get(self,request):
        user_id = request.user.id
        date = datetime.today().date()
        day_name = datetime.today().strftime("%A")
            
        daily_leave= DailyLeave.objects.filter(emp_user_id=user_id,date=date)
        holiday= Holiday.objects.filter(date=date).exists()
            
        can_mark_attendance=False
        is_requested= False
        
        
        daily_attendance = DailyAttendance.objects.filter(emp_user_id=user_id,date=date)

        if not daily_leave.exists():
            
            can_mark_attendance=True
        
        else:
            if daily_leave[0].date_is_half:
                
                in_time = request.user.user_basics.shift_details.in_time.strftime("%H:%M:%S")
                out_time = request.user.user_basics.shift_details.out_time.strftime("%H:%M:%S")
                current_time = datetime.now().time().strftime("%H:%M:%S")
                    
                in_time = datetime.strptime(in_time, "%H:%M:%S")
                out_time = datetime.strptime(out_time, "%H:%M:%S")
                current_time = datetime.strptime(current_time, "%H:%M:%S")
                    
                total_working_hours =(out_time-in_time)
                second_half_in_time_time = in_time + total_working_hours/2
                
                if daily_leave[0].date_is_first_half:
                    
                    
                    if current_time >= second_half_in_time_time and current_time<= out_time:
                        can_mark_attendance = True
                    else:
                        can_mark_attendance = False
                        
                else:
                    
                    if current_time >= in_time and  current_time <= second_half_in_time_time:
                        can_mark_attendance = True
                    else:
                        can_mark_attendance = False
            else:
                can_mark_attendance=False
        
        if day_name == 'Saturday' or day_name == 'Sunday':
            can_mark_attendance=False
        
        if holiday:
            can_mark_attendance = False
            
            
            
        if not daily_attendance.exists():
            
            can_mark_attendance= True
            is_requested= False

        else:
            
            if daily_attendance[0].logout_time is None:
                can_mark_attendance = True
                is_requested= True
                
            else:
                can_mark_attendance = False
                is_requested =False
       
            # calculates no of present days in current month
        month_full_day_present_count = DailyAttendance.objects.filter(emp_user_id = user_id, month = get_month_year(), is_present = True).count()
        month_half_day_present_count = DailyAttendance.objects.filter(emp_user_id = user_id, month = get_month_year(), is_present = True, is_half_day = True).count()
        if month_full_day_present_count == 0:
            month_presenty_count = Decimal(month_half_day_present_count*0.5)
        else:
            month_presenty_count = Decimal(month_full_day_present_count - (month_half_day_present_count*0.5))
            
        
            
        months = {month: index for index, month in enumerate(month_abbr) if month}
        month_index = int(months[str(get_month_year())[0:3]])
        year = int(str(get_month_year())[-4:])
        end_date = get_end_date_of_month(year, month_index)
        first_date = end_date.replace(day = 1)
        
        month_full_day_leaves = DailyLeave.objects.filter(emp_user_id = user_id, date__gte = first_date, date__lte = last_date).count()
        month_half_day_leaves = DailyLeave.objects.filter(emp_user_id = user_id, date__gte = first_date, date__lte = last_date, date_is_half = True).count()
        if month_full_day_leaves == 0:
            month_leaves_count = Decimal(month_half_day_leaves*0.5)
        else:
            month_leaves_count = Decimal(month_full_day_leaves - (month_half_day_leaves * 0.5))
        
        holiday_month_count = Decimal(Holiday.objects.filter(month = get_month_year()).count())
        
        
        month_days = Decimal(monthrange(year, month)[1])
        
        sundays = 0
        saturdays = 0
        for day in Calendar().itermonthdates(year, month_index):
            if day.weekday() == 6 and day.month == month_index:
                sundays += 1
        for day in Calendar().itermonthdates(year, month_index):
            if day.weekday() == 5 and day.month == month_index:
                saturdays += 1
        weekdays = Decimal(sundays + saturdays)
        

        today_date = datetime.today()
        

        # initializing dates ranges 
        test_date1, test_date2 = first_date, today_date

        # generating total days using busday_count()
        res = np.busday_count(test_date1.strftime('%Y-%m-%d'),
                              test_date2.strftime('%Y-%m-%d'))

        num_days = int((today_date - first_date).days)
        weekdays_ab = num_days - int(res)
        
        holiday_month_count_ab = Decimal(Holiday.objects.filter(date__gte = first_date, date__lte = today_date).count())
        
        month_full_day_leaves_ab = DailyLeave.objects.filter(emp_user_id = user_id, date__gte = first_date, date__lte = today_date).count()
        month_half_day_leaves_ab = DailyLeave.objects.filter(emp_user_id = user_id, date__gte = first_date, date__lte = today_date, date_is_half = True).count()
        if month_full_day_leaves_ab == 0:
            month_leaves_count_ab = Decimal(month_half_day_leaves_ab*0.5)
        else:
            month_leaves_count_ab = Decimal(month_full_day_leaves_ab - (month_half_day_leaves_ab * 0.5))
        
        month_full_day_present_count_ab = DailyAttendance.objects.filter(emp_user_id = user_id, date__gte = first_date, date__lte = last_date, is_present = True).count()
        month_half_day_present_count_ab = DailyAttendance.objects.filter(emp_user_id = user_id, date__gte = first_date, date__lte = last_date, is_present = True, is_half_day = True).count()
        if month_full_day_present_count_ab == 0:
            month_presenty_count_ab = Decimal(month_half_day_present_count_ab*0.5)
        else:
            month_presenty_count_ab = Decimal(month_full_day_present_count_ab - (month_half_day_present_count_ab*0.5))
        
        absent_days = Decimal(datetime.now().strftime('%d')) - holiday_month_count_ab - month_leaves_count_ab - month_presenty_count_ab - weekdays_ab
        
        working_days = month_days - holiday_month_count - weekdays
        
        
        
       
        
        context = {
            'can_mark_attendance':can_mark_attendance,
            'is_requested':is_requested,
            'present_days': month_presenty_count,   
            'leaves': month_leaves_count,
            'holidays': holiday_month_count,
            'working_days': working_days,
            'absent_days':absent_days
            }
            
        return render(request,"account/self_services/self_attendance.html", context)
    
    

    @method_decorator(login_required(login_url='login'))
    def post(self,request):
        user_id = request.user.id
        data = request.POST
        
        
        
        
        if user_id  == int(data['user_id']):
            
            date = datetime.today().date()
            day_name = datetime.today().strftime("%A")
            
            daily_leave= DailyLeave.objects.filter(emp_user_id=user_id,date=date)
            holiday= Holiday.objects.filter(date=date).exists()
            
            can_mark_attendance=False
            is_half_day=False
            is_first_half= False
            is_second_half = False
            
            if not daily_leave.exists():
                can_mark_attendance=True
                
            else:
                if daily_leave[0].date_is_half:
                    can_mark_attendance=True
                    is_half_day = True
                    is_first_half= daily_leave[0].date_is_first_half
                    is_second_half=daily_leave[0].date_is_second_half
                        
                else:
                    can_mark_attendance=False
                    
            if day_name == 'Saturday' or day_name == 'Sunday':
                can_mark_attendance=False
                
            if holiday:
                can_mark_attendance = False
                

            if can_mark_attendance:
                
                daily_attendance = DailyAttendance.objects.filter(emp_user_id=user_id,date=date)
                
                
                if not daily_attendance.exists():
                    

                    in_time = request.user.user_basics.shift_details.in_time.strftime("%H:%M:%S")
                    out_time = request.user.user_basics.shift_details.out_time.strftime("%H:%M:%S")
                    current_time = datetime.now().time().strftime("%H:%M:%S")
                    
                    
                    in_time = datetime.strptime(in_time, "%H:%M:%S")
                    out_time = datetime.strptime(out_time, "%H:%M:%S")
                    current_time = datetime.strptime(current_time, "%H:%M:%S")
                    
                    total_working_hours = out_time-in_time
                    
                    half_day = False
                    first_half= False
                    second_half= False
                    
                    if is_half_day:
                        
                        second_half_in_time_time = in_time + total_working_hours/2
                        
                        if is_first_half:
                            
                        
                            if current_time > second_half_in_time_time + timedelta(hours=2) :
                                messages.warning(request, 'your are too late can not mark todays attendance')
                                return redirect('self_attendance')
                            
                            else:
                                half_day = True
                                first_half = False
                                
                        if is_second_half:
                            
                            if current_time > in_time + timedelta(hours=2):
                                messages.warning(request, 'your are too late can not mark todays attendance')
                                return redirect('self_attendance')
                            else:
                                half_day = True
                                second_half = False
                                
                    else:
                        
                        if current_time > in_time + timedelta(hours=2):
                            half_day= True
                            first_half = True

                    month= get_month_year()
                    DailyAttendance.objects.create(emp_user_id=user_id,date=date,month=month,login_time=current_time,is_half_day=half_day,is_first_half=first_half,is_second_half=second_half,is_requested=True)
                    messages.success(request, "your daily attendance processed successfully")
                    

                else:
                    
                    
                    if daily_attendance[0].logout_time is None:
                        
                        
                        daily_attendance=DailyAttendance.objects.get(emp_user_id=user_id,date=date)
                        daily_attendance.logout_time = datetime.now().time().strftime("%H:%M:%S")
                        daily_attendance.save()
                        messages.success(request, "your Out time updated successfully")
                        
                        
                    else:
                        
                        messages.warning(request,'your request has already processed')
                    
                    
                    
                    
            else:
                messages.warning(request, "you are on the leave thats why your attendance not mark")

        else:
            messages.success(request,"Your todays attendance request added successfully")

        return redirect('self_attendance')




class MissedAttendance(View):
    
    @method_decorator(login_required(login_url='login'))
    def post(self, request):
        user_id = request.user.id
        data = request.POST

        date = datetime.today().date()
        pre_date = (date + relativedelta(days=-3))
        request_date =datetime.strptime(data['date'], "%Y-%m-%d").date()
    

        if request_date >= date  or request_date < pre_date:
            messages.warning(request,'You can\'t apply missing attendace for this date')
            return redirect('self_attendance')
        
    
        half_day= False
        first_half= False
        second_half= False

        missing_attendance= MissingAttendance.objects.filter(emp_user_id= user_id,date=data['date'])


        if missing_attendance.exists():
            messages.warning(request,'you all ready add request for this day')
            return redirect('self_attendance')

    
        if data['half_day'] == "True":
            half_day= True

            if data['first_half'] =='True':
                first_half= True
            else:
                second_half= True

        if half_day:
            MissingAttendance.objects.create(emp_user_id=user_id,date=data['date'],is_half_day=half_day, is_first_half=first_half,is_second_half=second_half,is_requested=True )
            messages.success(request,'added successfully')
            return redirect('self_attendance')
                        
        else:
            MissingAttendance.objects.create(emp_user_id=user_id,date=data['date'],is_half_day=False,is_requested=True)
            messages.success(request,'added successfully')
            return redirect('self_attendance')



        return redirect('self_attendance')


class AttendanceHistory(View):
    @method_decorator(login_required(login_url='login'))
    def get (self, request):
        user_id = request.user.id
        
        attendance_history = DailyAttendance.objects.filter(emp_user_id = user_id, month = get_month_year())
        month_name = attendance_history[0].month.month_name[0:-4] + ' ' + attendance_history[0].month.month_name[-4:]
    
        months = {month: index for index, month in enumerate(month_abbr) if month}
        month = int(months[attendance_history[0].month.month_name[0:3]])
        year = int(attendance_history[0].month.month_name[-4:])
        end_date = get_end_date_of_month(year, month)
        first_date = end_date.replace(day = 1).date()
        
        
        monthly_data= []
        
        date_range= pd.date_range(first_date,end_date)
        current_date= datetime.today().date()
        
        for date in date_range:
        
            if date.date() > current_date:
                break
        
            
            data= {
                'date': date.strftime("%d-%m-%Y"),
                'day':date.strftime("%a"),
                'status' :None,
                'login_time':None,
                'logout_time':None,
            }
            
            
            if Holiday.objects.filter(date=date).exists():
                
                data["status"]="H"
                data["login_time"]="-"
                data["logout_time"]="-"
                
            
            elif data["day"]== "Sat" or data["day"]== "Sun":
                data["status"]="WO"
                data["login_time"]="-"
                data["logout_time"]="-"

            else:
                leave = DailyLeave.objects.filter(emp_user_id = user_id, date=date)
                attendance = DailyAttendance.objects.filter(emp_user_id = user_id, date=date, is_present=True)
                
                if  leave.exists() and attendance.exists():
                    
                    if leave[0].date_is_half == True:
                        
                        if leave[0].date_is_first_half== True and attendance[0].is_second_half== True:
                            data["status"]="FHL SHP"
                            data["login_time"]= attendance[0].login_time
                            data["logout_time"]= attendance[0].logout_time
                            
                        
                        if leave[0].date_is_second_half== True and attendance[0].is_first_half== True:
                            data["status"]="FHP SHL"
                            data["login_time"]= attendance[0].login_time
                            data["logout_time"]= attendance[0].logout_time
            
                    else:
                        data["status"]="L"
                        data["login_time"]="-"
                        data["logout_time"]="-"
                        
                        
                elif leave.exists():
                    
                    if leave[0].date_is_half== True:
                        
                        if leave[0].date_is_first_half== True:
                            data["status"]="FHL SHA"
                        
                        elif leave[0].date_is_second_half== True:
                            data["status"]="FHA SHL"
                            
                    else:
                        data["status"]="L"
                        data["login_time"]="-"
                        data["logout_time"]="-"
            
                    
                elif attendance.exists():
                    
                    if attendance[0].is_half_day == True:
                    
                        if attendance[0].is_first_half== True:
                            data["status"]="FHP SHA"
                            data["login_time"]= attendance[0].login_time
                            data["logout_time"]= attendance[0].logout_time
                        
                        if attendance[0].is_second_half== True:
                            data["status"]="FHA SHP"
                            data["login_time"]= attendance[0].login_time
                            data["logout_time"]= attendance[0].logout_time
                        
                    else:
                        data["status"]="P"
                        data["login_time"]= attendance[0].login_time
                        data["logout_time"]= attendance[0].logout_time
                            
                                    
                else:
                    
                    
                    data["status"]="AB"
                    data["login_time"]="-"
                    data["logout_time"]="-"
                        
                
            
            monthly_data.append(data)
            
    
        
        return render (request, "account/self_services/self_attendance_history.html", {'monthly_data':monthly_data, 'month':month_name})