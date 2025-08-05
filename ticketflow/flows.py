from django.contrib.auth import get_user_model
from viewflow import this
from viewflow.workflow import flow, lock
from viewflow.workflow.flow.views import CreateProcessView, UpdateProcessView
from .models import TicketProcess

User = get_user_model()

class TicketFlow(flow.Flow):
    process_class = TicketProcess
    lock_impl = lock.select_for_update_lock

    start = (
        flow.Start(
            CreateProcessView.as_view(
                model=TicketProcess,
                fields=["form_definition", "ticket_data"]
            )
        )
        .Annotation(title="Start Jira Ticket")
        .Permission(auto_create=True)
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