from django import forms
from .models import Sign_up,mynotes

class sign_form(forms.ModelForm):
    class Meta:
        model = Sign_up
        fields = "__all__"

class notesform(forms.ModelForm):
    class Meta:
        model = mynotes
        fields = "__all__"

class updateform(forms.ModelForm):
    class Meta:
        model = Sign_up
        fields = ["firstname",'lastname','username','password','city','state','mobil']   #optional

