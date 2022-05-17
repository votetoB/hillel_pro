from rest_framework import generics
from lms.serializers.QuestionnaireSerializer import QuestionnaireResponseSerializer


class QuestionnaireResponseViewRest(generics.CreateAPIView):
    serializer_class = QuestionnaireResponseSerializer

    # queryset = QuestionnaireResponse.objects.all()
