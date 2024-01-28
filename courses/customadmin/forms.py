from django.forms import ModelForm
from home.models import *

from . admin import models

for arr in models:
    model = arr[1]
class PredictionForm(ModelForm):
    class Meta:
        model = Predicted_stock
        fields = ["pub_date", "headline", "content", "reporter"]