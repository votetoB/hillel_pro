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

    def save(self, commit=True):
        raise Exception("DON'T TRY TO SAVE HEAR")

    class Meta:
        model = Questionnaire
        fields = (
        )
