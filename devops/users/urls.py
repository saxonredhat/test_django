from django.urls import path

from . import views

app_name='users'

urlpatterns = [
	path('', views.IndexListView.as_view(),name='index'),
	path('login/', views.UserLoginView.as_view(),name='user-login'),
	path('logout/', views.UserLogoutView.as_view(),name='user-logout'),
	path('protected/', views.ProtectedPageView.as_view(),name='protected'),
	path('needlogin/', views.NeedLoginView.as_view(),name='needlogin'),
	path('role/<int:pk>/', views.RoleDetailView.as_view(),name='role-detail'),
	path('role/delete/<int:pk>/', views.RoleDeleteView.as_view(),name='role-delete'),
	path('role/update/<int:pk>/', views.RoleUpdateView.as_view(),name='role-update'),
	path('role/add/', views.RoleCreateView.as_view(),name='role-add'),
	path('role/list/', views.RoleListView.as_view(),name='role-list'),
	path('user/list/', views.UserListView.as_view(),name='user-list'),
	path('user/add/', views.UserCreateView.as_view(),name='user-add'),
	path('user/delete/<int:pk>', views.UserDeleteView.as_view(),name='user-delete'),
	path('user/update/<int:pk>', views.UserUpdateView.as_view(),name='user-update'),
	path('user/<int:pk>/', views.UserDetailView.as_view(),name='user-detail'),
	path('permission/list/', views.PermissionListView.as_view(),name='permission-list'),
	path('permission/add/', views.PermissionCreateView.as_view(),name='permission-add'),
	path('permission/delete/<int:pk>', views.PermissionDeleteView.as_view(),name='permission-delete'),
	path('permission/update/<int:pk>', views.PermissionUpdateView.as_view(),name='permission-update'),
	path('menu/list/', views.MenuListView.as_view(),name='menu-list'),
	path('menu/add/', views.MenuCreateView.as_view(),name='menu-add'),
	path('menu/delete/<int:pk>', views.MenuDeleteView.as_view(),name='menu-delete'),
	path('menu/update/<int:pk>', views.MenuUpdateView.as_view(),name='menu-update'),
	path('menu/<int:pk>/', views.MenuDetailView.as_view(),name='menu-detail'),
]
