from lms.models.Questionnaire import *
from django import forms


class QuestionnaireForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionnaireForm, self).__init__(*args, **kwargs)
        assert isinstance(self.instance, Questionnaire)
        for question in self.instance.questions.all():
            if question.answer_type == 'integer':
                self.fields[f"question_{question.id}"] = forms.IntegerField(label=question.text)
            else:
                assert question.answer_type == 'text'
                self.fields[f"question_{question.id}"] = forms.CharField(max_length=200, label=question.text)

    def clean(self):
        # TODO: add validation
        answer = {}
        for field_name, field_value in self.data.items():
            if field_name == 'questionnaire_id':
                answer['questionnaire_id'] = field_value

            elif field_name.startswith('question_'):
                question = Question.objects.get(id=field_name[len('question_'):])
                answer[question.id] = {f'answer_{question.answer_type}': field_value}

        return answer

    def save(self, commit=True):
        response = QuestionnaireResponse.objects.create(
            questionnaire_id=self.cleaned_data.pop('questionnaire_id')
        )
        for question_id, answer in self.cleaned_data.items():
            QuestionResponse.objects.create(
                response=response,
                question_id=question_id,
                **answer,
            )
        return response

    class Meta:
        model = Questionnaire
        fields = (
        )
