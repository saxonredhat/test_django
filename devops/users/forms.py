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
	

class ContactForm(forms.Form):
	name = forms.CharField()
	message = forms.CharField(widget=forms.Textarea)
	
	def send_email(self):
		pass
