from rest_framework import generics
from lms.serializers.QuestionnaireSerializer import QuestionnaireSerializer
from lms.models.Questionnaire import Questionnaire
from rest_framework.response import Response

from django.db import connection


class QuestionnaireViewRest(generics.ListAPIView):
    serializer_class = QuestionnaireSerializer

    queryset = Questionnaire.objects.prefetch_related('questions')

    def list(self, request, *args, **kwargs):
        print(f"BEFORE WAS len({connection.queries}")
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print(f"AFTER WAS len({connection.queries}")
        return Response(serializer.data)
