from app.api.emails.models import UserEmail


def time_sent_and_count_per_project(user, oppid):

    time_sent, user_emails_count = UserEmail.objects.time_sent_and_email_count_per_project(user, oppid)
    return time_sent, user_emails_count
