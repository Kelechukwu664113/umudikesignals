from django import forms
from .models import SignalReport
from .models import LocationSuggestion


class SignalReportForm(forms.ModelForm):
    class Meta:
        model = SignalReport
        fields = ["provider", "rating", "used_router", "note"]

class LocationSuggestionForm(forms.ModelForm):
    class Meta:
        model = LocationSuggestion
        fields = ["suggested_name", "notes"]