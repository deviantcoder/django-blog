from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail


def send_verification_email(user):
    """
    Sends an email verification link to the specified user.

    This function generates a unique verification URL for the user by encoding
    their primary key (UID) and creating a token using Django's 
    PasswordResetTokenGenerator. The verification URL is then embedded in an 
    email template and sent to the user's email address.
    """

    token_generator = PasswordResetTokenGenerator()

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = token_generator.make_token(user)
    domain = settings.DOMAIN
    verify_url = f'{domain}/account/verify-email/{uid}/{token}'

    subject = 'Email Verification'
    message = render_to_string(
        'emails/verification_email.html',
        {
            'user': user,
            'verify_url': verify_url,
        }
    )

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=message
    )
