from django.urls import path
from. import views
urlpatterns = [
    path("user/",views.list_book,name='list'),
    path("search/",views.search_book,name='search'),
    path("detail/<int:book_id>/",views.detail_view,name='detail'),
    path('addcart/<int:book_id>/',views.AddCart,name='addcart'),
    path('viewcart/',views.ViewCart,name='viewcart'),
    path('increase/<int:book_id>/',views.increase_quantity,name='increase_quantity'),
    path('decrease/<int:book_id>/',views.decrease_quantity,name='decrease_quantity'),
    path('remove/<int:book_id>/',views.remove_from_cart,name='remove_cart'),
    path('create-checkout-session/',views.create_checkout_session,name='create-checkout-session'),
    path('success/',views.success, name='success'),
    path('cancel/',views.cancel,name='cancel'),

]