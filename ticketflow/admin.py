import json
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import FormTemplate, FormSubmission, TicketProcess

@admin.register(FormTemplate)
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')


@admin.register(FormSubmission)
class FormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('template', 'submitted_at')
    readonly_fields = ('display_response',)

    def display_response(self, obj):
        if not obj.response:
            return mark_safe("<i>No response data</i>")
        try:
            parsed = json.loads(obj.response)
            pretty_json = json.dumps(parsed, indent=2, ensure_ascii=False)
            return mark_safe(f"<pre>{pretty_json}</pre>")
        except (json.JSONDecodeError, TypeError):
            return mark_safe(f"<i>Invalid JSON:</i> {obj.response}")

    display_response.short_description = "Response"


@admin.register(TicketProcess)
class TicketProcessAdmin(admin.ModelAdmin):
    readonly_fields = (
        'ticket_data',
        'approved_by_user', 'approved_by_dev',
        'approved_by_ba', 'approved_by_pm',
        'user_comment', 'dev_comment', 'ba_comment', 'pm_comment'
    )
    list_display = ('id', 'form_template')