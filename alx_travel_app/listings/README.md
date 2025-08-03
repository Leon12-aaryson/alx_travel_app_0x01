# Listings App

The `listings` app is the core Django application for the ALX Travel App, handling property listings, bookings, and reviews.

## App Overview

This app provides the main functionality for:
- **Property Listings**: Create and manage travel accommodations
- **Booking System**: Handle property reservations
- **Review System**: User ratings and feedback
- **API Endpoints**: REST API for all models
- **Data Seeding**: Management commands for sample data

## App Structure

```text
listings/
├── __init__.py              # Python package initialization
├── admin.py                 # Django admin interface configuration
├── apps.py                  # App configuration
├── models.py                # Database models
├── serializers.py           # API serializers
├── views.py                 # View logic (to be implemented)
├── tests.py                 # Test cases
├── migrations/              # Database migrations
├── management/
│   └── commands/
│       └── seed.py          # Database seeding command
└── README.md               # This documentation file
```

## Models

### Listing Model

**Purpose**: Represents travel property listings

**Key Fields:**

- `title`: Property title
- `description`: Detailed description
- `address`, `city`, `state`, `zipcode`, `country`: Location
- `price_per_night`: Nightly rate
- `bedrooms`, `bathrooms`, `max_guests`: Capacity
- `property_type`: Type (apartment, house, villa, cabin, condo)
- `amenities`: JSON field for property features
- `images`: JSON field for property photos
- `host`: Foreign key to User model
- `is_available`: Availability status

**Relationships:**

- One-to-Many with User (host)
- One-to-Many with Booking
- One-to-Many with Review

### Booking Model

**Purpose**: Manages property reservations

**Key Fields:**

- `listing`: Foreign key to Listing
- `guest`: Foreign key to User
- `check_in_date`, `check_out_date`: Booking dates
- `num_guests`: Number of guests
- `total_price`: Calculated total (auto-calculated)
- `status`: Booking status (pending, confirmed, cancelled, completed)
- `special_requests`: Optional special requests

**Features:**

- Automatic total price calculation
- Date validation
- Guest capacity validation
- Status management

### Review Model

**Purpose**: User ratings and feedback system

**Key Fields:**

- `listing`: Foreign key to Listing
- `reviewer`: Foreign key to User
- `rating`: 1-5 star rating
- `comment`: Review text
- `created_at`, `updated_at`: Timestamps

**Constraints:**

- Unique constraint: one review per user per listing
- Rating validation: 1-5 stars

## API Serializers

### UserSerializer

Serializes User model data for API responses.

### ListingSerializer

Comprehensive serializer for Listing model:

- Includes nested review data
- Calculates average rating
- Provides review count
- Handles host information

### BookingSerializer

Booking serialization with validation:

- Date validation (check-out after check-in)
- Guest capacity validation
- Listing availability check
- Automatic guest assignment

### ReviewSerializer

Review serialization with user data integration.

## Admin Interface

### ListingAdmin

- **List Display**: title, city, country, price, host, availability
- **Filters**: property type, availability, country, city
- **Search**: title, description, address, city
- **Editable**: availability status

### BookingAdmin

- **List Display**: ID, listing, guest, dates, status, price
- **Filters**: status, check-in/out dates
- **Search**: listing title, guest username
- **Read-only**: total price, timestamps

### ReviewAdmin

- **List Display**: listing, reviewer, rating, created date
- **Filters**: rating, created date
- **Search**: listing title, reviewer username, comment
- **Read-only**: timestamps

## Management Commands

### seed.py

Database seeding command for sample data generation.

**Usage:**

```bash
# Default values
python manage.py seed

# Custom values
python manage.py seed --users 10 --listings 50 --bookings 100 --reviews 200
```

**Features:**

- Creates sample users with credentials
- Generates realistic property listings
- Creates bookings with various statuses
- Adds reviews with ratings and comments
- Handles relationships properly

**Sample Data:**

- **Users**: user1-user5 (password: password123)
- **Cities**: Worldwide locations (NY, LA, Paris, London, Tokyo, etc.)
- **Property Types**: apartment, house, villa, cabin, condo
- **Amenities**: Various combinations (WiFi, Kitchen, Pool, etc.)

## Database Migrations

### Initial Migration (0001_initial.py)

Creates all three models with proper relationships and constraints:

- Listing model with all fields
- Booking model with foreign keys and validation
- Review model with unique constraints

## API Endpoints (To be implemented)

### Planned Endpoints

- `GET /api/listings/` - List all listings
- `POST /api/listings/` - Create new listing
- `GET /api/listings/{id}/` - Get specific listing
- `PUT /api/listings/{id}/` - Update listing
- `DELETE /api/listings/{id}/` - Delete listing

- `GET /api/bookings/` - List all bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/{id}/` - Get specific booking
- `PUT /api/bookings/{id}/` - Update booking

- `GET /api/reviews/` - List all reviews
- `POST /api/reviews/` - Create new review
- `GET /api/reviews/{id}/` - Get specific review

## Testing

### Test Structure

- `tests.py`: Basic test file (to be expanded)
- Model validation tests
- Serializer validation tests
- API endpoint tests
- Management command tests

### Running Tests

```bash
python manage.py test listings
```

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guide
- Use descriptive variable names
- Add docstrings to classes and methods
- Keep methods focused and single-purpose

### Model Best Practices

- Use appropriate field types
- Add proper validation
- Set up meaningful relationships
- Include helpful Meta options

### Serializer Best Practices

- Validate data properly
- Handle nested relationships
- Provide calculated fields
- Use appropriate read-only fields

## Future Enhancements

### Planned Features

1. **Image Upload**: File upload for property images
2. **Search & Filtering**: Advanced search capabilities
3. **Pagination**: API pagination for large datasets
4. **Caching**: Redis caching for performance
5. **Notifications**: Email notifications for bookings
6. **Payment Integration**: Payment processing for bookings

### Performance Optimizations

1. **Database Indexing**: Add indexes for frequently queried fields
2. **Query Optimization**: Optimize database queries
3. **Caching**: Implement caching strategies
4. **API Rate Limiting**: Add rate limiting for API endpoints

## Dependencies

### Internal Dependencies

- Django User model (authentication)
- Django admin interface
- Django REST Framework

### External Dependencies

- None currently (all Django built-in or DRF)

## Contributing

1. Follow Django best practices
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages
5. Test thoroughly before submitting

## License

This app is part of the ALX Software Engineering curriculum.

## Author

Created as part of ALX Software Engineering program. 