from rest_framework import generics
from lms.serializers.QuestionnaireSerializer import QuestionnaireSerializer
from lms.models.Questionnaire import Questionnaire


class QuestionnaireViewRest(generics.ListAPIView):
    serializer_class = QuestionnaireSerializer

    queryset = Questionnaire.objects.all()
