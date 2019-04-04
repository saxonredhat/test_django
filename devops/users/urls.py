from django.urls import path

from . import views

app_name='users'

urlpatterns = [
	path('login/', views.UserLoginView.as_view(),name='user_login'),
	path('protected/', views.ProtectedPageView.as_view(),name='protected'),
	path('needlogin/', views.NeedLoginView.as_view(),name='needlogin'),
	path('publishers/', views.PublisherList.as_view(),name='publisher_list'),
	path('books/([\w-]+)/', views.PublisherBookList.as_view(),name='publisher_book_list'),
	path('authors/<int:pk>/', views.AuthorDetailView.as_view(),name='author_detail'),
	path('thanks/', views.Thanks,name='thanks'),
	path('author/add/',views.AuthorCreate.as_view(),name='author-add'),
	path('author/<int:pk>/',views.AuthorUpdate.as_view(),name='author-update'),
	path('author/<int:pk>/delete/',views.AuthorDelete.as_view(),name='author-delete'),
]
