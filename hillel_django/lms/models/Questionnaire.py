from django.db import models


class Questionnaire(models.Model):
    name = models.CharField(max_length=50)


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
