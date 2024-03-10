from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_activation_email(recipient_email):
    subject = "Registerd your account on " + settings.SITE_NAME
    from_email = settings.EMAIL_HOST_USER
    to = [recipient_email]
    # Load the Html template

    try:
        html_content = render_to_string('account/activation_email.html')
        # create the email body with both HTML and plain text versions
        text_content = strip_tags(html_content)

        email_message= EmailMultiAlternatives(subject, text_content, from_email, to)
        email_message.attach_alternative(html_content, "text/html")

        email_message.send()
    except Exception as e:
        # Handle the exception (log, print, etc.)
        print(f"Error sending activation email: {str(e)}")
def send_reset_password_email(recipient_email,reset_url):
    subject = "Reset your password on " + settings.SITE_NAME
    from_email = settings.EMAIL_HOST_USER
    to = [recipient_email]
    # Load the Html template

    try:
        html_content = render_to_string('account/reset_password_email.html',{'reset_url': reset_url})
        # create the email body with both HTML and plain text versions
        text_content = strip_tags(html_content)

        email_message= EmailMultiAlternatives(subject, text_content, from_email, to)
        email_message.attach_alternative(html_content, "text/html")

        email_message.send()
    except Exception as e:
        # Handle the exception (log, print, etc.)
        print(f"Error sending activation email: {str(e)}")
