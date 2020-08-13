from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserForm,ContactForm,ReviewForm,CheckoutForm,CareerForm
from django.core.mail import send_mail,mail_admins
from uv.settings import EMAIL_HOST_USER
from .models import Review,Contact,Cart,Product,Checkout,Payment
from django.views.generic import View
from django.contrib import messages
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

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
    '''
    :Checkout Page for saving users address:
    '''
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
        return redirect('app:payment',check.pk)

    return render(request, 'checkout.html',{
        "title":"CHECKOUT",
        "form":form,
        "cart":cart,
        "total":total,
    })


def career(request):
    '''
    :For Career page form:
    '''
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


class PaymentView(View):
    '''
    :For payment page:
    '''
    def get(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=self.request.user)
        except:
            cart = Cart(user=self.request.user,item=Product.objects.get(pk=1))
            cart.save()

        total = int(cart.get_total())
        key = self.kwargs['key'] #for checkout
        if Checkout.objects.get(pk=self.kwargs['key']).user != self.request.user:
            return render(self.request,'404.html',{
                "title" : "Page Not Found",
                "error" : "404",
            })
        return render(self.request, "payment.html", {
            "title":"payment",
            "cart":cart,
            "total":total,
            "key": key,
        })

    def post(self, *args, **kwargs):
        try:
            cart = Cart.objects.get(user=self.request.user)
        except:
            cart = Cart(user=self.request.user,item=Product.objects.get(pk=1))
            cart.save()
        if Checkout.objects.get(pk=self.kwargs['key']).user != self.request.user:
            return render(self.request,'404.html',{
                "title" : "Page Not Found",
                "error" : "404",
            })
        checkout = Checkout.objects.get(pk=self.kwargs['key'])
        print(checkout)
        total = int(cart.get_total())
        
        try:
            token = self.request.POST.get('stripeToken')
            customer = stripe.Customer.create(
                email = self.request.user.email,
                name = self.request.user.first_name,
                source=token,
                description = "buying UV PURE product."
            )
            charge = stripe.Charge.create(
                customer = customer,
                amount=total*100,
                currency="inr",
                # source=token,
                description="buying UV PURE product.",
            )

            # creating payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = total
            payment.save()

            # adding to checkout
            checkout.ordered = True
            checkout.payment = payment
            checkout.save()
            messages.success(self.request, "Your order was successful! Check your mail for order reciept.")
            return redirect("/")


        except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.warning(self.request, "Rate limit error")
            return redirect("/")

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            print(e)
            messages.warning(self.request, "Invalid parameters")
            return redirect("/")

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.warning(self.request, "Not authenticated")
            return redirect("/")

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.warning(self.request, "Network error")
            return redirect("/")

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.warning(
                self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("app:payment")