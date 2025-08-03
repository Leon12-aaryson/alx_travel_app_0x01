from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import models
from .models import Listing, Booking, Review
from .serializers import (
    ListingSerializer, 
    BookingSerializer, 
    ReviewSerializer,
    UserSerializer,
    ListingDetailSerializer
)


class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Listing model providing CRUD operations.
    
    list: Get all listings
    create: Create a new listing
    retrieve: Get a specific listing
    update: Update a listing
    partial_update: Partially update a listing
    destroy: Delete a listing
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on action"""
        if self.action == 'retrieve':
            return ListingDetailSerializer
        return ListingSerializer
    
    def perform_create(self, serializer):
        """Set the host to the current user when creating a listing"""
        serializer.save(host=self.request.user)
    
    def perform_update(self, serializer):
        """Ensure only the host can update their listing"""
        if serializer.instance.host != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own listings")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure only the host can delete their listing"""
        if instance.host != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own listings")
        instance.delete()
    
    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific listing"""
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        """Add a review to a specific listing"""
        listing = self.get_object()
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            # Check if user has already reviewed this listing
            if Review.objects.filter(listing=listing, reviewer=request.user).exists():
                return Response(
                    {"error": "You have already reviewed this listing"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(listing=listing, reviewer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_listings(self, request):
        """Get all listings created by the current user"""
        listings = Listing.objects.filter(host=request.user)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Get all available listings"""
        listings = Listing.objects.filter(is_available=True)
        serializer = self.get_serializer(listings, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Booking model providing CRUD operations.
    
    list: Get all bookings
    create: Create a new booking
    retrieve: Get a specific booking
    update: Update a booking
    partial_update: Partially update a booking
    destroy: Delete a booking
    """
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return bookings based on user role"""
        user = self.request.user
        # Users can see their own bookings and bookings for their listings
        return Booking.objects.filter(
            models.Q(guest=user) | models.Q(listing__host=user)
        )
    
    def perform_create(self, serializer):
        """Set the guest to the current user when creating a booking"""
        serializer.save(guest=self.request.user)
    
    def perform_update(self, serializer):
        """Ensure only the guest or host can update the booking"""
        booking = serializer.instance
        user = self.request.user
        
        if booking.guest != user and booking.listing.host != user:
            raise permissions.PermissionDenied("You can only edit your own bookings")
        
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure only the guest or host can delete the booking"""
        user = self.request.user
        
        if instance.guest != user and instance.listing.host != user:
            raise permissions.PermissionDenied("You can only delete your own bookings")
        
        instance.delete()
    
    @action(detail=False, methods=['get'])
    def my_bookings(self, request):
        """Get all bookings made by the current user"""
        bookings = Booking.objects.filter(guest=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_hosted_bookings(self, request):
        """Get all bookings for listings owned by the current user"""
        bookings = Booking.objects.filter(listing__host=request.user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        user = request.user
        
        if booking.guest != user and booking.listing.host != user:
            raise permissions.PermissionDenied("You can only cancel your own bookings")
        
        if booking.status == 'cancelled':
            return Response(
                {"error": "Booking is already cancelled"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'cancelled'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking (host only)"""
        booking = self.get_object()
        
        if booking.listing.host != request.user:
            raise permissions.PermissionDenied("Only the host can confirm bookings")
        
        if booking.status != 'pending':
            return Response(
                {"error": "Only pending bookings can be confirmed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = 'confirmed'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review model providing CRUD operations.
    
    list: Get all reviews
    create: Create a new review
    retrieve: Get a specific review
    update: Update a review
    partial_update: Partially update a review
    destroy: Delete a review
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        """Set the reviewer to the current user when creating a review"""
        serializer.save(reviewer=self.request.user)
    
    def perform_update(self, serializer):
        """Ensure only the reviewer can update their review"""
        if serializer.instance.reviewer != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own reviews")
        serializer.save()
    
    def perform_destroy(self, instance):
        """Ensure only the reviewer can delete their review"""
        if instance.reviewer != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own reviews")
        instance.delete() 