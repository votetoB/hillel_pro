from django.db import models
from redis.client import StrictRedis
from django.utils import timezone

redis_client = StrictRedis()


class Questionnaire(models.Model):
    name = models.CharField(max_length=50)
    amount_of_users_that_answered = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def cached_amount_of_users(self):
        answer = redis_client.get(f'cached_amount_of_users_{self.id}') or self.amount_of_users_that_answered
        if timezone.now() - self.last_updated_in_db > timezone.timedelta(days=12 * 3600):
            self.amount_of_users_that_answered = answer
            self.save(update_fields=['amount_of_users_that_answered'])
        return answer

    def increment_cached_amount_of_users(self, amount=1):
        return_value = redis_client.incrby(f'cached_amount_of_users_{self.id}', amount)
        if return_value == 1:
            # ...


class Question(models.Model):
    text = models.TextField()
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='questions')
    answer_type = models.CharField(max_length=20)  # TODO: and choices: text, integer


class QuestionnaireResponse(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.PROTECT)


class QuestionResponse(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    response = models.ForeignKey(QuestionnaireResponse, on_delete=models.CASCADE, related_name='question_responses')

    answer_text = models.TextField(null=True)
    answer_integer = models.PositiveSmallIntegerField(null=True)

    class Meta:
        unique_together = ('question', 'response')

    @property
    def answer(self):
        if self.question.answer_type == 'text':
            return self.answer_text

        assert self.question.answer_type == 'int'
        return self.answer_integer


class RedisLock:
    def __init__(self, key, timeout, release_on_exit=True):
        self.key = key
        self.timeout = timeout
        self.release_on_exit = release_on_exit
        self.acquired = False

    def acquire(self):
        return bool(redis_client.set(self.key, 0, nx=True, ex=self.timeout))

    def release(self):
        redis_client.delete(self.key)

    def __enter__(self):
        if self.acquire() is False:
            self.acquired = False
            raise ConflictException("Duplicate request!")

        self.acquired = True

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired is True and self.release_on_exit is True:
            self.release()
        else:
            assert self.acquired is False or self.release_on_exit is False
