from django import forms
from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta: 
        model = Movie # Movie Model을 참고
        fields = '__all__'