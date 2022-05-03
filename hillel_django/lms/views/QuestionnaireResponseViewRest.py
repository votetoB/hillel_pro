from rest_framework import generics
from lms.serializers.QuestionnaireSerializer import QuestionnaireResponseSerializer
from lms.models.Questionnaire import QuestionnaireResponse


class QuestionnaireResponseViewRest(generics.CreateAPIView):
    serializer_class = QuestionnaireResponseSerializer

    # queryset = QuestionnaireResponse.objects.all()
