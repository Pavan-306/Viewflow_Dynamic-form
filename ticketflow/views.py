from django import forms
from .models import TicketProcess, FormTemplate
from viewflow.workflow.flow.views import CreateProcessView

class DynamicStartView(CreateProcessView):
    model = TicketProcess

    def get_form_class(self):
        class DynamicForm(forms.ModelForm):
            class Meta:
                model = TicketProcess
                fields = ["form_template"]

        form_template_id = self.request.POST.get("form_template") or self.request.GET.get("form_template")
        if form_template_id:
            try:
                template = FormTemplate.objects.get(id=form_template_id)
                for field_name, config in template.form_definition.items():
                    field_type = config.get("type")
                    field_label = config.get("label", field_name)
                    required = config.get("required", False)

                    if field_type == "char":
                        DynamicForm.base_fields[field_name] = forms.CharField(
                            label=field_label,
                            required=required,
                            max_length=config.get("max_length", 255)
                        )
                    elif field_type == "int":
                        DynamicForm.base_fields[field_name] = forms.IntegerField(
                            label=field_label,
                            required=required,
                            min_value=config.get("min_value"),
                            max_value=config.get("max_value")
                        )
                    elif field_type == "text":
                        DynamicForm.base_fields[field_name] = forms.CharField(
                            label=field_label,
                            widget=forms.Textarea,
                            required=required
                        )
                    elif field_type == "choice":
                        DynamicForm.base_fields[field_name] = forms.ChoiceField(
                            label=field_label,
                            choices=[(c, c) for c in config.get("choices", [])],
                            required=required
                        )
            except FormTemplate.DoesNotExist:
                pass

        return DynamicForm