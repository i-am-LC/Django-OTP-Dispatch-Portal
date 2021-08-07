import datetime
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# import decouple to retrieve secret keys
from decouple import config
# Import AWS Python SDK
import boto3
# Import phonenumbers to handle country codes.
import phonenumbers
from django.contrib.auth.decorators import login_required

# Import models here.
from django.contrib.auth.models import User
from .models import OneTimePasscodeSMS
from .forms import OneTimePasscodeVerificationForm



# Create your views here.

# Create random code and send to recipient via AWS SNS.
def otp_dispatcher_func(msn, region):

    # String defining chars OTP can be generated from. Uncomment to allow alphanumeric OTP.
    base_string = '0123456789' \
                 # 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                 # 'abcdefghijklmnopqrstuvwxyz'
    # Set your desired code length
    otp_length = 6
    # Make use of the random password function from Djangos User module.
    random_string = User.objects.make_random_password(length=otp_length, allowed_chars=base_string)

    # Define your SMS content.
    sms_message = str("This is a no reply message. \n\n"
                      "Please provide the below one time code when prompted. \n\n"
                      "Your code: ") + random_string
    sms_recipient = msn
    recipient_region = region
    # Using phonenumbers retrieve the correct number format.
    country_code = phonenumbers.parse(
        sms_recipient, recipient_region).country_code
    national = phonenumbers.parse(
        sms_recipient, recipient_region).national_number
    clean_msn = str(country_code) + str(national)

    # Create connection with AWS.
    aws_sns_connection = boto3.client("sns",
                                      aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                                      aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                                      region_name=config('AWS_REGION'))
    # Sender name which will appear on recipients device.
    sender_name = 'SENDER-NAME'

    # Send SNS via AWS using values set above.
    aws_sns_connection.publish(PhoneNumber=clean_msn,
                               Message=sms_message,
                               MessageAttributes={
                                   'AWS.SNS.SMS.SenderID': {
                                       'DataType': 'String',
                                       'StringValue': sender_name
                                   },
                                   'AWS.SNS.SMS.SMSType': {
                                       'DataType': 'String',
                                       'StringValue': 'Transactional'
                                   }
                               })
    # Return randomly generated string which will be saved against DB entry.
    return random_string

# Validate previously sent OTP.
@login_required
def otp_verification_page(request, pk):
    obj = get_object_or_404(OneTimePasscodeSMS, pk=pk)
    form = OneTimePasscodeVerificationForm()

    # On page load - If tries have been exceed then set record as failed and redirect to dash.
    if obj.attempts_remaining <= 0:
        messages.add_message(request, level=messages.ERROR,
                             message='Tries exceeded. Please send a new code to proceed.')
        obj.verified = False
        obj.save()
        return redirect('dashboard')
    # On page load - If time expired then set record as failed and redirect to dash.
    elif obj.expire_time < timezone.now():
        messages.add_message(request, level=messages.ERROR,
                             message='OTP expired. Please send a new code to proceed.')
        obj.verified = False
        obj.save()
        return redirect('dashboard')
    # If form submission.
    if request.method == 'POST':
        form = OneTimePasscodeVerificationForm(request.POST)
        if form.is_valid():
            submitted_otp = form.cleaned_data.get('otp_confirmed_val')
            # If OTP does not match that stored in DB subtract one try and return to validation page.
            if submitted_otp != obj.otp_dispatched_val:
                messages.add_message(request, level=messages.ERROR,
                                     message='OTP does not match.')
                obj.attempts_remaining -= 1
                obj.save()
            # Else if submission does match that stored in DB. Mark object as passed validation and return to dash.
            elif submitted_otp == obj.otp_dispatched_val:
                messages.add_message(request, level=messages.INFO,
                                     message='OTP validated successfully.')
                obj.otp_confirmed_val = submitted_otp
                obj.verified = True
                obj.verified_datetime = datetime.datetime.now()
                obj.save()
                return redirect('dashboard')

    return render(request, 'otp_dispatcher/otp_verification_page.html', {'form': form, 'obj': obj})