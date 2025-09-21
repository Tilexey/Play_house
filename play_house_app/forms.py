from django import forms
from .models import Booking
from datetime import date

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['place', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Скрываем поле place, так как оно будет установлено автоматически
        self.fields['place'].widget = forms.HiddenInput()
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("Час завершення повинен бути пізніше за час початку")
        
        return cleaned_data