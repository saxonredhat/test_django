from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm,ContactForm
from django.views import View
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView,FormMixin 
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.contrib import messages
from django.urls.exceptions import NoReverseMatch 
from .models import User,Role,Permission,Menu
from django.contrib.auth.hashers import (
	check_password, is_password_usable, make_password,
)
import logging as log


# Create your views here.
class IndexListView(LoginRequiredMixin,
					ListView):
	template_name = 'users/index.html'
	queryset = Menu.objects.filter(is_topmenu=True)


class UserLoginView(View):
	"""User Login View
	"""
	form_class = LoginForm
	initial = {}
	template_name='users/login.html'

	def get(self,request):
		login_form=self.form_class(initial=self.initial)
		return render(request,self.template_name,{'login_form':login_form})

	def post(self,request):
		login_form=self.form_class(request.POST)
		if login_form.is_valid():
			username = login_form.cleaned_data.get("username")
			password = login_form.cleaned_data.get("password")
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request,user)
				return HttpResponseRedirect(reverse('users:index'))
		return render(request,self.template_name,{'login_form':login_form})

	def dispatch(self, request, *args, **kwargs):
		obj = super(UserLoginView,self).dispatch(request, *args, **kwargs)
		return obj


class UserLogoutView(LoginRequiredMixin,
					View):
	def get(self,request):
		logout(request)
		return HttpResponseRedirect(reverse('users:user-login'))


class ProtectedPageView(View):
	def get(self,request):
		return HttpResponse('ProtectedPage!!!')
		
	need_permisson='Capacity.add_env'
	decorators_list = (login_required,
					  )

	@method_decorator(decorators_list)
	def dispatch(self, request, *args, **kwargs):
		obj = super(ProtectedPageView,self).dispatch(request, *args, **kwargs)
		return obj


@method_decorator(login_required,name='dispatch')
class NeedLoginView(View):
	def get(self,request):
		return HttpResponse('Need Login Page!!!')
		
	def dispatch(self, request, *args, **kwargs):
		obj = super(NeedLoginView,self).dispatch(request, *args, **kwargs)
		return obj


class RoleListView(LoginRequiredMixin,
					PermissionRequiredMixin,
					ListView):
	permission_required = 'ROLE_VIEW'
	model = Role


class RoleDetailView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DetailView):
	permission_required = 'ROLE_VIEW'
	model = Role

class RoleForm(forms.ModelForm):
	permissions = forms.ModelMultipleChoiceField(
		widget=forms.CheckboxSelectMultiple,
		queryset=Permission.objects.filter(level=2),
		required=False,
	)
	class Meta:
		model = Role
		fields = '__all__'


class RoleCreateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					CreateView):
	permission_required = 'ROLE_ADD'
	template_name = 'users/user_form.html'
	form_class = RoleForm
	#fields = ['name','permissions']


class RoleDeleteView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DeleteView):
	permission_required = 'ROLE_DELETE'
	model = Role 
	success_url = reverse_lazy('users:role-list')


class RoleUpdateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					UpdateView):
	permission_required = 'ROLE_UPDATE'
	template_name = 'users/role_update_form.html'
	form_class = RoleForm
	model = Role


class UserListView(LoginRequiredMixin,
					PermissionRequiredMixin,
					ListView):
	permission_required = 'USER_VIEW'
	model = User 


class UserDetailView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DetailView):
	permission_required = 'USER_VEIW'
	model = User 


class UserCreateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					CreateView):
	permission_required = 'USER_ADD'
	model = User 
	fields = ['username','email','phone','password','roles','is_active']


	def get_form(self, form_class=None):
		form = super(UserCreateView, self).get_form(form_class)
		form.instance.user = self.request.user
		form.fields['password'].widget = forms.PasswordInput()
		return form

	def form_valid(self, form):
		form.instance.password = make_password(form.cleaned_data['password'])
		form.save()
		return super(UserCreateView, self).form_valid(form)


class UserDeleteView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DeleteView):
	permission_required = 'USER_DELETE'
	model = User 
	success_url = reverse_lazy('users:user-list')


class UserUpdateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					UpdateView):
	permission_required = 'USER_UPDATE'
	model = User 
	fields = ['username','email','phone','roles','is_active']


class PermissionListView(LoginRequiredMixin,
					PermissionRequiredMixin,
					ListView):
	permission_required = 'PERMISSION_VIEW'
	model = Permission 
	paginate_by = 10
	queryset = Permission.objects.all().order_by('seq')


class PermissionForm(forms.ModelForm):
	comment = forms.CharField(widget=forms.Textarea(attrs={'width':"100%",'cols':80,'rows':6}))
	parent_permission = forms.ModelChoiceField(
        queryset=Permission.objects.filter(level=1),
        required=False,
    )

	class Meta:
		model = Permission 
		fields = ['name', 'codename', 'level', 'parent_permission', 'seq', 'comment'] 


class PermissionCreateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					CreateView):
	permission_required = 'PERMISSION_ADD'
	template_name = 'users/permission_form.html'
	form_class = PermissionForm


class PermissionDeleteView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DeleteView):
	permission_required = 'PERMISSION_DELETE'
	model = Permission 
	success_url = reverse_lazy('users:permission-list')


class PermissionUpdateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					UpdateView):
	permission_required = 'PERMISSION_UPDATE'
	template_name = 'users/permission_update_form.html'
	form_class = PermissionForm	
	model = Permission 


class MenuListView(LoginRequiredMixin,
					PermissionRequiredMixin,
					ListView):
	permission_required = 'MENU_VIEW'
	model = Menu 
	template_name = 'users/menu_list.html'


class MenuDetailView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DetailView):
	permission_required = 'MENU_VIEW'
	model = Menu 


class MenuForm(forms.ModelForm):
	parent_menu = forms.ModelChoiceField(
		queryset=Menu.objects.filter(is_topmenu=True),
		required=False,
	)
	class Meta:
		model = Menu
		fields = '__all__'


class MenuCreateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					CreateView):
	permission_required = 'MENU_ADD'
	template_name = 'users/user_form.html'
	form_class = MenuForm


class MenuDeleteView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DeleteView):
	permission_required = 'MENU_DELETE'
	model = Menu 
	success_url = reverse_lazy('users:menu-list')


class MenuUpdateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					UpdateView):
	permission_required = 'MENU_UPDATE'
	template_name = 'users/menu_update_form.html'
	form_class = MenuForm	
	model = Menu 
