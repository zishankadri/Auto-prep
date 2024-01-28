from django import forms

from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'ans_a', 'ans_b', 'ans_c', 'ans_d', 'correct_ans']

        widgets = {
            'question': forms.Textarea(attrs={'placeholder': 'Question', 'rows': 2, 'class': 'question-input question', 'required':True}),
            'ans_a': forms.TextInput(attrs={'placeholder': 'A)', 'class': 'ans-input ans-a', 'required':True}),
            'ans_b': forms.TextInput(attrs={'placeholder': 'B)', 'class': 'ans-input ans-b', 'required':True}),
            'ans_c': forms.TextInput(attrs={'placeholder': 'C)', 'class': 'ans-input ans-c', 'required':True}),
            'ans_d': forms.TextInput(attrs={'placeholder': 'D)', 'class': 'ans-input ans-d', 'required':True}),
            'correct_ans': forms.Select(attrs={'class': 'regular-input correct-ans', 'required':True}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Add custome css class to all input widgets.
        # for field_name, field in self.fields.items():
            # current_class = field.widget.attrs.get('class') or ''
            # field.widget.attrs['class'] = current_class+" "+'regular-input'
