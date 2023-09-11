import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")

app = Celery("service")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # sender.add_periodic_task(
#     #     crontab(hour="7", minute="30"),
#     #     test.s("Happy Mondays!"),
#     # )
#     sender.add_periodic_task(10.0, send_statistics_to_admins_task.s(), name="add every 10")


app.conf.timezone = "UTC"
