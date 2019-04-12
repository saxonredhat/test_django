import django_tables2 as tables
from django.urls import reverse
from django_tables2.utils import A
from .models import User,Role,Permission,Department


class UserTable(tables.Table):
	edit = tables.TemplateColumn(
		verbose_name='操作',
		template_name='users/tables/update_delete_column.html',
		extra_context={'update_url':'users:user-update','delete_url':'users:user-delete'},
		attrs={'th': {'class': 'nosort'}}
	)
	class Meta:
		model = User 
		orderable = False
		attrs = {
			'id': 'example1',
			'class': 'table table-bordered table-striped',
		}
		fields = ('username','email','phone','department','roles','is_active','is_superuser')


class RoleTable(tables.Table):
	edit = tables.TemplateColumn(
		verbose_name='操作',
		template_name='users/tables/update_delete_column.html',
		extra_context={'update_url':'users:role-update','delete_url':'users:role-delete'},
		attrs={'th': {'class': 'nosort'}}
	)
	#all_permissions = tables.Column(verbose_name='拥有的权限')
	class Meta:
		model = Role 
		orderable = False
		attrs = {
			'id': 'example1',
			'class': 'table table-bordered table-striped',
		}
		fields = ('name','comment')


class PermissionTable(tables.Table):
	edit = tables.TemplateColumn(
		verbose_name='操作',
		template_name='users/tables/update_delete_column.html',
		extra_context={'update_url':'users:permission-update','delete_url':'users:permission-delete'},
		attrs={'th': {'class': 'nosort'}}
	)
	class Meta:
		model = Permission 
		orderable = False
		attrs = {
			'id': 'example1',
			'class': 'table table-bordered table-striped',
		}
		fields = ('name','codename','comment',)

class DepartmentTable(tables.Table):
	edit = tables.TemplateColumn(
		verbose_name='操作',
		template_name='users/tables/update_delete_column.html',
		extra_context={'update_url':'users:department-update','delete_url':'users:department-delete'},
		attrs={'th': {'class': 'nosort'}}
	)
	class Meta:
		model = Department 
		orderable = False
		attrs = {
			'id': 'example1',
			'class': 'table table-bordered table-striped',
		}
		fields = ('name','comment',)
