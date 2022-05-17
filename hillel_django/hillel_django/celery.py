from celery import Celery
import celery


class CeleryConfig:
    beat_schedule = {

    }


app = Celery(**{})

app.config_from_object(CeleryConfig)
