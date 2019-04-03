from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm


# Create your views here.
def UserLogin(request):
	#判断是否为post
	login_form=LoginForm(request.POST or None)
	if login_form.is_valid():
		username = login_form.cleaned_data.get("username")
		password = login_form.cleaned_data.get("password")
		print(username,password)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request,user)
			return HttpResponseRedirect(reverse('users:needlogin'))
	return render(request,'users/login.html',{'login_form':login_form})


@login_required
def NeedLogin(request): 
	return HttpResponse('needlogin page')
