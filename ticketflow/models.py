from django.contrib.auth import get_user_model
from django.db import models
from viewflow.workflow.models import Process
from viewflow import jsonstore
from dynamic_forms.models import FormField, ResponseField


class FormTemplate(models.Model):
    name = models.CharField(max_length=200)
    form_definition = models.JSONField(default=dict, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FormSubmission(models.Model):
    template = models.ForeignKey(
        FormTemplate, on_delete=models.CASCADE, related_name="submissions"
    )
    response = ResponseField(default=dict)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Submission #{self.id} - {self.template.name if self.template else 'No Template'}"


class TicketProcess(Process):
    form_template = models.ForeignKey(
        FormTemplate, null=False, on_delete=models.PROTECT
    )

    ticket_data = jsonstore.JSONField(default=dict)
    approved_by_user = jsonstore.CharField(max_length=100, blank=True)
    approved_by_dev = jsonstore.CharField(max_length=100, blank=True)
    approved_by_ba = jsonstore.CharField(max_length=100, blank=True)
    approved_by_pm = jsonstore.CharField(max_length=100, blank=True)

    user_comment = jsonstore.TextField(blank=True)
    dev_comment = jsonstore.TextField(blank=True)
    ba_comment = jsonstore.TextField(blank=True)
    pm_comment = jsonstore.TextField(blank=True)

    def __str__(self):
        return f"TicketProcess for {self.form_template.name}"