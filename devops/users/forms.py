from django import forms
from .models import User 

class LoginForm(forms.ModelForm):
	class Meta:
		model = User 
		fields = ('username','password')
		widgets = {
            'password': forms.PasswordInput(),
        }
	def clean(self):
		return self.cleaned_data 
	
