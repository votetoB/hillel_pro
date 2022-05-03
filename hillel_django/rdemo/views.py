from rest_framework import views, serializers, response, status, generics, permissions, pagination
from lms.models.Questionnaire import *


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'text',
            'answer_type',
        )


class QuestionnaireSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Questionnaire
        fields = (
            'id',
            'name',
            'questions',
        )

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        questionnaire = super().create(validated_data)
        for q in questions_data:
            q['questionnaire'] = questionnaire
            s = QuestionSerializer(q)
            s.is_valid(raise_exception=True)
            s.save()
        return questionnaire


class QuestionnaireView(generics.RetrieveAPIView):
    serializer_class = QuestionnaireSerializer
    lookup_field = 'id'
    queryset = Questionnaire.objects.all()


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = (
            'question',
            'response',
        )

        validators = []
        extra_kwargs = {
            'response': {
                'required': False,
            }
        }


class ResponseSerializer(serializers.ModelSerializer):
    question_responses = QuestionResponseSerializer(many=True)

    class Meta:
        model = QuestionnaireResponse
        fields = (
            'questionnaire',
            'question_responses',
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        question_responses = validated_data.pop('question_responses')
        response = super().create(validated_data)
        for question_response_data in question_responses:
            question_response_data['response'] = response
            question_response_serializer = QuestionResponseSerializer(question_response_data)
            question_response_serializer.is_valid(raise_exception=True)
            question_response_serializer.save()

        return response


class ResponseView(generics.CreateAPIView):
    serializer_class = ResponseSerializer
