from django.contrib import admin
from .models import User, Product, Purchase, Return

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Purchase)
admin.site.register(Return)
