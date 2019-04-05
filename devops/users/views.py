from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate,login
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

from .models import Publisher,Book,Author
import logging as log


# Create your views here.

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
				return HttpResponseRedirect(reverse('users:needlogin'))
		return render(request,self.template_name,{'login_form':login_form})

	def dispatch(self, request, *args, **kwargs):
		obj = super(UserLoginView,self).dispatch(request, *args, **kwargs)
		return obj


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


class PublisherList(ListView):
	model = Publisher
	template_name='users/publisher_list.html'
	context_object_name = 'publisher_list'


class PublisherDetail(DetailView):
	model = Publisher
	template_name='users/publisher_detail.html'
	#queryset = Publisher.objects.all()
	
	def get_contenxt_data(self, **kwargs):
		context = super(PublisherDetail, self).get_context_data(**kwargs)
		context['book_list'] = Book.objects.all()
		return context


class BookList(ListView):
	queryset = Book.objects.order_by('-publication_date')
	context_object_name = 'book_list'
	template_name = 'users/book_list.html'


class PublisherBookList(SingleObjectMixin, ListView):
	paginate_by = 2
	template_name = 'users/publisher_book_list.html'

	def get(self, request,**kwargs):
		log.info('## Enter Function get() ##')
		self.object = self.get_object(queryset=Publisher.objects.all())
		try:
			return super(PublisherBookList, self).get(self,request,**kwargs)
		finally:
			log.info('## Leave Function get() ##')

	def get_queryset(self):
		log.info('## Enter Function get_queryset() ##')
		try:
			return self.object.book_set.all()
		finally:
			log.info('## Leave Function  get_queryset() ##')

	def get_context_data(self, **kwargs):
		log.info('## Enter Function get_context_data() ##')
		context = super(PublisherBookList, self).get_context_data(**kwargs)
		context['publisher'] = self.object
		log.info('## leave Function get_context_data() ##')
		log.info(context)
		try:
			return context
		finally:
			log.info('## leave Function get_context_data() ##')

class AcmeBookList(ListView):
	context_object_name = 'book_list'
	queryset = Book.objects.filter(publisher__name='ACME Publishing')
	template_name = 'books/acme_list.html'

class AuthorInterestForm(forms.Form):
	message = forms.CharField()

class AuthorDetail(FormMixin, DetailView):
	model = Author
	form_class = AuthorInterestForm
	
	def get_success_url(self):
		return reverse('author-detail', kwargs={'pk': self.object.pk})
	
	def get_context_data(self, **kwargs):
		context = super(AuthorDetail, self).get_context_data(**kwargs)
		context['form'] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		return super(AuthorDetail, self).form_valid(form)


class RecordInterest(SingleObjectMixin, View):
	model = Author
	
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return HttpResponseForbidden()
		self.object = self.get_object()
		return HttpResponseRedirect(reverse('users:author-detail', kwargs={'pk': self.object.pk}))


class AuthorDetailView(DetailView):
	queryset = Author.objects.all()
	template_name = 'users/author_detail.html'
	
	def get_object(self):
		object = super(AuthorDetailView, self).get_object()
		object.last_accessed = timezone.now()
		object.save()
		return object

	
def Thanks(self,request):
	return HttpResponse('Thanks!!!')


class ContactView(FormView):
	template_name = 'users/contact.html'
	form_class = ContactForm
	success_url = '/thanks/'
	
	def form_valid(self, form):
		form.send_email()
		return super(ContactView,self).form_valid(form)


class AuthorCreate(CreateView):
	model = Author
	template_name = 'users/author_add.html'
	fields = ['name']

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super(AuthorCreate, self).form_valid(form)


class AuthorUpdate(UpdateView):
	model = Author
	fields = ['name']


class AuthorDelete(DeleteView):
	model = Author
	success_url = reverse_lazy('author-list')
