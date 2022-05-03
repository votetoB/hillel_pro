from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from lms.models.Questionnaire import *
from django.shortcuts import HttpResponse
from django.db import transaction
from lms.tasks import hochu_chto_to_sdelat



class QuestionnaireResponseView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        questionnaire_id = kwargs['questionnaire_id']

        # if self.request.is_ajax() is False:
        #     raise ValidationError("This request has to be ajax")

        form_data = request.POST
        # {
        #     'question_123': '123123',
        #     'question_234': 3,
        # }
        questionnaire = get_object_or_404(Questionnaire, id=questionnaire_id)

        response = QuestionnaireResponse.objects.create(
            user=User.objects.first(),
            questionnaire=questionnaire,
        )

        for question_string, answer in form_data.items():
            if question_string.startswith("question") is False:
                continue

            question_id = question_string.split("_")[1]
            question = get_object_or_404(Question.objects.filter(questionnaire=questionnaire), id=question_id)

            if question.answer_type == 'integer':
                answer_kwargs = {
                    'answer_integer': answer,  # TODO: add validation
                }
            else:
                assert question.answer_type == 'text'
                answer_kwargs = {
                    'answer_text': answer,  # TODO: add validation
                }

            QuestionResponse.objects.create(
                response=response,
                question=question,
                **answer_kwargs,
            )

        return HttpResponse("You answer has been received")
