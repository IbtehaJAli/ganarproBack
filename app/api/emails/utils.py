# utils.py
from django.core.mail import send_mail, EmailMessage


def send_email(user, contact, subject, body ):
    user_full_name = f"{user.first_name} {user.last_name}"
    user_email = user.outbound_email
    contact_email = contact.email
    email = EmailMessage(
        subject,
        body,
        from_email=f'{user_full_name} <{user_email}>',
        to=[contact_email],
        reply_to=[contact_email],
    )
