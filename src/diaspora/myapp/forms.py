from django import forms
from . import models


class ArduinoSettings(forms.Form):
    pass


class AddArduinoForm(forms.ModelForm):
    class Meta:
        model = models.Arduino
        fields = ['name', 'path', 'description']
