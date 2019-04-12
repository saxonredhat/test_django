from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import User,Role,Permission,Department 

class LoginForm(forms.ModelForm):
	class Meta:
		model = User 
		fields = ('username','password')
		widgets = {
			'password': forms.PasswordInput(),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Login'))

	def clean(self):
		return self.cleaned_data 

class UserCreateForm(forms.ModelForm):
	class Meta:
		model = User
		widgets = {
			'password': forms.PasswordInput(),
		}
		fields = ['username','email','phone', 'department','password','roles','is_superuser','is_active']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', '保存'))

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password"])
		if commit:
			user.save()
		return user

			
	
class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		widgets = {
			'password': forms.PasswordInput(),
		}
		fields = ['id','username','email','phone', 'department','roles','is_superuser','is_active']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', '修改'))


class ContactForm(forms.Form):
	name = forms.CharField()
	message = forms.CharField(widget=forms.Textarea)
	
	def send_email(self):
		pass

class RoleCreateUpdateForm(forms.ModelForm):
	permissions = forms.ModelMultipleChoiceField(
		widget=forms.CheckboxSelectMultiple,
		queryset=Permission.objects.filter(),
		required=False,
		label = '权限',
	)
	class Meta:
		model = Role 
		fields = ['name','comment','permissions']
		widgets = {
			'comment': forms.Textarea(attrs={'rows':4}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', '保存'))

class PermissionCreateUpdateForm(forms.ModelForm):
	class Meta:
		model = Permission 
		fields = ['name','codename','comment']
		widgets = {
			'comment': forms.Textarea(attrs={'rows':4}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', '保存'))


class DepartmentCreateUpdateForm(forms.ModelForm):
	class Meta:
		model = Department 
		fields = ['name','comment']
		widgets = {
			'comment': forms.Textarea(attrs={'rows':4}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', '保存'))
