from django.contrib import admin
from .models import Listing, Booking, Review


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'country', 'price_per_night', 'host', 'is_available']
    list_filter = ['property_type', 'is_available', 'country', 'city']
    search_fields = ['title', 'description', 'address', 'city']
    list_editable = ['is_available']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'listing', 'guest', 'check_in_date', 'check_out_date', 'status', 'total_price']
    list_filter = ['status', 'check_in_date', 'check_out_date']
    search_fields = ['listing__title', 'guest__username']
    readonly_fields = ['total_price', 'created_at', 'updated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['listing', 'reviewer', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['listing__title', 'reviewer__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
