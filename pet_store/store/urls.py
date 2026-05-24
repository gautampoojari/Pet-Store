from django.urls import path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path('product/<int:id>',product,name='product'),
    path('Login/',login_user, name="Login"),
    path('Signup/',signup_user, name="Signup"),
    path('Logout/', logout_user , name= "Logout"),
    path('category/<int:id>', category, name="category"),
    path('about/', about, name="about"),
    path('cart/', display_cart, name="cart"),
    path('add_to_cart/<int:id>', add_to_cart, name="add_to_cart"),
    path('delete_cart/<int:id>', delete_cart, name="delete_cart"),
    path('pay/', homepage, name="pay"),
    path('cart/success/', success, name="success"),
]