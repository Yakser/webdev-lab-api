import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "service.settings")

app = Celery("service")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(5.0, test.s("hello"), name="add every 10")

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour="7", minute="30", day_of_week="1"),
        test.s("Happy Mondays!"),
    )


@app.task
def test(arg):
    print(arg)


app.autodiscover_tasks()


app.conf.timezone = "UTC"
