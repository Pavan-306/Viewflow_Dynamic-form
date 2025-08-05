from django import forms
from .models import FormDefinition, TicketProcess

TYPE_MAP = {
    'text': forms.CharField,
    'textarea': lambda **kwargs: forms.CharField(widget=forms.Textarea, **kwargs),
    'integer': forms.IntegerField,
    'boolean': forms.BooleanField,
}

class DynamicJSONForm(forms.Form):
    """
    Build a form dynamically from the given field_schema (list of dicts).
    """

    def __init__(self, *args, schema=None, initial=None, **kwargs):
        super().__init__(*args, **kwargs)
        assert isinstance(schema, list), "schema must be a list"
        for fd in schema:
            name = fd['name']
            field_cls = TYPE_MAP.get(fd.get('type', 'text'), forms.CharField)
            self.fields[name] = field_cls(
                label=fd.get('label', name.capitalize()),
                required=fd.get('required', False),
                initial=(initial or {}).get(name)
            )

class ApprovalForm(forms.Form):
    """
    Step form used by each approver: whether approved + comment.
    """
    decision = forms.ChoiceField(
        choices=[('approved', 'Approve'), ('rejected', 'Reject')],
        widget=forms.RadioSelect
    )
    comment = forms.CharField(widget=forms.Textarea, required=False)