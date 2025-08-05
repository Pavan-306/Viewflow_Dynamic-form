from django.contrib import admin
from django.urls import path
from viewflow.contrib.auth import AuthViewset
from viewflow.urls import Site, Application
from viewflow.workflow.flow import FlowAppViewset
from ticketflow.flows import TicketFlow

site = Site(
    title="Ticket Workflow",
    viewsets=[
        Application(
            title="Jira Ticket Requests",
            app_name="ticketflow",
            viewsets=[FlowAppViewset(TicketFlow, icon="assignment")],
        )
    ]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', AuthViewset().urls),
    path('', site.urls),
]