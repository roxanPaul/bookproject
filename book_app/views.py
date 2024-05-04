from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render,redirect
from.models import Book,Author
from .forms import BookForm, AuthorForm
from django.db import transaction


from django.contrib import messages

def Create_Author(request):
    if request.method=='POST':
        form= AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return  redirect('create')
    else:
        form=AuthorForm()

    return render(request,'authors/author.html',{'form':form})
def create_book(request):
    form = BookForm()
    books = Book.objects.all()
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)

        # Inside your view function
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, 'Book created successfully.')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
        return redirect('/')



    else:
        form = BookForm()

    return render(request, 'authors/create.html', {'form': form, 'books': books})
def listbook(request):
    books=Book.objects.all()
    paginator=Paginator(books,4)
    page_no=request.GET.get('page')
    try:
        page=paginator.get_page(page_no)
    except EmptyPage:
        page=paginator.page(page_no.num_pages)

    return render(request,'authors/booklist.html',{'books':books,'page':page})



def Search_Book(request):
    query = None
    books = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books = []

    context = {'books': books, 'query': query}
    return render(request, 'authors/search.html', context)

def deletebook(request,book_id):

    book=Book.objects.get(id=book_id)
    if request.method=="POST":
        book.delete()
        return redirect('/')
    return render(request,'authors/deleteview.html')

def detailsView(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request,'authors/detailview.html',{'book':book})
def updateBook(request,book_id):
    form=None
    book=Book.objects.get(id=book_id)

    if request.method == 'POST':
        form=BookForm(request.POST,request.FILES,instance=book)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form=BookForm(instance=book)
    return render(request,'authors/updateview.html',{'form':form})

def index(request):
    return render(request,'base.html')