from django.contrib import admin
from .models import Contact,Review,Cart,Checkout,Product,Career,Payment

class DateAdmin(admin.ModelAdmin):
    readonly_fields = ('time',)

admin.site.register(Contact,DateAdmin)
admin.site.register(Review,DateAdmin)
admin.site.register(Cart,DateAdmin)
admin.site.register(Checkout,DateAdmin)
admin.site.register(Product)
admin.site.register(Career,DateAdmin)
admin.site.register(Payment,DateAdmin)