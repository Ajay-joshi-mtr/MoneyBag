from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.models import User
from accounting.helpers import AccHelper
from django.db import IntegrityError,transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta
from calendar import monthrange

def login(request):
    """
    Handles authentication
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            messages.info(request,'Welcome, Login successfull!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username/Password is not valid!')
            return redirect('/')
    else:
        return render(request, 'base/login.html')


def register(request):
    """
    Handles registration
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        if password == confirm_password:
            user_exists = User.objects.filter(email=email)
            if user_exists:
                messages.error(request, "Account already exists!")
                return redirect('register')
            else:
                with transaction.atomic():
                    try:
                        user = User.objects.create_user(username=username,
                                                        email=email,
                                                        password=password)
                        AccHelper.create_all_basic_acc_heads(user)
                        AccHelper.add_dashboard_metas(user)
                        return render(request, 'base/thanks.html')
                    except IntegrityError:
                        messages.error(request, "Internal error! Contact with support.")
                        return redirect('register')

        else:
            messages.error(request, 'Password did not match!')
            return redirect('register')
    else:
        return render(request, 'base/sign_up.html')

@login_required
def dashboard(request):
    meta_data = AccHelper.get_meta_data(request.user)
    meta_data['balance'] = meta_data['total_income'] - meta_data['total_expense']
    meta_data['rp_or_adm'] = meta_data['total_receivable'] - meta_data['total_payable']
    donut_chart_data = AccHelper.get_expenses(request.user)

    current_date = datetime.today()
    #todays income expense
    # today = current_date.strftime('%Y-%m-%d')
    today_inc_exp = AccHelper.get_income_expense_in_range(request.user,current_date,current_date)

    #yesterday income expense
    yester_day_date  = current_date + relativedelta(days=-1)
    # yester_day = yester_day_date.strftime('%Y-%m-%d')
    yester_day_inc_exp = AccHelper.get_income_expense_in_range(request.user,yester_day_date,yester_day_date)

    #this week income expense
    this_week_start  = current_date - timedelta(days=current_date.weekday()+2)
    this_week_end  = this_week_start + timedelta(days=6)
    this_week_inc_exp = AccHelper.get_income_expense_in_range(request.user,this_week_start,this_week_end)


    # this week income expense
    last_week_end = this_week_start - timedelta(days=1)
    last_week_start = last_week_end - timedelta(days=6)
    last_week_inc_exp = AccHelper.get_income_expense_in_range(request.user,last_week_start,last_week_end)

    #this month income expense
    _, num_days = monthrange(current_date.year, current_date.month)
    this_month_start = date(current_date.year, current_date.month, 1)
    this_month_end = date(current_date.year, current_date.month, num_days)
    this_month_inc_exp = AccHelper.get_income_expense_in_range(request.user,this_month_start,this_month_end)

    # last month income expense
    _, num_days = monthrange(current_date.year, current_date.month-1)
    last_month_start = date(current_date.year, current_date.month-1, 1)
    last_month_end = date(current_date.year, current_date.month-1, num_days)
    last_month_inc_exp = AccHelper.get_income_expense_in_range(request.user, last_month_start, last_month_end)

    context = {
        'meta_data':meta_data,
        'donut_chart_data': json.dumps(donut_chart_data,cls=DjangoJSONEncoder),
        'today' : today_inc_exp,
        'yester_day' : yester_day_inc_exp,
        'this_week' : this_week_inc_exp,
        'last_week' : last_week_inc_exp,
        'this_month' : this_month_inc_exp,
        'last_month' : last_month_inc_exp,
    }
    return render(request, 'base/dashboard.html',context)

@login_required
def logout(request):
    messages.add_message(request, messages.SUCCESS, 'Your are successfully logged out.')
    auth.logout(request)
    return redirect('login')

@login_required
def change_password(request):
    """
        Handles password change
        :param request:
        :return:
        """
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == old_password:
            messages.error(request, 'new password and old one can not be same!')
            return redirect('change_password')
        if password != confirm_password:
            messages.error(request, 'Confirm password did not match!')
            return redirect('change_password')

        current_user = User.objects.get(id=request.user.id)
        if not current_user.check_password(old_password):
            messages.error(request, 'Old password did not match!')
            return redirect('change_password')

        current_user.set_password(password)
        current_user.save()
        update_session_auth_hash(request, current_user)  # Important!
        messages.info(request, 'Password change successfullly!')
        return redirect('dashboard')

    else:
        return render(request, 'base/change_password.html')