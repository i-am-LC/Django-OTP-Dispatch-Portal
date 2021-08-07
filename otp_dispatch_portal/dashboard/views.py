from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
import datetime

# Load model from OTP dispatcher app
from otp_dispatcher.models import OneTimePasscodeSMS
# Load form from OTP dispatcher app
from otp_dispatcher.forms import OneTimePasscodeSMSForm
# Load OTP dispatcher views.
from otp_dispatcher.views import otp_dispatcher_func

# Create your views here.

# Project dashboard / landing page. Will only allow access to authorised users.
@login_required
def dashboard(request):

    form = OneTimePasscodeSMSForm()
    # Retrieve all previous OTP records.
    previous_dispatches = OneTimePasscodeSMS.objects.all().order_by('-created')
    # Create pagination.
    page = request.GET.get('page', 1)
    paginator = Paginator(previous_dispatches, 10)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    # If form submission.
    if request.method == 'POST':
        form = OneTimePasscodeSMSForm(request.POST)
        if form.is_valid():
            # retrieve cleaned form values.
            msn = form.cleaned_data.get('mobile_number')
            country = form.cleaned_data.get('country')
            skipped = form.cleaned_data.get('skip_verification')

            instance = form.save(commit=False)
            instance.created_by = request.user
            # If skip validation is selected proceed to save without calling OTP dispatcher func.
            if skipped:
                instance.verified_datetime = datetime.datetime.now()
                instance.save()
                messages.add_message(request, level=messages.INFO,
                                     message='OTP verification skipped.')
                return redirect('dashboard')
            # if skip was not selected we'll proceed with OTP dispatch.
            else:
                # Try opt dispatcher function. If exception return dash with error message
                try:
                    # otp_code is received by dispatcher.
                    otp_code = otp_dispatcher_func(msn, country)
                    instance.otp_dispatched_val = otp_code
                    # set expire time to 5 mins from form submission.
                    instance.expire_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
                    instance.save()
                    messages.add_message(request, level=messages.INFO,
                                         message='OTP dispatched.')
                    return redirect('otp_verification_page', pk=instance.pk)

                except:
                    messages.add_message(request, level=messages.ERROR,
                                         message='An error has occurred. OTP not dispatched.')
                    return redirect('dashboard')

    return render(request, 'dashboard/dashboard.html', {'form': form, 'records': records})