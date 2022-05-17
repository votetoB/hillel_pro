from django.contrib import admin
from django.contrib.admin import site
from lms.models.Questionnaire import *
from django.utils.safestring import mark_safe

from django.utils import timezone


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):

    search_fields = ['name', ]
    inlines = [QuestionInline, ]

    list_display = (
        'name',
        # 'priority',
        'some_field',
    )

    def some_field(self, instance: Questionnaire):
        return mark_safe('<a href="https://google.com.ua">Some text</a>')

    def some_action(self, request, queryset):
        i = 0
        for questionnaire in queryset:
            i += 1
            # some_action(questionnaire)
        from django.contrib import messages
        self.message_user(request, f"Done something with {i} objects", level=messages.WARNING)

    actions = ['some_action']


class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse


@admin.register(QuestionnaireResponse)
class QuestionnaireResponseAdmin(admin.ModelAdmin):
    fields = (
        'user',
        'questionnaire',
    )

    inlines = [QuestionResponseInline]

    autocomplete_fields = ('user', 'questionnaire')

    list_display = (
        'user',
        'id',
        'questionnaire'
    )
