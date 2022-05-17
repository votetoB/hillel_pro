import time, random
from django.views import View
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from lms.models.Questionnaire import *
from django.shortcuts import HttpResponse
from django.db import transaction
from lms.tasks import hochu_chto_to_sdelat, send_email_about_new_response
from lms.forms.QuestionnaireForm import QuestionnaireForm
from django.utils.translation import get_language, gettext, gettext_lazy as _

from django.db.models import Q, F


class QuestionnaireResponseView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        answer = _("Dear {}, thanks for your response").format(name=request.user.username)

        # if self.request.is_ajax() is False:
        #     raise ValidationError("This request has to be ajax")

        form_data = dict(**request.POST)
        form_data['questionnaire_id'] = kwargs['questionnaire_id']
        # User 1 ...
        form = QuestionnaireForm(
            data=form_data
        )  # User 2
        form.is_valid()
        q_response = form.save()

        send_email_about_new_response.delay(q_response.id)

        if random.random() > 0.5:
            questionnaire = q_response.questionnaire
            questionnaire.increment_cached_amount_of_users()
            questionnaire.amount_of_users_that_answered = F('amount_of_users_that_answered') + 1
            questionnaire.save(update_fields=['amount_of_users_that_answered'])
        else:
            # second option
            Questionnaire.objects.filter(
                id=q_response.questionnaire_id
            ).update(amount_of_users_that_answered=F('amount_of_users_that_answered') + 1)

        query1 = Q(id=q_response.questionnaire_id)
        query2 = Q(id2=q_response.questionnaire_id)

        qs = Question.objects
        return HttpResponse(answer)
