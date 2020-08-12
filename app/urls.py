from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/',views.product, name='product'),
    path('faq/',views.faq, name='faq'),
    path('login/',views.user_login, name='account'),
    path('logout/',views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('reviews/',views.all_review, name='reviews'),
    path('cart/',views.cart,name='cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('career/',views.career,name='career'),
]
