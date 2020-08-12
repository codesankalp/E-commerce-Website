from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField

User = get_user_model()

# Create your models here.
class Contact(models.Model):
    author = models.CharField(max_length=1000)
    email = models.EmailField()
    phone = models.CharField(max_length=12,blank=True)
    subject = models.CharField(max_length=1000)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-time']

    def __str__(self):
        return "Contact - {} - {}".format(self.author,self.email)


class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    rating = models.SmallIntegerField(default=5,blank=True)
    comment = models.TextField()
    author = models.CharField(max_length=1000)
    email = models.EmailField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return "{} - {}".format(self.author,self.email)


class Product(models.Model):
    name = models.CharField(max_length=1000, default='UV PURE',unique=True)
    price = models.IntegerField(default=4399)

    def __str__(self):
        return "{} - {}".format(self.name, self.price)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    time = models.DateTimeField(auto_now_add=True)

    def get_price(self):
        return self.item.price

    def get_total(self):
        return (self.item.price)*(self.count)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.user.username


class Checkout(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(default="IN",multiple=False)
    name = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    address = models.TextField()
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip_code = models.IntegerField()
    phone = models.CharField(max_length=12)
    notes = models.TextField(blank=True,null=True)
    time = models.DateTimeField(auto_now_add=True)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-time']


class Career(models.Model):
    name = models.CharField(max_length=1000) 
    father_name = models.CharField(max_length=1000)
    dob = models.DateField()
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    address = models.TextField()
    profession_role = models.CharField(max_length=1000)
    experience = models.CharField(max_length=1000)
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return self.name