from django.contrib import admin

# Register your models here.

from django.contrib import admin
from payment.models import Price, Product


admin.site.register(Product)
admin.site.register(Price)