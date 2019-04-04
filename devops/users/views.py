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
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView 
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Publisher,Book,Author


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


class PublisherBookList(ListView):
	template_name = 'users/publisher_book_list.html'
	context_object_name = 'publisher_book_list'
	
	def get_queryset(self):
		self.publisher = get_object_or_404(Publisher,name = self.args[0])
		return Book.objects.filter(publisher=self.publisher)

	def get_context_data(self, **kwargs):
		context = super(PublisherBookList, self).get_context_data(**kwargs)
		context['publisher'] = self.publisher
		return context

class AcmeBookList(ListView):
	context_object_name = 'book_list'
	queryset = Book.objects.filter(publisher__name='ACME Publishing')
	template_name = 'books/acme_list.html'


class AuthorDetailView(DetailView):
	queryset = Author.objects.all()
	
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
