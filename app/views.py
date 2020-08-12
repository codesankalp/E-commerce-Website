from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm,ContactForm,ReviewForm,CheckoutForm,CareerForm
from django.core.mail import send_mail,mail_admins
from uv.settings import EMAIL_HOST_USER
from .models import Review,Contact,Cart,Product,Checkout
import random


def handler404(request, exception):
    return render(request,'404.html',{
        "title" : "Page Not Found",
        "error" : "404",
    })


def handler500(request):
    return render(request,'404.html',{
        "title": "Server Error",
        "error" : "500",
    })


def index(request):
    try:
        product = Product.objects.get(pk=1) 
    except:
        product = Product()
        product.save()
    
    return render(request, 'index.html',{
        "title": "UV PURE",
        "product": product,
    })


def about(request):
    return render(request, 'about.html',{
        "title": "About UV Pure"
    })


def contact(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        author = form.cleaned_data['author']
        phone = form.cleaned_data['phone']
        info = form.save()
        message = '''
        query_email: {}
        query_subject: {}
        query_message: {}
        query_author: {}
        query_phone: {}
        '''.format(email,subject,message,author,phone)
        subject_for_user = 'We Will Contact You Soon !!'
        message_for_user = "\nYour information shared with us : \n" + message + "\nWe will contact you soon!!"
        recepient = str(email)
        send_mail(subject_for_user,message_for_user,EMAIL_HOST_USER,[recepient], fail_silently = False)
        mail_admins(subject='CONTACT {}'.format(author), message=message, fail_silently=False)
        return render(request, 'contact.html',{
        "form":form,
        "warning":"We Will Contact You Soon !!!",
        "title": "Contact"  
    })
    return render(request, 'contact.html',{
        "form":form,
        "title": "Contact"  
    })


def faq(request):
    return render(request, 'faq.html',{
        "title": "FAQs"
    })


def product(request):
    review_form = ReviewForm(request.POST or None)
    try:
        product = Product.objects.get(pk=1) 
    except:
        product = Product()
        product.save()
    try:
        reviews = (Review.objects.all())[:3]
    except:
        reviews = []
    if review_form.is_valid():
        try:
            review = Review.objects.get(user=request.user)
        except:
            review = review_form.save(commit=False)
        review.user = request.user
        review.comment = review_form.cleaned_data['comment']
        review.rating = review_form.cleaned_data['rating']
        review.save()
        return render(request, 'product_single.html', {
        "warning":"Review, submitted we will process it soon.!!",
        "title": 'Buy Product',
        "reviews": reviews,
        "form":review_form,
        "product":product
        })
        return redirect('app:product')

    return render(request, 'product_single.html', {
        "title": 'Buy Product',
        "reviews": reviews,
        "form":review_form,
        "product":product
    })


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("app:home")
            else:
                return render(request, 'account.html', {'warning': 'Your account has been disabled'})
        else:
            return render(request, 'account.html', {'warning': 'Invalid login'})
    return render(request, 'account.html', {
        "title" : "LOGIN / REGISTER" 
    })


def user_logout(request):
    logout(request)
    return redirect("app:home")


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        try:
            obj = User.objects.get(email=email)
            return render(request, 'account.html', context={
                "warning":" Email - {} Already Taken !!".format(email),
                "title" : "LOGIN / REGISTER",
                })
        except:
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("app:home")
    context = {
        "form": form,
        "title" : "LOGIN / REGISTER",
    }
    return render(request, 'account.html', context)


def all_review(request):
    reviews = Review.objects.all()
    return render(request, 'review.html', {
        "title":"ALL REVIEWS",
        "reviews":reviews,
    })


@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except:
        cart = Cart(user=request.user,item=Product.objects.get(pk=1))
        cart.save()
    
    if request.method == 'POST':
        cart.count = int(request.POST.get("count"))
        cart.save()
    total = cart.get_total()
    return render(request,'cart.html',{
        "cart":cart,
        "title":"CART",
        "total":total
    })


@login_required
def checkout(request):
    form = CheckoutForm(request.POST or None)
    try:
        cart = Cart.objects.get(user=request.user)
    except:
        cart = Cart(user=request.user,item=Product.objects.get(pk=1))
        cart.save()

    total = cart.get_total()
    if form.is_valid():
        check = form.save(commit=False)
        check.user = request.user
        check.cart = cart
        check.save()

    return render(request, 'checkout.html',{
        "title":"CHECKOUT",
        "form":form,
        "cart":cart,
        "total":total,
    })


def career(request):
    form = CareerForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        form.save()
        recepient = str(data['email'])
        subject_for_user = 'We will contact you soon! - UV PURE Pvt. Ltd.'
        message_for_user = 'We take your career seriously. Our Client will reach to you soon !'
        send_mail(subject_for_user,message_for_user,EMAIL_HOST_USER,[recepient], fail_silently = False)
        mail_admins(subject='CAREER {}'.format(data['name']), message=str(data), fail_silently=False)
        return render(request, 'career.html',{
        "form":form,
        "warning":"We Will Contact You Soon !!!",
        "title": "CAREER WITH US"  
    })
    return render(request,'career.html',{
        "title":"CAREER WITH US",
        "form":form
    })