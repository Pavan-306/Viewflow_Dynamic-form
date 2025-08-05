from django.contrib.auth import get_user_model
from django.db import models
from viewflow.workflow.models import Process
from viewflow import jsonstore

class FormDefinition(models.Model):
    title = models.CharField(max_length=200)
    field_schema = models.JSONField(
        default=list,
        help_text='e.g. [{"name":"summary","type":"text","label":"Summary?","required":true}]'
    )
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class TicketProcess(Process):
    form_definition = models.ForeignKey(
        FormDefinition, null=False, on_delete=models.PROTECT)
    
    ticket_data = jsonstore.JSONField(default=dict)
    approved_by_user = jsonstore.CharField(max_length=100, blank=True)
    approved_by_dev = jsonstore.CharField(max_length=100, blank=True)
    approved_by_ba = jsonstore.CharField(max_length=100, blank=True)
    approved_by_pm = jsonstore.CharField(max_length=100, blank=True)

    user_comment = jsonstore.TextField(blank=True)
    dev_comment = jsonstore.TextField(blank=True)
    ba_comment = jsonstore.TextField(blank=True)
    pm_comment = jsonstore.TextField(blank=True)