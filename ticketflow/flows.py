from django.contrib.auth import get_user_model
from viewflow import this
from viewflow.workflow import flow, lock
from viewflow.workflow.flow.views import UpdateProcessView
from .models import TicketProcess
from .views import DynamicStartView

User = get_user_model()


class TicketFlow(flow.Flow):
    process_class = TicketProcess
    lock_impl = lock.select_for_update_lock
    start = (
        flow.Start(
            DynamicStartView.as_view()
        )
        .Annotation(title="Start Jira Ticket")
        .Permission(auto_create=True)
        .Next(this.save_ticket_data)
    )

    save_ticket_data = (
        flow.Function(
            lambda activation: _save_ticket_data(activation)
        )
        .Annotation(title="Save Ticket Data")
        .Next(this.user_approval)
    )

    user_approval = (
        flow.View(
            UpdateProcessView.as_view(
                model=TicketProcess,
                fields=["approved_by_user", "user_comment"]
            )
        )
        .Annotation(title="User Approval")
        .Permission(auto_create=True)
        .Next(this.dev_approval)
    )

    dev_approval = (
        flow.View(
            UpdateProcessView.as_view(
                model=TicketProcess,
                fields=["approved_by_dev", "dev_comment"]
            )
        )
        .Annotation(title="Developer Approval")
        .Permission(auto_create=True)
        .Next(this.ba_approval)
    )

    ba_approval = (
        flow.View(
            UpdateProcessView.as_view(
                model=TicketProcess,
                fields=["approved_by_ba", "ba_comment"]
            )
        )
        .Annotation(title="BA Approval")
        .Permission(auto_create=True)
        .Next(this.pm_approval)
    )

    pm_approval = (
        flow.View(
            UpdateProcessView.as_view(
                model=TicketProcess,
                fields=["approved_by_pm", "pm_comment"]
            )
        )
        .Annotation(title="PM Approval")
        .Permission(auto_create=True)
        .Next(this.end)
    )

    end = flow.End()


def _save_ticket_data(activation):
    process = activation.process
    if hasattr(activation, 'form') and activation.form.is_valid():
        process.ticket_data = activation.form.cleaned_data
        process.save()