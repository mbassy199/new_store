from django.contrib import admin
from store.models import (
    Cart, Product, Category, Gallery, Specification, Size, Color, 
    CartOrder, CartOrderItem, Wishlist, Review, ProductFaq, Coupon, Notification
)
from shortuuid.django_fields import ShortUUIDField


# Inline classes for related models to display in the admin for Product and CartOrder models
class GalleryInline(admin.TabularInline):
    model = Gallery


class SpecificationInline(admin.TabularInline):
    model = Specification


class SizeInline(admin.TabularInline):
    model = Size


class ColorInline(admin.TabularInline):
    model = Color


# ProductAdmin customization
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'featured', 'status', 'vendor']  # Added status and vendor
    list_editable = ['featured']  # Allow 'featured' to be editable directly in the list
    list_filter = ['date', 'status', 'category', 'vendor']  # Filters by date, status, category, vendor
    search_fields = ['title', 'description', 'pid']  # Search by title, description, and product ID
    inlines = [GalleryInline, SpecificationInline, SizeInline, ColorInline]  # Inline for related models


# CartOrderItemInline for displaying CartOrderItems within CartOrderAdmin
class CartOrderItemInline(admin.TabularInline):
    model = CartOrderItem


# CartOrderAdmin customization
class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['oid', 'buyer', 'order_status', 'payment_status', 'total']  # Relevant fields
    list_filter = ['order_status', 'payment_status']  # Filters by order status and payment status
    search_fields = ['oid', 'full_name', 'email']  # Search by order ID, buyer's name and email
    inlines = [CartOrderItemInline]  # Inline for CartOrderItems


# CartOrderItemAdmin customization
class CartOrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'qty', 'price', 'total']  # Relevant fields to display
    search_fields = ['order__oid', 'product__title']  # Search by order ID and product title


# CartAdmin customization
class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'product', 'user', 'qty', 'total']  # Display relevant fields for the cart
    search_fields = ['cart_id', 'product__title', 'user__email']  # Search by cart ID, product title, and user email


# WishlistAdmin customization
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']  # Display user, product, and date
    search_fields = ['user__email', 'product__title']  # Search by user email and product title


# ReviewAdmin customization
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'date', 'active']  # Display product, user, rating, and status
    list_filter = ['rating', 'active']  # Filters by rating and active status
    search_fields = ['product__title', 'user__email']  # Search by product title and user email


# ProductFaqAdmin customization
class ProductFaqAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'question', 'active', 'date']  # Display product, user, question, etc.
    list_filter = ['active']  # Filter by active status
    search_fields = ['product__title', 'user__email', 'question']  # Search by product, user email, and question


# CouponAdmin customization
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'active', 'vendor', 'date']  # Display relevant fields for Coupon
    list_filter = ['active']  # Filter by active status
    search_fields = ['code', 'vendor__name']  # Search by coupon code and vendor name


# NotificationAdmin customization
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'vendor', 'order', 'seen', 'date']  # Display relevant fields for Notification
    list_filter = ['seen']  # Filter by seen status
    search_fields = ['user__email', 'order__oid']  # Search by user email and order ID


# Registering models with their custom admin configurations
admin.site.register(Category)  # Register Category model
admin.site.register(Product, ProductAdmin)  # Register Product with ProductAdmin customization
admin.site.register(Cart, CartAdmin)  # Register Cart with CartAdmin customization
admin.site.register(CartOrder, CartOrderAdmin)  # Register CartOrder with CartOrderAdmin customization
admin.site.register(CartOrderItem, CartOrderItemAdmin)  # Register CartOrderItem with CartOrderItemAdmin customization
admin.site.register(Wishlist, WishlistAdmin)  # Register Wishlist with WishlistAdmin customization
admin.site.register(Review, ReviewAdmin)  # Register Review with ReviewAdmin customization
admin.site.register(ProductFaq, ProductFaqAdmin)  # Register ProductFaq with ProductFaqAdmin customization
admin.site.register(Coupon, CouponAdmin)  # Register Coupon with CouponAdmin customization
admin.site.register(Notification, NotificationAdmin)  # Register Notification with NotificationAdmin customization
