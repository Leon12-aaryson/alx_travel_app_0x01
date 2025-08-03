from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    reviewer = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'rating', 'comment', 'created_at']
        read_only_fields = ['reviewer', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'address', 'city', 'state', 
            'zipcode', 'country', 'price_per_night', 'bedrooms', 'bathrooms',
            'max_guests', 'property_type', 'amenities', 'images', 'host',
            'is_available', 'created_at', 'updated_at', 'reviews',
            'average_rating', 'review_count'
        ]
        read_only_fields = ['host', 'created_at', 'updated_at', 'average_rating', 'review_count']
    
    def get_average_rating(self, obj):
        """Calculate average rating for the listing"""
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    def get_review_count(self, obj):
        """Get the number of reviews for the listing"""
        return obj.reviews.count()


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    listing = ListingSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_id', 'guest', 'check_in_date', 
            'check_out_date', 'num_guests', 'total_price', 'status',
            'special_requests', 'created_at', 'updated_at'
        ]
        read_only_fields = ['guest', 'total_price', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate booking data"""
        # Check if check-out date is after check-in date
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        
        # Check if listing exists and is available
        try:
            listing = Listing.objects.get(id=data['listing_id'])
            if not listing.is_available:
                raise serializers.ValidationError("This listing is not available")
            
            # Check if number of guests doesn't exceed max capacity
            if data['num_guests'] > listing.max_guests:
                raise serializers.ValidationError(f"Maximum {listing.max_guests} guests allowed")
            
        except Listing.DoesNotExist:
            raise serializers.ValidationError("Listing not found")
        
        return data
    
    def create(self, validated_data):
        """Create booking with listing reference"""
        listing_id = validated_data.pop('listing_id')
        listing = Listing.objects.get(id=listing_id)
        validated_data['listing'] = listing
        validated_data['guest'] = self.context['request'].user
        return super().create(validated_data)


class ListingDetailSerializer(ListingSerializer):
    """Detailed serializer for Listing with more information"""
    bookings = BookingSerializer(many=True, read_only=True)
    
    class Meta(ListingSerializer.Meta):
        fields = ListingSerializer.Meta.fields + ['bookings'] 