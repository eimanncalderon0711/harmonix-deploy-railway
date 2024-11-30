from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(email, code):
    subject = 'Your Verification Code'
    message = f'''Hello {email}, \n\n
    Before you finish creating your account, we need to verify your identity. 
    On the verification page, enter the following 
    
    CODE: {code}
    
    Your verification code expires after 2 minutes.
    '''
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])