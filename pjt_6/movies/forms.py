from django import forms
from .models import Movie, Comment

class MovieForm(forms.ModelForm):
    class Meta: 
        model = Movie # Movie Model을 참고
        exclude = ('user', )

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content', )
