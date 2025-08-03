# ALX Travel App

A Django-based travel application for property listings, bookings, and reviews.

## Features

- **Property Listings**: Create and manage travel property listings with detailed information
- **Booking System**: Handle property bookings with date validation and guest limits
- **Review System**: Allow users to rate and review properties
- **User Management**: User authentication and profile management
- **REST API**: Full API support with Django REST Framework
- **Database Seeding**: Management command to populate the database with sample data

## Models

### Listing

- Property details (title, description, address, etc.)
- Pricing and capacity information
- Property type and amenities
- Host relationship
- Availability status

### Booking

- Guest and listing relationships
- Check-in/check-out dates
- Guest count and total price calculation
- Booking status management
- Special requests

### Review

- Rating system (1-5 stars)
- User comments
- One review per user per listing
- Timestamp tracking

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x00
   ```

2. **Create and activate virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install django djangorestframework
   ```

4. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Seed the database with sample data**

   ```bash
   python manage.py seed
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

## Usage

### Seeding the Database

The application includes a management command to populate the database with sample data:

```bash
# Use default values (5 users, 20 listings, 30 bookings, 50 reviews)
python manage.py seed

# Customize the number of records
python manage.py seed --users 10 --listings 50 --bookings 100 --reviews 200
```

### API Endpoints

The application provides REST API endpoints for all models:

- **Listings**: `/api/listings/`
- **Bookings**: `/api/bookings/`
- **Reviews**: `/api/reviews/`
- **Users**: `/api/users/`

### Sample Data

The seed command creates:

- **Users**: Sample users with credentials (username: user1, password: password123)
- **Listings**: Properties in various cities worldwide with different types and amenities
- **Bookings**: Sample bookings with different statuses and date ranges
- **Reviews**: User reviews with ratings and comments

## Project Structure

```text
alx_travel_app_0x00/
├── alx_travel_app/          # Django project settings
├── listings/                # Main app
│   ├── models.py           # Database models
│   ├── serializers.py      # API serializers
│   ├── management/
│   │   └── commands/
│   │       └── seed.py     # Database seeding command
│   └── migrations/         # Database migrations
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Database Schema

### Listing Model
- `title`: Property title
- `description`: Detailed description
- `address`, `city`, `state`, `zipcode`, `country`: Location information
- `price_per_night`: Nightly rate
- `bedrooms`, `bathrooms`, `max_guests`: Property capacity
- `property_type`: Type of property (apartment, house, villa, etc.)
- `amenities`: JSON field for property amenities
- `images`: JSON field for property images
- `host`: Foreign key to User model
- `is_available`: Availability status

### Booking Model
- `listing`: Foreign key to Listing
- `guest`: Foreign key to User
- `check_in_date`, `check_out_date`: Booking dates
- `num_guests`: Number of guests
- `total_price`: Calculated total price
- `status`: Booking status (pending, confirmed, cancelled, completed)
- `special_requests`: Optional special requests

### Review Model
- `listing`: Foreign key to Listing
- `reviewer`: Foreign key to User
- `rating`: 1-5 star rating
- `comment`: Review text
- Unique constraint: one review per user per listing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the ALX curriculum and is for educational purposes.

## Author

Created as part of ALX Software Engineering program. 