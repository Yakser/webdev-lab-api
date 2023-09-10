from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

User = get_user_model()


@shared_task
def notify_moderators_about_new_comment(author_fullname: str, comment_pk: int) -> None:
    context = {
        "author_fullname": author_fullname,
        "comment_pk": comment_pk,
    }

    # email_html_message = render_to_string("email/password_reset_email.html", context)
    email_plaintext_message = render_to_string("emails/new_comment.txt", context)

    moderators_emails = [
        moderator["email"]
        for moderator in User.objects.filter(is_staff=True).values("email")
    ]

    msg = EmailMultiAlternatives(
        "Новый комментарий | webdev-lab",
        email_plaintext_message,
        settings.EMAIL_HOST,
        moderators_emails,  # todo
    )
    # msg.attach_alternative(email_html_message, "text/html")
    msg.send()
