
# Jointoit test task

## Setup

    cp t-env.json env.json

Fill env.json with your data

    pyton manage.py docker

Create compose and Dockerfile

    docker compose up --build -d

Starts app

## Stack

- Django / drf
- Postgresql / redis
- Grafana
- Celery


## Details

- Email service works via Celery
- Authorization with JWT
- Full authorization service with verifying and recovering


## Docs
http://127.0.0.1:8000/api/docs


## Documentation

### Overview
This API provides:
- User authentication (JWT + session cookies)
- Event CRUD operations
- Event registration system
- Member management
- Password reset & email verification
- Event search functionality

### Base URL
/api/v1/

### Authentication
The API supports two authentication methods:
1. JWT Authentication
Send token in headers:
Authorization: Bearer <access_token>
2. Session Authentication
Uses Django session cookie:
sessionid=<cookie>

### User Endpoints

#### Register User
    POST /users/register/
Request:
    
    {
      "email": "user@example.com",
      "name": "John Doe",
      "password": "securepass123"
    }

#### Login
    POST /users/login/
Request:

    {
      "email": "user@example.com",
      "password": "securepass123"
    }

Response:

    {
      "access": "jwt_access_token",
      "refresh": "jwt_refresh_token"
    }

#### Refresh Token
    POST /users/refresh/
Request:

    {
      "refresh": "refresh_token"
    }

Response:

    {
      "access": "new_access_token"
    }

#### Logout
    GET /users/logout/

#### Forgot Password
    POST /users/forgot/

Request

    {
      "email": "user@example.com"
    }


#### Reset Password
    POST /users/reset/

Request

    {
      "email": "user@example.com",
      "code": "123456",
      "password": "newpassword123"
    }

#### Verify Email
    POST /users/verify/

Request

    {
      "email": "user@example.com",
      "code": "123456"
    }

### Event Endpoints
#### List Events
    GET /events/

#### Create Event
    POST /events/

Request

    {
      "title": "Tech Meetup",
      "description": "Django conference",
      "date": "2026-05-20T18:00:00Z",
      "location": "Kyiv"
    }

#### Get Event Detail
    GET /events/{id}/

#### Update Event
    PUT /events/{id}/

#### Partial Update Event
    PATCH /events/{id}/

#### Delete Event
    DELETE /events/{id}/

### Event Actions

#### Register for Event
    POST /events/{id}/register/

#### Leave Event
    POST /events/{id}/leave/

#### Kick Member (Organizer only)
    POST /events/{id}/kick/

Request

    {
      "user_id": 1
    }

#### Get Event Members
    GET /events/{id}/members/

#### Search Events
    POST /events/search/

Request

    {
      "query": "django",
      "organizer_id": 1,
      "date_from": "2026-05-01T00:00:00Z",
      "date_to": "2026-06-01T00:00:00Z"
    }
