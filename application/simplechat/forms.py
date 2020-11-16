from django import forms
from rest_framework.exceptions import ValidationError

from .constants import MAX_PARTICIPANTS_NUMBER
from .models import Thread


class ThreadUpdateForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['participants']

    def clean(self):
        participants = self.cleaned_data.get('participants')
        if participants and participants.count() > MAX_PARTICIPANTS_NUMBER:
            raise ValidationError(f'Maximum {MAX_PARTICIPANTS_NUMBER} participants are allowed.')
        return self.cleaned_data
