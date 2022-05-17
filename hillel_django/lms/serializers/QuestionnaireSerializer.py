from rest_framework import serializers, exceptions
from lms.models.Questionnaire import *


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
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
            'cached_amount_of_users',
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


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = (
            'id',
            'question',
            'response',
            'answer_text',
            'answer_integer'
        )

        validators = []
        extra_kwargs = {
            'response': {
                'required': False,
            }
        }

    def validate_answer_integer(self, value):
        if not (0 < value < 10):
            raise exceptions.ValidationError("Answer should be between 0 and 10")

        return value

    def validate(self, attrs):
        # attrs = {
        #     'question': Question(),
        #     'response': QuestionnaireResponse(),
        #     'answer_text': '123',  # None
        #     'answer_integer': None,  # 3
        # }
        if 'response' in attrs:
            print("RESPONSE")
        else:
            print("NO RESPONSE")
        question = attrs['question']
        # assert isinstance(response, QuestionnaireResponse)
        response = attrs.get('response')
        if response is not None and question.questionnaire_id != response.questionnaire_id:
            raise exceptions.ValidationError("This question is from a different questionnaire")

        assert isinstance(question, Question)
        if question.answer_type == 'integer':
            if attrs.get('answer_text') is not None or attrs.get('answer_integer') is None:
                raise exceptions.ValidationError("This questions should have integer answer")
        if question.answer_type == 'text':
            if attrs.get('answer_integer') is not None or attrs.get('answer_text') is None:
                raise exceptions.ValidationError("This questions should have text answer")

        return attrs


class QuestionnaireResponseSerializer(serializers.ModelSerializer):
    question_responses = QuestionResponseSerializer(many=True)

    class Meta:
        model = QuestionnaireResponse
        fields = (
            'id',
            'questionnaire',
            'question_responses',
        )

    def create(self, validated_data):
        # validated_data['user'] = self.context['request'].user
        question_responses = validated_data.pop('question_responses')
        response = super(QuestionnaireResponseSerializer, self).create(validated_data)
        errors_list = []
        required_questions_to_answer = set(Question.objects.filter(
            questionnaire_id=response.questionnaire_id,
            # required=True,
        ).values_list('id', flat=True))

        for question_response_data in question_responses:
            question_response_data['response'] = response.id

            question_response_data['question'] = question_response_data['question'].id
            required_questions_to_answer.remove(question_response_data['question'])
            question_response_serializer = QuestionResponseSerializer(data=question_response_data)
            if question_response_serializer.is_valid(raise_exception=False) is False:
                errors_list.append(question_response_serializer.errors)

            if not errors_list:
                question_response_serializer.save()

        if required_questions_to_answer:
            raise exceptions.ValidationError({'not_answered': required_questions_to_answer})

        if errors_list:
            raise exceptions.ValidationError(errors_list)

        return response
