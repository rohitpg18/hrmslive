from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate,logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta,date
import pandas as pd
from dateutil.relativedelta import *
from account.models import *
from payroll.models import *
from decimal import Decimal
from calendar import Calendar, monthrange, month_abbr
import numpy as np
import re
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.validators import validate_email
from django.http import JsonResponse