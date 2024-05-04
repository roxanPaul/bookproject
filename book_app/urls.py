from django.urls import path
from. import views
urlpatterns = [
    path("create/",views.create_book, name='create'),
    path("author/",views.Create_Author,name='author'),
    path('',views.listbook,name='booklist'),
    path('detailview/<int:book_id>/',views.detailsView , name="details"),
    path('updateview/<int:book_id>/',views.updateBook, name="update"),
    path('deleteview/<int:book_id>/',views.deletebook, name="delete"),
    path('search/',views.Search_Book,name='search'),
    path('index',views.index),
]
