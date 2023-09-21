
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token
from .models import Realtor, Renter






def send_renter_verification_mail (recipient , first_name, last_name):
    subject = 'Realtest Market Verification'
    message = f' Hi {first_name} {last_name}, Thank you for joining realest market us! please click on the link to activate your account '
    from_email = 'your-gmail-email@gmail.com' # realest market email
    recipient_list = [str(recipient)]
    send_mail(subject, message, from_email, recipient_list)


def send_realtor_account_creation_mail (recipient):
    subject = 'Realtest Market Business Verication'
    message = ' Hi , Thank you for joining realest market us! Please submit your business document, to enable you list your properties  '
    from_email = 'your-gmail-email@gmail.com' # realest market email
    recipient_list = [str(recipient)]
    send_mail(subject, message, from_email, recipient_list)

def verify_phone_number ():
    pass



def getAuthUserId(request):
     
    # Get the authentication token from the headers
    auth_token = request.META.get('HTTP_AUTHORIZATION', '')
    msg = {'error' : True }

    try:  
        # Get the Token object associated with the provided token
        token_obj = Token.objects.get(key=auth_token)
        # print(token_obj.user)
        # Get the user associated with the token
        id = token_obj.user.id
        msg['error'] = False 
        msg['id'] = id 
        return msg
    except Exception as e:
        msg['msg'] = "invalid token"
        return  msg
    

def flush_user_token(request):
    # Get the authentication token from the headers
    auth_token = request.META.get('HTTP_AUTHORIZATION', '')
    msg = {'error' : True }
    try:  
        # Get the Token object associated with the provided token
        token_obj = Token.objects.get(key=auth_token)
        token_obj.delete()
        return True
    except Exception as e:
        return False 
        





