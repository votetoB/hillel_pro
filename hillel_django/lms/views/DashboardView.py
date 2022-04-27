from django.views.generic import TemplateView, DetailView
from lms.models.Questionnaire import Questionnaire
from lms.forms.QuestionnaireForm import QuestionnaireForm


class DashboardView(TemplateView):
    template_name = 'lms/dashboard.html'

    def get_context_data(self, **kwargs):
        answer = {}
        # ...  Куча кода, которая как-то добавляет полезные данные в answer
        try:
            questionnaire = Questionnaire.objects.get(name="dashboard")
            questionnaire_form = QuestionnaireForm(instance=questionnaire)
            answer['questionnaire'] = {
                'form': questionnaire_form,
                'name': questionnaire.name,
                'id': questionnaire.id,
            }
        except Questionnaire.DoesNotExist:
            pass

        return answer
