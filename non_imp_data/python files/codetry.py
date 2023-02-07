
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def validate (input_type, value):
    
    if input_type == 'mobile_number':
        regex = "[0-9]{10}"
        p = re.compile(regex)
        if(str(value) == None):
            return False  
        if(re.search(p, str(value)) and
           len(str(value)) == 10):
            return True
        else:
            return False
        
    if input_type == 'pan_card':
        regex = "^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        p = re.compile(regex)
        if(value == None):
            return False  
        if(re.search(p, value) and
           len(value) == 10):
            return True
        else:
            return False 
    
    # for uan & adhar number
    if input_type == 'aadhar': 
        regex = "^[0-9]{12}$"
        p = re.compile(regex)
        if(str(value) == None):
            return False  
        if(re.search(p, str(value)) and
           len(str(value)) == 12):
            return True
        else:
            return False
        
    if input_type == 'ifsc_code':
        regex = "^[A-Z]{4}0[A-Z0-9]{6}$"
        p = re.compile(regex)
        if (value == None):
            return False
        if(re.search(p, value)):
            return True
        else:
            return False
    
    if input_type == 'bank_account_number':
        regex = "^[0-9]{9,18}$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if(re.search(p, str(value))):
            return True
        else:
            return False
    
    if input_type == 'salary':
        regex = "^[0-9]{3,7}$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if(re.search(p, str(value))):
            return True
        else:
            return False
        
    if input_type == 'names':
        regex = "^[A-Z]{1}[a-z]{1,19}$"
        p = re.compile(regex)
        if (value == None):
            return False
        if(re.search(p, value)):
            return True
        else:
            return False
        
    if input_type == 'percentage':
        regex = "^100(\.0{0,2})? *%?$|^\d{2}(\.\d{1,2})? *%?$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if(re.search(p, str(value))):
            return True
        else:
            return False
    
    
    if input_type == 'pf_number':
        regex = "^[A-Z]{2}[\\s\\/]?[A-Z]{3}[\\s\\/]?[0-9]{7}[\\s\\/]?[0-9]{3}[\\s\\/]?[0-9]{7}$"
        p = re.compile(regex)
        if (value == None):
            return False
        if(re.search(p, value)):
            return True
        else:
            return False
    
    if input_type == 'year':
        regex = "^[0-9]{4}$"
        p = re.compile(regex)
        if (str(value) == None):
            return False
        if(re.search(p, str(value))):
            return True
        else:
            return False
        
    if input_type == 'address':
        regex = "^[-/.0-9a-zA-Z\s,-]{5,255}+$"
        p = re.compile(regex)
        if ((value) == None):
            return False
        if(re.search(p, value)):
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
    
    




























































# from datetime import datetime, timedelta, date
# from dateutil.relativedelta import *

# def create_month_year_formate(date=0,is_current_month=True,month=0):
    
    
        
#     if is_current_month:
        
#         if month == 0:
#             date = datetime.today()
#             return str(date.strftime('%B')) + str(date.year)
            
#         else:
#             date = datetime.now()
#             date = date + relativedelta(months=+month)
            
#             return str(date.strftime('%B')) + str(date.year)
    
#     else:
#         if date == 0:
#             date = datetime.today()
#             return str(date.strftime('%B')) + str(date.year)
#         else:
            
#             return date + relativedelta(months=+month)


# print(create_month_year_formate())


# from datetime import date, timedelta

# def daterange(start_date, end_date):
#     for n in range(int((end_date - start_date).days)):
#         yield start_date + timedelta(n)

# start_date = date(2013, 1, 1)
# end_date = date(2013, 6, 2)
# for single_date in daterange(start_date, end_date):
#     print(single_date.strftime("%Y-%m-%d"))

# from datetime import datetime
# from datetime import datetime, timedelta

# current_time = datetime.now().time().strftime("%H:%M:%S")
# current_time = datetime.strptime(current_time, "%H:%M:%S")

# a= current_time + timedelta(hours=2)
# if current_time < a:
#     print(a)

# a = 'May2023'

# print((a[-1:-5:-1])[::-1]
# print(((a[::-1])[4::])[::-1] + ' ' + ((a[-1:-5:-1])[::-1]) )
# print(a[0:-4] + ' ' +a[-4:])

# def get_last_date_of_month(year, month):
#     """Return the last date of the month.
    
#     Args:
#         year (int): Year, i.e. 2022
#         month (int): Month, i.e. 1 for January

#     Returns:
#         date (datetime): Last date of the current month
#     """
    
#     if month == 12:
#         last_date = datetime(year, month, 31)
#     else:
#         last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
    
#     return last_date.strftime("%Y-%m-%d")

# year = int(datetime.now().year)

# month = int(datetime.now().strftime('%m'))

# first_date = date.today().replace(day=1)

# last_date = get_last_date_of_month(year, month)
# last_date = get_last_date_of_month(2024, 2)

# print(first_date)
# print(last_date)

# from datetime import timedelta, date

# Date_req = date.today() + timedelta(days=3)

# print(type(Date_req))


# Python3 code to demonstrate working of
# Business days in range
# Using timedelta() + sum() + weekday()

# from datetime import datetime, timedelta

# month = int(datetime.now().strftime('%m'))
# first_date = date.today().replace(day=25, month = month-1)
# last_date = date.today().replace(day=25)
  
# initializing dates ranges
# test_date1, test_date2 = first_date, last_date
  
# printing dates
# print("The original range : " + str(test_date1) + " " + str(test_date2))
  
# generating dates
# dates = (test_date1 + timedelta(idx + 1)
#          for idx in range((test_date2 - test_date1).days))
  
# summing all weekdays
# res = sum(1 for day in dates if day.weekday() < 5)
  
# printing
# # print("Total business days in range : " + str(res))

# from datetime import date, datetime, timedelta
# import numpy as np

# month = int(datetime.now().strftime('%m'))
# first_date = date.today().replace(day=26, month = month-1)
# last_date = date.today().replace(day=25)

# # initializing dates ranges 
# test_date1, test_date2 = first_date, last_date
  
# # printing dates 
# print("The original range : " + str(test_date1) + " " + str(test_date2))
  
# # generating total days using busday_count()
# res = np.busday_count(test_date1.strftime('%Y-%m-%d'),
#                       test_date2.strftime('%Y-%m-%d'))
  
# # printing 
# print("Total business days in range : " + str(res))

# num_days = last_date - first_date

# num_days = int ((last_date - first_date).days)

# print((num_days) + 1)

# weekdays = num_days + 1 - int(res)

# print(weekdays)

# def validate (input_type, value):
#     if input_type == 'pan_card':
#         if len(str(value)) > 10 or len(str(value))<10:
#             return ("False2")
        
#         elif str(value).isalnum() == True:
#             return ("Fal")
        
        
        
# print(validate("pan_card", "QWERTY1IOP"))
# from account.account_views.dependencies.dependencie import *
# import re 
# def isValid(Z): 
#     Result=re.compile("[A-Za-z]{5}\d{4}[A-Za-z]{1}") 
#     return Result.match(Z)
# # Driver Code 
# Z="ABCDE9999K"
# # if (isValid(Z)):  
# #     print ("It's a Valid PAN Number")      
# # else : 
# #     print ("Invalid PAN Number entered.")

# def validate (input_type, value):
#     if input_type == 'mobile_number':
#         if type(value) != int:
#             return False
#         elif len(str(value)) > 10 or len(str(value))<10:
#             return False
#         else:
#             return True
        
#     if input_type == 'pan_card':
#         try:
#             validate_email(value)
#         except ValidationError as e:
#             return False
#         else:
#             return True
        
        
        
        
        # if value[-1] != '%':
        #     return value+''+' %'
        # else:
        #     return value
        
#         regex = "^100(\.0{0,2})? *%?$|^\d{2}(\.\d{1,2})? *%?$"

#         # Compile the ReGex
#         p = re.compile(regex)

#         # If the PAN Card number
#         # is empty return false
#         if(value == None):
#             return False

#         # Return if the PAN Card number
#         # matched the ReGex
#         if re.search(p, value):
#             return True
#         else:
#             return False
# #             result = re.compile("[A-Za-z]{5}\d{4}[A-Za-z]{1}")
# #             return result.match(value)
    


# print(validate("pan_card",'At/post-tarapur, taluka- pandharpur, dist-solapur 413304' ))


 
    