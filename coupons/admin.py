from django.contrib import admin
from .models import ClaimedCoupon, Coupon
# Register your models here.

admin.site.register(Coupon)
admin.site.register(ClaimedCoupon)
