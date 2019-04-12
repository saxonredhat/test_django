from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
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
from django.contrib.auth.hashers import (
	check_password, is_password_usable, make_password,
)
from django_tables2 import SingleTableView,RequestConfig
import django_tables2 as tables
import itertools
from django_tables2.paginators import LazyPaginator

from .forms import UserCreateForm,UserUpdateForm,LoginForm,ContactForm,RoleCreateUpdateForm,PermissionCreateUpdateForm,DepartmentCreateUpdateForm
from .tables import UserTable,RoleTable,PermissionTable,DepartmentTable
from .models import User,Role,Permission,Menu,Department

import logging as log


# Create your views here.
class IndexListView(LoginRequiredMixin,
					ListView):
	template_name = 'users/index.html'
	queryset = Menu.objects.filter(is_topmenu=True)


class TestTable(tables.Table):
	class Meta:
		model = User
		template_name = 'django_tables2/bootstrap.html'

class NameTable(tables.Table):
	name = tables.Column()

data = [
{'name': 'Bradley'},
{'name': 'Stevie'},
]

class SimpleTable(tables.Table):
	row_number = tables.Column(empty_values=())
	id = tables.Column()
	age = tables.Column()
	
	def __init__(self, *args, **kwargs):
		super(SimpleTable, self).__init__( *args, **kwargs)
		self.counter = itertools.count()

	def render_row_number(self):
		return 'Row %d' % next(self.counter)

	def render_id(self, value):
		return '<%s>' % value

class UpperColumn(tables.Column):
	def render(self, value):
		return value.upper()

class Example(tables.Table):
	normal = tables.Column()
	upper = UpperColumn()

data = [{'normal': 'Hi there!',
         'upper': 'Hi there!'}]			

class SummingColumn(tables.Column):
	def render_footer(self, bound_column, table):
		return sum(bound_column.accessor.resolve(row) for row in table.data)

class MyTable(tables.Table):
	name = tables.Column()
	country = tables.Column(footer='Total:')
	id = SummingColumn()


class UserTable_test(tables.Table):
	#full_name = tables.Column(order_by={'last_name','first_name'})
	#actions = tables.Column(orderable=False)
	class Meta:
		model = User
		#sequence = ('first_name', 'last_name')

class UsefulMixin(tables.Table):
	extra = tables.Column()	

class TestTable(UsefulMixin, tables.Table):
	name = tables.Column()
	class Meta:
		attrs = {'class': 'table'}
		#template_name = 'django_tables2/semantic.html'
		template_name = 'django_tables2/bootstrap-responsive.html'


def test_table(request):
	#table = TestTable(User.objects.all())
	#table = NameTable(data)
	#table = SimpleTable([{'age': 31, 'id': 10}, {'age': 34, 'id': 11}])
	#table = Example(data)
	#table = UserTable_test(User.objects.all())
	table = TestTable(User.objects.all())
	#table.paginate(page=request.GET.get('page', 1), per_page=1)
	RequestConfig(request, paginate={'per_page': 2}).configure(table)
	#table = MyTable(User.objects.all())
	#RequestConfig(request).configure(table)
	return render(request,'users/test_table.html',{'my_table':table})	

class UserListTest(SingleTableView):
	model = User 
	table_class = UserTable_test 
	table_pagination = {
        'per_page': 2 
    }

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


class RoleListView(LoginRequiredMixin,
					PermissionRequiredMixin,
					SingleTableView):
	permission_required = 'ROLE_VIEW'
	model = Role
	table_class = RoleTable


class RoleDetailView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DetailView):
	permission_required = 'ROLE_VIEW'
	model = Role

class RoleForm(forms.ModelForm):
	permissions = forms.ModelMultipleChoiceField(
		widget=forms.CheckboxSelectMultiple,
		queryset=Permission.objects.filter(),
		required=False,
		label="权限",
	)
	class Meta:
		model = Role
		fields = '__all__'


class RoleCreateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					CreateView):
	permission_required = 'ROLE_ADD'
	form_class = RoleCreateUpdateForm 
	template_name = 'users/role_form.html'
	success_url = reverse_lazy('users:role-list') 


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
	model = Role
	template_name = 'users/role_update_form.html'
	form_class = RoleCreateUpdateForm 
	success_url = reverse_lazy('users:user-list')


class UserListView(LoginRequiredMixin,
					PermissionRequiredMixin,
					SingleTableView):
	permission_required = 'USER_VIEW'
	model = User
	table_class = UserTable

class UserDetailView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DetailView):
	permission_required = 'USER_VEIW'
	model = User 


class UserCreateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					CreateView):
	permission_required = 'USER_ADD'
	form_class = UserCreateForm
	template_name = 'users/user_form.html'
	success_url = reverse_lazy('users:user-list') 


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
	#initial = {'password':''}
	form_class = UserUpdateForm
	template_name = 'users/user_form.html'
	success_url = reverse_lazy('users:user-list')


class PermissionListView(LoginRequiredMixin,
					PermissionRequiredMixin,
					SingleTableView):
	permission_required = 'PERMISSION_VIEW'
	model = Permission 
	table_class = PermissionTable


class PermissionForm(forms.ModelForm):
	comment = forms.CharField(widget=forms.Textarea(attrs={'width':"100%",'cols':80,'rows':6}))
	parent_permission = forms.ModelChoiceField(
        queryset=Permission.objects.filter(),
        required=False,
    )

	class Meta:
		model = Permission 
		fields = ['name', 'codename', 'comment'] 


class PermissionCreateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					CreateView):
	permission_required = 'PERMISSION_ADD'
	form_class = PermissionCreateUpdateForm 
	template_name = 'users/permission_form.html'
	success_url = reverse_lazy('users:permission-list')


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
	form_class = PermissionCreateUpdateForm 
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


class DepartmentListView(LoginRequiredMixin,
					PermissionRequiredMixin,
					SingleTableView):
	permission_required = 'DEPARTMENT_VIEW'
	model = Department
	table_class = DepartmentTable
	template_name = 'users/department_list.html'


class DepartmentDetailView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DetailView):
	permission_required = 'DEPARTMENT_VIEW'
	model = Department 


class DepartmentForm(forms.ModelForm):
	class Meta:
		model = Department
		fields = '__all__'


class DepartmentCreateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					CreateView):
	permission_required = 'DEPARTMENT_ADD'
	template_name = 'users/department_form.html'
	form_class = DepartmentCreateUpdateForm 
	success_url = reverse_lazy('users:departement-list') 


class DepartmentDeleteView(LoginRequiredMixin,
					PermissionRequiredMixin,
					DeleteView):
	permission_required = 'DEPARTMENT_DELETE'
	model = Department 
	success_url = reverse_lazy('users:department-list')


class DepartmentUpdateView(LoginRequiredMixin,
					PermissionRequiredMixin,
					UpdateView):
	permission_required = 'DEPARTMENT_UPDATE'
	template_name = 'users/department_update_form.html'
	model = Department 
	form_class = DepartmentCreateUpdateForm 
	success_url = reverse_lazy('users:department-list')
