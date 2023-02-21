from account.account_views.dependencies.dependencie import *


def get_end_date_of_month(year, month):
    """Return the last date of the month.
    
    Args:
        year (int): Year, i.e. 2022
        month (int): Month, i.e. 1 for January

    Returns:
        date (datetime): Last date of the current month
    """

    if month == 12:
        end_date = datetime(year, month, 31)
    else:
        end_date = datetime(year, month + 1, 1) + timedelta(days=-1)

    return end_date


month = int(datetime.now().strftime('%m'))
first_date = date.today().replace(day=25, month=month-1)
last_date = date.today().replace(day=25)

# initializing dates ranges
test_date1, test_date2 = first_date, last_date

# generating total days using busday_count()
res = np.busday_count(test_date1.strftime('%Y-%m-%d'),
                      test_date2.strftime('%Y-%m-%d'))

num_days = int((last_date - first_date).days)
weekdays = num_days - int(res)


def user_details(user_id, is_detail_required=False, detail=0, **kwargs):

    if User.objects.filter(id=user_id).exists() == False:
        return None

    if is_detail_required:
        if detail == 0:

            basic_detail = UserBasicDetails.objects.get(emp_user_id=user_id)
            additional_detail = UserAdditionalDetail.objects.get(
                emp_user_id=user_id)
            bank_detail = UserBankDetail.objects.get(emp_user_id=user_id)
            education_detail = UserEducationDetails.objects.get(
                emp_user_id=user_id)
            previous_organisation_detail = PreviousOrganisationDetail.objects.filter(
                emp_user_id=user_id)

            if basic_detail is None:
                basic_detail = UserBasicDetails.objects.create(
                    emp_user_id=user_id)

            if additional_detail is None:
                additional_detail = UserAdditionalDetail.objects.create(
                    emp_user_id=user_id)

            if bank_detail is None:
                bank_detail = UserBankDetail.objects.create(
                    emp_user_id=user_id)

            if education_detail is None:
                education_detail = UserEducationDetails.objects.create(
                    emp_user_id=user_id)

            if previous_organisation_detail is None:
                previous_organisation_detail = PreviousOrganisationDetail.objects.create(
                    emp_user_id=user_id)

            return {"basic_detail": basic_detail, "additional_detail": additional_detail, "bank_detail": bank_detail, "education_detail": education_detail, 'previous_organisation_detail': previous_organisation_detail}

        elif detail == 1:
            basic_detail = UserBasicDetails.objects.get(emp_user_id=user_id)
            if basic_detail is None:
                basic_detail = UserBasicDetails.objects.create(
                    emp_user_id=user_id)

            return basic_detail

        elif detail == 2:
            additional_detail = UserAdditionalDetail.objects.get(
                emp_user_id=user_id)

            if additional_detail is None:
                additional_detail = UserAdditionalDetail.objects.create(
                    emp_user_id=user_id)

            return additional_detail

        elif detail == 3:
            bank_detail = UserBankDetail.objects.get(emp_user_id=user_id)

            if bank_detail is None:
                bank_detail = UserBankDetail.objects.create(
                    emp_user_id=user_id)

            return bank_detail

        elif detail == 4:
            education_detail = UserEducationDetails.objects.get(
                emp_user_id=user_id)

            if education_detail is None:
                education_detail = UserEducationDetails.objects.filter(
                    emp_user_id=user_id)

            return education_detail

        elif detail == 5:
            previous_organisation_detail = PreviousOrganisationDetail.objects.filter(
                emp_user_id=user_id)

            if previous_organisation_detail is None:
                previous_organisation_detail = PreviousOrganisationDetail.objects.filter(
                    emp_user_id=user_id)
            return previous_organisation_detail

        else:
            return None


def is_profile_complete(user_id, **kwargs):

    user_detail = user_details(user_id, True, 0)

    if user_detail is not None:

        if user_detail["basic_detail"].is_verify or user_detail["basic_detail"].is_requested:

            return 'self_details'

        else:

            if user_detail["additional_detail"].is_completed_additional_details == False:

                return 'additional_details'

            elif user_detail["bank_detail"].is_completed_bank_details == False:

                return 'bank_details'

            elif user_detail["education_detail"].is_completed_academics == False:
                return 'educational_details'

            elif user_detail["previous_organisation_detail"][0].is_completed_previous_organisation_details == False and user_detail["previous_organisation_detail"][1].is_completed_previous_organisation_details == False and user_detail["previous_organisation_detail"][2].is_completed_previous_organisation_details == False and user_detail["basic_detail"].experience_status == "Experienced":

                return 'previous_organization_details'

            else:
                return 'self_details'

    return 'login'


def create_month_year_formate(date=0, is_current_month=True, month=0):

    if is_current_month:

        if month == 0:
            date = datetime.today()
            return str(date.strftime('%B')) + str(date.year)

        else:
            date = datetime.now()
            date = date + relativedelta(months=+month)

            return str(date.strftime('%B')) + str(date.year)

    else:
        if date == 0:
            date = datetime.today()
            return str(date.strftime('%B')) + str(date.year)
        else:

            return date + relativedelta(months=+month)


def get_month_year(month_name=0):

    if month_name == 0:
        month_name = create_month_year_formate()

    month = Month.objects.filter(month_name=month_name)

    if not month.exists():
        month = Month.objects.create(month_name=month_name)
    else:
        return month[0]


def monthly_leave_count(user_id, month_name=0):

    if User.objects.filter(id=user_id).exists() == False:
        return None

    if month_name == 0:
        month = get_month_year()  # get current month object

    leave_count = LeaveCount.objects.filter(emp_user_id=user_id, month=month)

    if not leave_count.exists():

        preview_month = get_month_year(create_month_year_formate(month=1))

        pre_month_leave_count = LeaveCount.objects.filter(emp_user_id=user_id, month=preview_month.id)

        if not pre_month_leave_count.exists():
            leave_count = LeaveCount.objects.create(emp_user_id=user_id, month=get_month_year(), sl_count=2, pl_count=2, cl_count=2)
            return leave_count

        else:
            sl_count = 2 + pre_month_leave_count[0].sl_count
            pl_count = 2 + pre_month_leave_count[0].pl_count
            cl_count = 2 + pre_month_leave_count[0].cl_count

            leave_count = LeaveCount.objects.create(emp_user_id=user_id, month=get_month_year(), sl_count=sl_count, pl_count=pl_count, cl_count=cl_count)

            return leave_count

    else:
        return leave_count[0]


def user_permissions(user_id):

    user = EmployeePermissions.objects.filter(emp_user_id=user_id)

    if user.exists():
        return user[0]
    else:
        return None


def month_attendance_counter(user_id, month_name=0):
    if User.objects.filter(id=user_id).exists() == False:
        return None

    if month_name == 0:
        month = get_month_year()  # get current month object

    holiday_month_count = Decimal(Holiday.objects.filter(date__gte=first_date, date__lte=last_date).count())  # returns count of holidays in current month

    month_attendance_count = MonthAttendanceCounter.objects.filter(emp_user_id=user_id, month=month)

    if not month_attendance_count.exists():
        month_attendance_count = MonthAttendanceCounter.objects.create(emp_user_id=user_id, month=month, present_days=0, absent_days=0, week_offs=weekdays,paid_leaves=0, non_paid_leaves=0, paid_holiday=holiday_month_count, sand_witched_days=0, total_paid_days=0, over_time_hours=0)
    else:
        month_attendance_count = month_attendance_count[0]

    # calculates no of present days in current month
    month_full_day_present_count = DailyAttendance.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, is_present=True).count()
    month_half_day_present_count = DailyAttendance.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, is_present=True, is_half_day=True).count()
    if month_full_day_present_count == 0:
        month_presenty_count = Decimal(month_half_day_present_count*0.5)
    else:
        month_presenty_count = Decimal(
            month_full_day_present_count - (month_half_day_present_count*0.5))

    # calculates no of sick leaves in current month
    month_full_day_sl_leaves = DailyLeave.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, leave_application__type='SL').count()
    month_half_day_sl_leaves = DailyLeave.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, leave_application__type='SL', date_is_half=True).count()
    if month_full_day_sl_leaves == 0:
        month_sl_count = Decimal(month_half_day_sl_leaves*0.5)
    else:
        month_sl_count = Decimal(
            month_full_day_sl_leaves - (month_half_day_sl_leaves * 0.5))

    # calculates no of personal leaves in curent month
    month_full_day_pl_leaves = DailyLeave.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, leave_application__type='PL').count()
    month_half_day_pl_leaves = DailyLeave.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, leave_application__type='PL', date_is_half=True).count()
    if month_full_day_pl_leaves == 0:
        month_pl_count = Decimal(month_half_day_pl_leaves*0.5)
    else:
        month_pl_count = Decimal(
            month_full_day_pl_leaves - (month_half_day_pl_leaves * 0.5))

    # calculates no of casual leaves in curent month
    month_full_day_cl_leaves = DailyLeave.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, leave_application__type='CL').count()
    month_half_day_cl_leaves = DailyLeave.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, leave_application__type='CL', date_is_half=True).count()
    if month_full_day_cl_leaves == 0:
        month_cl_count = Decimal(month_half_day_cl_leaves * 0.5)
    else:
        month_cl_count = Decimal(
            month_full_day_cl_leaves - (month_half_day_cl_leaves * 0.5))

    # calculates no of loss of pay leaves in curent month
    month_full_day_lop_leaves = DailyLeave.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, leave_application__type='LOP').count()
    month_half_day_lop_leaves = DailyLeave.objects.filter(emp_user_id=user_id, date__gte=first_date, date__lte=last_date, leave_application__type='LOP', date_is_half=True).count()
    if month_full_day_lop_leaves == 0:
        month_lop_count = Decimal(month_half_day_lop_leaves * 0.5)
    else:
        month_lop_count = Decimal(
            month_full_day_lop_leaves - (month_half_day_lop_leaves * 0.5))

    month_attendance_count.present_days = month_presenty_count

    month_attendance_count.paid_leaves = month_sl_count + month_pl_count + month_cl_count

    month_attendance_count.non_paid_leaves = month_lop_count

    month_attendance_count.total_paid_days = Decimal(month_attendance_count.present_days + month_attendance_count.paid_leaves + month_attendance_count.week_offs + month_attendance_count.paid_holiday)  # no of days for which salary is given

    month_attendance_count.absent_days = Decimal(num_days - (month_attendance_count.total_paid_days + month_attendance_count.non_paid_leaves))

    month_attendance_count.save()

    return month_attendance_count


def salary_slip(user_id, month_name=0):
    if User.objects.filter(id=user_id).exists() == False:
        return None

    if month_name == 0:
        month = get_month_year()  # get current month object

    month_attendance_count = MonthAttendanceCounter.objects.get(emp_user_id=user_id, month=month)
    user_additional_details = UserAdditionalDetail.objects.get(emp_user_id=user_id)
    user_details = UserBasicDetails.objects.get(emp_user_id=user_id)

    user_salary = user_details.salary
    per_day_sal = round(((user_salary)/num_days), 1)

    if num_days == month_attendance_count.total_paid_days:
        user_sal = user_salary
    else:
        user_sal = round(month_attendance_count.total_paid_days * per_day_sal)

    gross = round(Decimal(user_sal / 1.12))

    if gross <= 15000:
        gross = gross
    else:
        gross = user_sal - Decimal(1800)

    if user_details.is_salaried == False:
        gross = user_sal

    basic_sal = round(Decimal(0.50) * gross)
    hra_sal = round(Decimal(0.20) * gross)
    conveyance_allo = round(Decimal(0.20) * gross)
    utility_allo = round(Decimal(0.10) * gross)

    if gross <= 15000:
        pf_employee = round(gross * Decimal(0.12))
    else:
        pf_employee = 1800

    if gross <= 15000:
        pf_employer = round(gross * Decimal(0.12))
    else:
        pf_employer = 1800

    epf_employer = round(pf_employer * Decimal(0.7))

    eps_employer = round(pf_employer * Decimal(0.3))

    if gross <= 7500:
        prof_tax = 0
    elif gross >= 10001:
        if month_attendance_count.month.month_name[0:3] == 'Feb':
            prof_tax = 300
        else:
            prof_tax = 200
    elif gross >= 7501 and gross <= 10000:
        if user_additional_details.gender == 'Female' and month_attendance_count.month.month_name[0:3] == 'Feb':
            prof_tax = 0
        else:
            if user_additional_details.gender == 'Male':
                if month_attendance_count.month.month_name[0:3] == 'Feb':
                    prof_tax = 275
                else:
                    prof_tax = 175

    deduction = round(pf_employee + prof_tax)

    in_hand_sal = round(gross - pf_employee - prof_tax)

    current_month_salary = Salary.objects.filter(emp_user_id=user_id, month=month)

    if user_details.is_salaried == True:

        if not current_month_salary.exists():
            Salary.objects.create(emp_user_id=user_id, month=month, current_month_ctc=user_sal, basic_salary=basic_sal, house_rent_allowance=hra_sal, conveyance_allowance=conveyance_allo, utility_allowance=utility_allo,pf_employer=pf_employer, pf_employee=pf_employee,  profession_tax=prof_tax, epf_employer=epf_employer, eps_employer=eps_employer, gross_salary=gross, deductions=deduction, net_salary=in_hand_sal)
        else:
            current_month_salary.update(current_month_ctc=user_sal, basic_salary=basic_sal, house_rent_allowance=hra_sal, conveyance_allowance=conveyance_allo, utility_allowance=utility_allo, pf_employer=pf_employer,pf_employee=pf_employee,  profession_tax=prof_tax, epf_employer=epf_employer, eps_employer=eps_employer, gross_salary=gross, deductions=deduction, net_salary=in_hand_sal)
    else:
        if not current_month_salary.exists():
            Salary.objects.create(emp_user_id=user_id, month=month, basic_salary=basic_sal, house_rent_allowance=hra_sal, conveyance_allowance=conveyance_allo, utility_allowance=utility_allo,current_month_ctc=user_sal, pf_employer=0.00, pf_employee=0.00,  profession_tax=0.00, epf_employer=0.00, eps_employer=0.00, gross_salary=0.00, deductions=0.00, net_salary=user_sal)
        else:
            current_month_salary.update(basic_salary=basic_sal, house_rent_allowance=hra_sal, conveyance_allowance=conveyance_allo, utility_allowance=utility_allo, current_month_ctc=user_sal, pf_employer=0.00, pf_employee=0.00,  profession_tax=0.00, epf_employer=0.00, eps_employer=0.00, gross_salary=0.00, deductions=0.00, net_salary=user_sal)

    return current_month_salary


def validate(input_type, value):

    if input_type == 'mobile_number':
        regex = "[0-9]{10}"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if (re.search(p, str(value)) and
           len(str(value)) == 10):
            return True
        else:
            return False

    if input_type == 'pan_card':
        regex = "^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        p = re.compile(regex)
        if (value == None):
            return False
        if (re.search(p, value) and
           len(value) == 10):
            return True
        else:
            return False

    # for uan & adhar number
    if input_type == 'aadhar':
        regex = "^[0-9]{12}$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if (re.search(p, str(value)) and
           len(str(value)) == 12):
            return True
        else:
            return False

    if input_type == 'uan':
        regex = "^[0-9]{12}$"
        p = re.compile(regex)
        if (str(value) == None):
            return True
        if (re.search(p, str(value)) and
           len(str(value)) == 12):
            return True
        else:
            return False

    if input_type == 'ifsc_code':
        regex = "^[A-Z]{4}0[A-Z0-9]{6}$"
        p = re.compile(regex)
        if (value == None):
            return False
        if (re.search(p, value)):
            return True
        else:
            return False

    if input_type == 'bank_account_number':
        regex = "^[0-9]{9,18}$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if (re.search(p, str(value))):
            return True
        else:
            return False

    if input_type == 'salary':
        regex = "^[0-9]{3,7}$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if (re.search(p, str(value))):
            return True
        else:
            return False

    if input_type == 'names':
        regex = "^[A-Z]{1}[a-z]{1,19}$"
        p = re.compile(regex)
        if (value == None):
            return False
        if (re.search(p, value)):
            return True
        else:
            return False

    if input_type == 'percentage':
        regex = "^100(\.0{0,2})? *%?$|^\d{2}(\.\d{1,2})? *%?$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if (re.search(p, str(value))):
            return True
        else:
            return False

    if input_type == 'pf_number':
        regex = "^[A-Z]{2}[\\s\\/]?[A-Z]{3}[\\s\\/]?[0-9]{7}[\\s\\/]?[0-9]{3}[\\s\\/]?[0-9]{7}$"
        p = re.compile(regex)
        if (value == None):
            return True
        if (re.search(p, value)):
            return True
        else:
            return False

    if input_type == 'year':
        regex = "^[0-9]{4}$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if (re.search(p, str(value))):
            return True
        else:
            return False

    if input_type == 'address':
        regex = "^[-/.0-9a-zA-Z\s,-]{5,255}+$"
        p = re.compile(regex)
        if ((value) == None):
            return False
        if (re.search(p, value)):
            return True
        else:
            return False

    if input_type == 'email':
        try:
            validate_email(value)
        except ValidationError as e:
            return e
        else:
            return True
