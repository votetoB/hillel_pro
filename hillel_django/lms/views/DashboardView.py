from django.views.generic import TemplateView, ListView
from lms.models.Questionnaire import Questionnaire
from lms.forms.QuestionnaireForm import QuestionnaireForm


class DashboardView(TemplateView):
    template_name = 'lms/dashboard.html'

    def get_context_data(self, **kwargs):

        answer = {}
        # ...  Куча кода, которая как-то добавляет полезные данные в answer
        try:
            questionnaire = Questionnaire.objects.get(name="dashboard")
            questionnaire_form = QuestionnaireForm(instance=questionnaire)
            answer['questionnaire'] = {
                'form': questionnaire_form,
                'name': questionnaire.name,
                'id': questionnaire.id,
            }
        except Questionnaire.DoesNotExist:
            pass

        return answer



class QView(ListView):
    page_kwarg = 'stranitsa'

    def get_context_data(self, *, object_list=None, **kwargs):
        try:
            page = roman_to_int(self.request.get(self.page_kwarg, 'i'))
        except ValueError:
            pass
        else:
            self.request.GET.query_params[self.page_kwarg] = page
        return super(QView, self).get_context_data(object_list=object_list, **kwargs)

    def paginate_queryset(self, queryset, page_size):
        # Monkey-patched MultipleObjectMixin.get_queryset() with roman-numbers page

        """Paginate the queryset, if needed."""
        paginator = self.get_paginator(
            queryset,
            page_size,
            orphans=self.get_paginate_orphans(),
            allow_empty_first_page=self.get_allow_empty(),
        )

        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1

        try:
            page = roman_to_int(page)
        except ValueError:
            pass

        try:
            page_number = int(page)
        except ValueError:
            if page == "last":
                page_number = paginator.num_pages
            else:
                raise Http404(
                    _("Page is not “last”, nor can it be converted to an int.")
                )
        try:
            page = paginator.page(page_number)
            # Fix security issue
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(
                _("Invalid page (%(page_number)s): %(message)s")
                % {"page_number": page_number, "message": str(e)}
            )
