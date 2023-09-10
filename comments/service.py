from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from comments.models import Comment

User = get_user_model()


def notify_moderators_about_new_comment(comment: Comment) -> None:
    context = {
        "user": comment.author,
        "comment": comment,
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
