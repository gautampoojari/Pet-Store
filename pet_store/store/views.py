from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
import razorpay
from django.conf import settings
from .models import *
from django.contrib.auth.decorators import login_required
# from django.contrib.messages import message

# Create your views here.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
 
 
def homepage(request):
    currency = 'INR'
    amount = 20000  # Rs. 200
 
    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    callback_url = 'success/'
 
    # we need to pass these details to frontend.
    pay_detail = {}
    pay_detail['razorpay_order_id'] = razorpay_order_id
    pay_detail['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    pay_detail['razorpay_amount'] = amount
    pay_detail['currency'] = currency
    pay_detail['callback_url'] = callback_url
 
    return render(request, 'pay.html')
@login_required(login_url='Login')


def home(request):
    # get all the rows from Product table in db
    products = Product.objects.all()
    categories=Category.objects.all()
    return render(request, 'index.html',{'products':products, 'categories':categories}) 

def product(request,id):
    categories = Category.objects.all()
    product=Product.objects.get(id = id)
    # print(product.category)
    related_products= Product.objects.filter(category = product.category).exclude(id = id)[:4] 
    return render(request, 'product.html',{'product':product, 'related_products': related_products, 'categories': categories})

def category(request, id):
    if id=="all":
        categories=Category.objects.all()
        for items in categories:
            product_count = Product.objects.filter(category = items).count()
            items.product_count = product_count
        products = Product.objects.all()
        return render(request, 'category.html', {'categories': categories, 'products': products})
    categories = Category.objects.all()
    products = Product.objects.filter(category=id)
    return render(request, 'category.html', {'categories': categories, 'products': products})
    


def login_user(request):
    if request.POST:
        username=request.POST.get('username')
        password = request.POST.get('password')
    
        log_User=authenticate(username=username,password=password)
        
        user=User.objects.filter(username=username).exists()
        if not user:
            return render(request,'Login.html',{'msg':'User does not exists'})
    
        if log_User is not  None:
            login(request,log_User)
            return redirect('home')
        else:
            return render(request,'Login.html',{'msg':'User or Password is Incorrect'})
    categories=Category.objects.all()   
    return render(request, 'Login.html', {'categories': categories})

def signup_user(request):
    if request.POST:
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        email=request.POST['email']
        password=request.POST['password']
        
        user=User.objects.filter(username=email).exists()
        if user:
            return render(request,'Signup.html',{'msg':'User already exists'})
        
        data=User.objects.create_user(first_name=firstname, last_name=lastname, username=email,email=email, password=password)
        data.save()
        
        return redirect('Login')
    
    categories=Category.objects.all()
    return render(request, 'Signup.html', {'categories': categories})

def logout_user(request):
    logout(request)
    return  redirect('Login')

def about(request):
    categories=Category.objects.all()
    return render(request,"about.html", {'categories': categories})

def display_cart(request):
    if request.user.is_authenticated:
        cart_product = Cart.objects.filter(user=request.user)
        sub_total = sum([product.product.price * product.quantity for product in cart_product])
        discounted_price = float(sub_total)*0.15
        final_price = float(sub_total)-discounted_price

        if sub_total > 0:
            currency = 'INR'
            amount = final_price*100  # Rs. 200
 
    # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
 
    # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'success/'
 
    # we need to pass these details to frontend.
            pay_detail = {}
            pay_detail['razorpay_order_id'] = razorpay_order_id
            pay_detail['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            pay_detail['razorpay_amount'] = amount
            pay_detail['currency'] = currency
            pay_detail['callback_url'] = callback_url
            categories=Category.objects.all()
            return render(request,"cart.html", {'categories':categories, 'cart_product':cart_product,'final_price':final_price,'sub_total':sub_total, 'discounted_price':discounted_price, 'pay_detail':pay_detail})
    
        categories=Category.objects.all()
        return render(request,"cart.html", {'categories':categories, 'cart_product':cart_product,'final_price':final_price,'sub_total':sub_total, 'discounted_price':discounted_price})
    return redirect('Login')

def add_to_cart(request, id):
    # print(request.user.is_authenticated)
    if request.user.is_authenticated:
        if Cart.objects.filter(product = id, user=request.user).exists():
            cart_product = Cart.objects.get(product=id, user = request.user)
            print(cart_product)
            cart_product.quantity += 1
            cart_product.save()
            return redirect('cart')
        user = request.user
        product = Product.objects.get(id = id)
        new_cart = Cart.objects.create(user = user, product = product)
        new_cart.save()
        return redirect('cart')
    return redirect('Login')

def delete_cart(request, id):
    cart = Cart.objects.get(id=id)
    cart.delete()
    return redirect('cart')


def success(request):
    return render(request, 'success.html')
