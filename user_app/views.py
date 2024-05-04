from audioop import reverse

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
import stripe
from .models import Cart, CartItem
from book_app.models import Book, Author
from django.http import HttpResponseServerError

# Create your views here.

def list_book(request):
    books=Book.objects.all()
    paginator = Paginator(books, 4)
    page_no = request.GET.get('page')
    try:
        page = paginator.get_page(page_no)
    except EmptyPage:
        page = paginator.page(page_no.num_pages)

    return render(request, 'user/list.html', {'books': books, 'page': page})


def detail_view(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request,'user/details.html',{'book':book})
def search_book(request):
    query=None
    books=None

    if 'q' in request.GET:

        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query)| Q(author__name__icontains=query))
    else:
        books=[]
    context={'books':books,'query':query}

    return render(request,'user/search_book.html',context)


def AddCart(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.user.is_authenticated:
        if book.quantity > 0:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

            if not item_created:
                cart_item.quantity += 1
                cart_item.save()

            return redirect('viewcart')
        else:
            messages.error(request, "This book is out of stock.")
    else:
        messages.error(request, "Please login to add items to your cart.")

    return redirect('login')
def ViewCart(request):
    try:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.cartitem_set.all()
            cart_item = CartItem.objects.all()
            total_price = sum(item.book.price * item.quantity for item in cart_items)
            total_items = cart_items.count()
            context = {
                'cart_items': cart_items,
                'cart_item': cart_item,
                'total_price': total_price,
                'total_items': total_items
            }

            return render(request, 'user/cart.html', context)
        else:
            messages.error(request, 'Please login first')

    except Cart.DoesNotExist:
        messages.error(request, 'Error retrieving the cart')

    # Default context in case of an exception or user not authenticated
    context = {
        'cart_items': [],
        'cart_item': [],
        'total_price': 0,
        'total_items': 0
    }

    return render(request, 'user/cart.html', context)
def increase_quantity(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    if cart_item.quantity < cart_item.book.quantity:

        cart_item.quantity +=1
        cart_item.save()
    return redirect('addtocart')

def decrease_quantity(request,item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('viewcart')

def remove_from_cart(request,item_id):
    try:

        cart_item=CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoseNotExist:
        pass
    return redirect('viewcart')


def create_checkout_session(request):
    cart_items=CartItem.objects.all()
    if cart_items:
        stripe.api_key=settings.STRIPE_SECRET_KEY

        if request.method=='POST':
            line_items=[]
            for cart_item in cart_items:
                if cart_item.book:
                    line_item={
                        'price_data':{
                            'currency':'INR',
                            'unit_amount':int(cart_item.book.price * 100),
                            'product_data':
                                {
                                    'name':cart_item.book.title

                                },
                        },
                        'quantity':1
                    }
                    line_items.append(line_item)
            if line_items:
                checkout_session=stripe.checkout.Session.create(
                   payment_method_types=['card'],
                   line_items=line_items,
                   mode='payment',
                   success_url=request.build_absolute_uri(reverse('success')),
                   cancel_url=request.build_absolut_uri(reverse('cancel')),
                   )
                return redirect(checkout_session.url,code=303)

def success(request):
    cart_items=CartItem.obects.all()

    for cart_item in cart_items:
         product=cart_item.book
         if product.quantity >= cart_item.quantity:
             product.quantity -= cart_item.quantity
             product.save()

    cart_items.delete()
    return render(request,'user/success.html')

def cancel(request):
    return render(request,'user/cancel.html')