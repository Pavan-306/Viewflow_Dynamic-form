from django.contrib import admin
from .models import FormDefinition, TicketProcess

@admin.register(FormDefinition)
class FormDefinitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created')

@admin.register(TicketProcess)
class TicketProcessAdmin(admin.ModelAdmin):
    readonly_fields = (
        'ticket_data',
        'approved_by_user', 'approved_by_dev',
        'approved_by_ba', 'approved_by_pm',
        'user_comment','dev_comment','ba_comment','pm_comment'
    )
    list_display = ('id', 'form_definition',)