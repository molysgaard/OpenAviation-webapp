from django.forms import ModelForm
from models import Height, HeightBounds, Airspace

class HeightForm(forms.Form):
    def is_valid():
        if (super.is_valid()):

    class Meta:
        model = Height
