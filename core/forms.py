from django import forms
from .models import Student, Klass


class KlassForm(forms.ModelForm):
    class Meta:
        model = Klass
        fields = ['name', 'level']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Add custome css class to all input widgets.
        for field_name, field in self.fields.items():
            current_class = field.widget.attrs.get('class') or ''
            field.widget.attrs['class'] = current_class+" "+'regular-input'

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Add custome css class to all input widgets.
        for field_name, field in self.fields.items():
            current_class = field.widget.attrs.get('class') or ''
            field.widget.attrs['class'] = current_class+" "+'regular-input'



from paypal.standard.forms import PayPalPaymentsForm
from django.utils.html import format_html

class CustomPayPalPaymentsForm(PayPalPaymentsForm):
    # def get_html_submit_element(self):
    #     return """<button type="btn-primary"> Continue With PayPal </button>"""

    def render(self, *args, **kwargs):
        if not args and not kwargs:
            # `form.render` usage from template
            return format_html(
                """<form action="{0}" method="post">
                        {1}
                        <button type="submit" class="btn-primary"> Get Started </button>
                    </form>""",
                self.get_login_url(),
                self.as_p(),
                self.get_image(),
            )
        else:
            # Need to delegate to super. This provides
            # support for `as_p` method and for `BoundField.label_tag`,
            # and perhaps others.
            return super().render(*args, **kwargs)
