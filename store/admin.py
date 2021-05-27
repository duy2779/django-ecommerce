from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Menu)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Banner)
admin.site.register(Post)
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(Topic)
admin.site.register(Order_detail)