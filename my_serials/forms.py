from django import forms
from . import models


class SerialForm(forms.ModelForm):
    class Meta:
        model = models.Serial
        fields = ('serial_id', )
