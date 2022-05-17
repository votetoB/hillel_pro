from hillel_django.celery import app
import logging


@app.task
def hochu_chto_to_sdelat(a, b):
    return a * b


@app.task
def send_email_about_new_response(q_id):
    __LOGGER.info(f"Sending email about {q_id}")


__LOGGER = logging.getLogger(__name__)
