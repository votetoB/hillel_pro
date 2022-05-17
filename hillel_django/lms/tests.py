from django.test import client, TestCase

# Create your tests here.

from django.urls import reverse
from lms.models.Questionnaire import *


class TestQuestionnaire(TestCase):
    # @pytest.fixture
    # def client_instance(self):
    #     return client.Client()

    def setUp(self):
        for i in range(3):
            Questionnaire.objects.create(name=f"Questionnaire_{i}")

    def test_questionnaire_request(self):
        response = client.Client().get(path=reverse("lms:questionnaires_rest"))
        assert response.status_code == 200, "Error text"
        # print(response.data)
        assert len(response.data) == 3

    def test_questionnaire_response(self):
        response = client.Client()
