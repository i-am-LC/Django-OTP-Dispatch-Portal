# import decouple to retrieve secret keys
from decouple import config
# Import AWS Python SDK
import boto3
# Import phonenumbers to handle country codes.
import phonenumbers

# Import models here.
from django.contrib.auth.models import User

# TODO Your test number and region/country goes here.
msn = '0412345678'
region = 'AU'

# String defining chars OTP can be generated from.
base_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
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
aws_sns_connection = boto3.client("sns", aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                                  aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                                  region_name=config('AWS_REGION'))
# Sender name which will appear on recipients device.
sender_name = 'SENDER-NAME'

# Send SNS via AWS using values set above.
aws_sns_connection.publish(PhoneNumber=clean_msn, Message=sms_message, MessageAttributes={
    'AWS.SNS.SMS.SenderID': {
        'DataType': 'String', 'StringValue': sender_name
    },
    'AWS.SNS.SMS.SMSType': {
        'DataType': 'String',
        'StringValue': 'Transactional'}
    })