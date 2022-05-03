from hillel_django.celery import app


@app.task
def hochu_chto_to_sdelat(a, b):
    return a * b



