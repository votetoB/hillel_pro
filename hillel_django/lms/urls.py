from django.urls import path
from lms.views.QuestionnaireResponseViewRest import QuestionnaireResponseViewRest
from lms.views.QuestionnaireViewRest import QuestionnaireViewRest

app_name = "lms"

urlpatterns = [
    path('questionnaire_responses/', QuestionnaireResponseViewRest.as_view(), name='questionnaire_responses_rest'),
    path('questionnaires/', QuestionnaireViewRest.as_view(), name='questionnaires_rest'),
    # path('questionnaire_response/<int:questionnaire_id>/', QuestionnaireResponseView.as_view(), name='questionnaire_response'),
]
