from django import forms
from account.models import Teams

class TeamsForm(forms.ModelForm):
    class Meta:
        model= Teams
        fields = ["team_name", "leader_name", "employees"]