# ALX Travel App API

A Django REST API for managing travel property listings, bookings, and reviews.

## Features

- **Listings Management**: Create, read, update, and delete property listings
- **Booking System**: Manage property bookings with status tracking
- **Review System**: Allow users to review properties
- **User Authentication**: Secure API with authentication and authorization
- **RESTful Design**: Follows REST conventions with proper HTTP methods
- **Pagination**: Built-in pagination for large datasets
- **Filtering**: Filter listings by availability and other criteria

## API Endpoints

### Base URL
```
http://localhost:8000/api/
```

### Listings Endpoints

#### GET /api/listings/
- **Description**: Get all listings with pagination
- **Authentication**: Not required (read-only)
- **Response**: Paginated list of listings with reviews and ratings

#### GET /api/listings/{id}/
- **Description**: Get a specific listing with detailed information
- **Authentication**: Not required (read-only)
- **Response**: Detailed listing information including bookings

#### POST /api/listings/
- **Description**: Create a new listing
- **Authentication**: Required
- **Request Body**: Listing data (title, description, address, etc.)
- **Response**: Created listing object

#### PUT /api/listings/{id}/
- **Description**: Update a listing (full update)
- **Authentication**: Required (host only)
- **Request Body**: Complete listing data
- **Response**: Updated listing object

#### PATCH /api/listings/{id}/
- **Description**: Partially update a listing
- **Authentication**: Required (host only)
- **Request Body**: Partial listing data
- **Response**: Updated listing object

#### DELETE /api/listings/{id}/
- **Description**: Delete a listing
- **Authentication**: Required (host only)
- **Response**: 204 No Content

#### GET /api/listings/available/
- **Description**: Get all available listings
- **Authentication**: Not required
- **Response**: List of available listings

#### GET /api/listings/my_listings/
- **Description**: Get all listings created by the current user
- **Authentication**: Required
- **Response**: List of user's listings

#### GET /api/listings/{id}/reviews/
- **Description**: Get all reviews for a specific listing
- **Authentication**: Not required
- **Response**: List of reviews for the listing

#### POST /api/listings/{id}/add_review/
- **Description**: Add a review to a specific listing
- **Authentication**: Required
- **Request Body**: Review data (rating, comment)
- **Response**: Created review object

### Bookings Endpoints

#### GET /api/bookings/
- **Description**: Get all bookings (user's bookings and hosted bookings)
- **Authentication**: Required
- **Response**: Paginated list of bookings

#### GET /api/bookings/{id}/
- **Description**: Get a specific booking
- **Authentication**: Required (guest or host)
- **Response**: Detailed booking information

#### POST /api/bookings/
- **Description**: Create a new booking
- **Authentication**: Required
- **Request Body**: Booking data (listing_id, check_in_date, check_out_date, num_guests)
- **Response**: Created booking object

#### PUT /api/bookings/{id}/
- **Description**: Update a booking (full update)
- **Authentication**: Required (guest or host)
- **Request Body**: Complete booking data
- **Response**: Updated booking object

#### PATCH /api/bookings/{id}/
- **Description**: Partially update a booking
- **Authentication**: Required (guest or host)
- **Request Body**: Partial booking data
- **Response**: Updated booking object

#### DELETE /api/bookings/{id}/
- **Description**: Delete a booking
- **Authentication**: Required (guest or host)
- **Response**: 204 No Content

#### GET /api/bookings/my_bookings/
- **Description**: Get all bookings made by the current user
- **Authentication**: Required
- **Response**: List of user's bookings

#### GET /api/bookings/my_hosted_bookings/
- **Description**: Get all bookings for listings owned by the current user
- **Authentication**: Required
- **Response**: List of hosted bookings

#### POST /api/bookings/{id}/cancel/
- **Description**: Cancel a booking
- **Authentication**: Required (guest or host)
- **Response**: Updated booking object

#### POST /api/bookings/{id}/confirm/
- **Description**: Confirm a booking (host only)
- **Authentication**: Required (host only)
- **Response**: Updated booking object

### Reviews Endpoints

#### GET /api/reviews/
- **Description**: Get all reviews
- **Authentication**: Not required (read-only)
- **Response**: Paginated list of reviews

#### GET /api/reviews/{id}/
- **Description**: Get a specific review
- **Authentication**: Not required (read-only)
- **Response**: Review object

#### POST /api/reviews/
- **Description**: Create a new review
- **Authentication**: Required
- **Request Body**: Review data (listing, rating, comment)
- **Response**: Created review object

#### PUT /api/reviews/{id}/
- **Description**: Update a review (full update)
- **Authentication**: Required (reviewer only)
- **Request Body**: Complete review data
- **Response**: Updated review object

#### PATCH /api/reviews/{id}/
- **Description**: Partially update a review
- **Authentication**: Required (reviewer only)
- **Request Body**: Partial review data
- **Response**: Updated review object

#### DELETE /api/reviews/{id}/
- **Description**: Delete a review
- **Authentication**: Required (reviewer only)
- **Response**: 204 No Content

## Data Models

### Listing
- `id`: Primary key
- `title`: Property title
- `description`: Property description
- `address`: Property address
- `city`, `state`, `zipcode`, `country`: Location details
- `price_per_night`: Price per night
- `bedrooms`, `bathrooms`, `max_guests`: Property details
- `property_type`: Type of property (apartment, house, villa, cabin, condo)
- `amenities`: List of amenities (JSON field)
- `images`: List of image URLs (JSON field)
- `host`: Foreign key to User
- `is_available`: Availability status
- `created_at`, `updated_at`: Timestamps

### Booking
- `id`: Primary key
- `listing`: Foreign key to Listing
- `guest`: Foreign key to User
- `check_in_date`, `check_out_date`: Booking dates
- `num_guests`: Number of guests
- `total_price`: Calculated total price
- `status`: Booking status (pending, confirmed, cancelled, completed)
- `special_requests`: Special requests text
- `created_at`, `updated_at`: Timestamps

### Review
- `id`: Primary key
- `listing`: Foreign key to Listing
- `reviewer`: Foreign key to User
- `rating`: Rating (1-5)
- `comment`: Review comment
- `created_at`, `updated_at`: Timestamps

## Authentication

The API uses Django's built-in authentication system with the following classes:
- Session Authentication
- Basic Authentication

## Permissions

- **Listings**: Read-only for anonymous users, full CRUD for authenticated users (host only for updates/deletes)
- **Bookings**: Full CRUD for authenticated users (guest or host for updates/deletes)
- **Reviews**: Read-only for anonymous users, full CRUD for authenticated users (reviewer only for updates/deletes)

## Installation and Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd alx_travel_app_0x01
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Testing the API

### Using curl

1. **Get all listings**:
```bash
curl http://localhost:8000/api/listings/
```

2. **Get available listings**:
```bash
curl http://localhost:8000/api/listings/available/
```

3. **Get a specific listing**:
```bash
curl http://localhost:8000/api/listings/1/
```

4. **Create a listing** (requires authentication):
```bash
curl -X POST http://localhost:8000/api/listings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "title": "Beautiful Apartment",
    "description": "Stunning apartment in the heart of the city",
    "address": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zipcode": "10001",
    "country": "USA",
    "price_per_night": "150.00",
    "bedrooms": 2,
    "bathrooms": 1,
    "max_guests": 4,
    "property_type": "apartment",
    "amenities": ["WiFi", "Kitchen", "Pool"],
    "images": ["https://example.com/image1.jpg"]
  }'
```

### Using Postman

1. Import the API endpoints into Postman
2. Set the base URL to `http://localhost:8000/api/`
3. For authenticated endpoints, use Basic Authentication or Session Authentication
4. Test each endpoint with appropriate HTTP methods and data

## API Documentation

The API includes browsable documentation. Visit `http://localhost:8000/api/` in your browser to see the interactive API documentation provided by Django REST Framework.

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK`: Successful GET, PUT, PATCH requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the ALX Software Engineering program. 