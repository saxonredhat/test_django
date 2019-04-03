from django.urls import path

from . import views

app_name='users'

urlpatterns = [
	path('login/', views.UserLogin,name='login'),
	path('needlogin/', views.NeedLogin,name='needlogin')
]
