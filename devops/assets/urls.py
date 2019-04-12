from django.urls import path

from . import views

app_name='assets'

urlpatterns = [
	path('dashboard/', views.dashboard,name='dashboard'),
	path('dashboard_test/', views.dashboard_test,name='dashboard_test'),
	path('list/', views.AssetsListView.as_view(),name='assets-list'),
	path('add/', views.AssetsCreateView.as_view(),name='assets-add'),
	path('index/', views.index,name='index'),
	path('detail/<int:pk>/', views.detail,name='detail'),
]
