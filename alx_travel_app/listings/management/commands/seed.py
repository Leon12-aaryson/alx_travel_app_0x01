from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
import random
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample listings, bookings, and reviews data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of users to create (default: 5)'
        )
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)'
        )
        parser.add_argument(
            '--bookings',
            type=int,
            default=30,
            help='Number of bookings to create (default: 30)'
        )
        parser.add_argument(
            '--reviews',
            type=int,
            default=50,
            help='Number of reviews to create (default: 50)'
        )

    def handle(self, *args, **options):
        self.stdout.write('Starting database seeding...')
        
        # Create users
        users = self.create_users(options['users'])
        
        # Create listings
        listings = self.create_listings(options['listings'], users)
        
        # Create bookings
        bookings = self.create_bookings(options['bookings'], listings, users)
        
        # Create reviews
        reviews = self.create_reviews(options['reviews'], listings, users)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with:\n'
                f'- {len(users)} users\n'
                f'- {len(listings)} listings\n'
                f'- {len(bookings)} bookings\n'
                f'- {len(reviews)} reviews'
            )
        )

    def create_users(self, count):
        """Create sample users"""
        users = []
        for i in range(count):
            username = f'user{i+1}'
            email = f'{username}@example.com'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'User{i+1}',
                    'last_name': f'LastName{i+1}',
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            
            users.append(user)
        
        return users

    def create_listings(self, count, users):
        """Create sample listings"""
        cities = [
            ('New York', 'NY', 'USA'),
            ('Los Angeles', 'CA', 'USA'),
            ('Chicago', 'IL', 'USA'),
            ('Miami', 'FL', 'USA'),
            ('San Francisco', 'CA', 'USA'),
            ('Paris', 'Île-de-France', 'France'),
            ('London', 'England', 'UK'),
            ('Tokyo', 'Tokyo', 'Japan'),
            ('Sydney', 'NSW', 'Australia'),
            ('Toronto', 'ON', 'Canada'),
        ]
        
        property_types = ['apartment', 'house', 'villa', 'cabin', 'condo']
        
        amenities_list = [
            ['WiFi', 'Kitchen', 'Free parking'],
            ['WiFi', 'Kitchen', 'Pool', 'Gym'],
            ['WiFi', 'Kitchen', 'Balcony', 'Air conditioning'],
            ['WiFi', 'Kitchen', 'Garden', 'BBQ'],
            ['WiFi', 'Kitchen', 'Hot tub', 'Mountain view'],
            ['WiFi', 'Kitchen', 'Beach access', 'Ocean view'],
            ['WiFi', 'Kitchen', 'Fireplace', 'Ski storage'],
            ['WiFi', 'Kitchen', 'Workspace', 'Coffee maker'],
        ]
        
        listings = []
        for i in range(count):
            city, state, country = random.choice(cities)
            property_type = random.choice(property_types)
            host = random.choice(users)
            
            listing = Listing.objects.create(
                title=f'Beautiful {property_type.title()} in {city}',
                description=f'Stunning {property_type} located in the heart of {city}. '
                           f'Perfect for your next vacation with all the amenities you need.',
                address=f'{random.randint(100, 9999)} {random.choice(["Main St", "Oak Ave", "Pine Rd", "Elm St"])}',
                city=city,
                state=state,
                zipcode=f'{random.randint(10000, 99999)}',
                country=country,
                price_per_night=random.randint(50, 500),
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 4),
                max_guests=random.randint(2, 12),
                property_type=property_type,
                amenities=random.choice(amenities_list),
                images=[
                    f'https://example.com/images/{property_type}_{i+1}_1.jpg',
                    f'https://example.com/images/{property_type}_{i+1}_2.jpg',
                ],
                host=host,
                is_available=random.choice([True, True, True, False]),  # 75% available
            )
            
            listings.append(listing)
            self.stdout.write(f'Created listing: {listing.title}')
        
        return listings

    def create_bookings(self, count, listings, users):
        """Create sample bookings"""
        bookings = []
        for i in range(count):
            listing = random.choice(listings)
            guest = random.choice(users)
            
            # Generate random dates
            start_date = date.today() + timedelta(days=random.randint(1, 365))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            # Skip if guest is the host
            if guest == listing.host:
                continue
            
            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in_date=start_date,
                check_out_date=end_date,
                num_guests=random.randint(1, listing.max_guests),
                status=random.choice(['pending', 'confirmed', 'completed', 'cancelled']),
                special_requests=random.choice([
                    '', 'Early check-in if possible', 'Late check-out requested',
                    'Extra towels needed', 'Quiet room preferred'
                ])
            )
            
            bookings.append(booking)
            self.stdout.write(f'Created booking: {booking}')
        
        return bookings

    def create_reviews(self, count, listings, users):
        """Create sample reviews"""
        reviews = []
        for i in range(count):
            listing = random.choice(listings)
            reviewer = random.choice(users)
            
            # Skip if reviewer is the host
            if reviewer == listing.host:
                continue
            
            # Check if review already exists
            if Review.objects.filter(listing=listing, reviewer=reviewer).exists():
                continue
            
            review = Review.objects.create(
                listing=listing,
                reviewer=reviewer,
                rating=random.randint(1, 5),
                comment=random.choice([
                    'Great place to stay! Highly recommended.',
                    'Clean and comfortable. Perfect location.',
                    'Amazing views and excellent amenities.',
                    'Good value for money. Would stay again.',
                    'Nice property but could use some updates.',
                    'Fantastic experience! The host was very helpful.',
                    'Beautiful property with everything we needed.',
                    'Peaceful location with great amenities.',
                    'Excellent communication with the host.',
                    'Wonderful stay, exceeded our expectations.'
                ])
            )
            
            reviews.append(review)
            self.stdout.write(f'Created review: {review}')
        
        return reviews 