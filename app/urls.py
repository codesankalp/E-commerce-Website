from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'app'

urlpatterns = [
    path('',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/',views.product, name='product'),
    path('login/',views.user_login, name='account'),
    path('logout/',views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('reviews/',views.all_review, name='reviews'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('career/',views.career,name='career'),
    path('payment/<int:key>/', login_required(views.PaymentView.as_view()), name='payment'),
]
