from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.logIn, name="login"),
    path('signup/', views.signUp, name="signup"),           
    path('shop/', views.shop, name="shop"),                 
    path('news/', views.New, name="whatsnew"),              
    path('update_item/', views.updateItem, name="update_item"),
    path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),
    path('submit-order/', views.submit_order, name='submit_order'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
]
