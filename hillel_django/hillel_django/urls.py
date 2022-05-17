from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from lms.views.DashboardView import DashboardView
from lms.views.QuestionnaireResponseView import QuestionnaireResponseView
from lms import urls as lms_urls
import redis


urlpatterns = [
    path('admin/', admin.site.urls),
    path('lms/', include(lms_urls, namespace='lms')),
    path('', DashboardView.as_view(), name='dashboard'),
    path('questionnaire_response/<int:questionnaire_id>/', QuestionnaireResponseView.as_view(), name='questionnaire_response'),
    # path('dancers/', DancerView.as_view(), name='dancers'),  # GET - list of dancers. POST - create a dancer
    # path('dancer/<uuid:dancer_id>/', DancerView.as_view(), name='dancer'),
    # path('group/<uuid:group_id>/students/', DancerView.as_view(), name='dancers'),
    # GET - single dancer PUT/PATCH - modify dancer. DELETE - delete dancer
]
