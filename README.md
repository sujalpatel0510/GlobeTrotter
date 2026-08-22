# GlobeTrotter — Full-Stack Travel Planning Platform

A full-stack travel-planning web application styled like a vintage atlas and boarding pass, built with **Python Flask**, **PostgreSQL**, **SQLAlchemy ORM**, **Flask-Migrate**, **Flask-Login**, and containerized with **Docker & Docker Compose**.

---

## 🌟 Key Features

- **User Authentication & Profile**:
  - Secure registration & login with password hashing (Werkzeug).
  - Profile photo uploads, travel stats, country wishlist count, account deletion.
  - Role-based authorization (`admin` vs `user`).
- **Trip & Itinerary Management**:
  - Create trips with dates, cover images, descriptions, and budget goals.
  - Interactive **Itinerary Builder**: dynamic stops, day-by-day section budgets, and note taking.
  - **Itinerary & Budget Analytics**: Day-by-day flight-node timeline, category breakdown (Transport, Stay, Activities, Meals), and over-budget warnings.
  - **Trip Duplication & Deletion**: Clone any completed/public trip into your account with one click.
- **City & Activity Exploration**:
  - Search destinations and curated activities by keywords and categories (Adventure, Food & Drink, Culture, Experience).
  - "+ Add to trip" modal to instantly attach activities/cities to any of your trips.
- **Yearly / Monthly Calendar**:
  - Calendar matrix visually highlighting trip durations with color-coded badges (Ongoing, Upcoming, Completed).
- **Community Travel Stories**:
  - Social feed where travelers share trip reviews, recommendations, and budget tips with tags and AJAX like counters.
- **Admin Panel & Analytics**:
  - Platform overview: total trips created, active users, top cities, average budget, shared links count.
  - User management table with one-click activate/deactivate.

---

## 🚀 Running with Docker & PostgreSQL (Recommended)

### Prerequisites
- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

### Quick Start

1. **Clone or navigate to the repository directory**:
   ```bash
   cd ODOO_LD
   ```

2. **Start the containers** (Flask app + PostgreSQL 16):
   ```bash
   docker compose up --build
   ```

3. **Access the application**:
   - Web App: [http://localhost:5000](http://localhost:5000)
   - Health Check: [http://localhost:5000/health](http://localhost:5000/health)

The database will be automatically initialized and seeded with rich demo trips, destinations, activities, and community posts.

---

## 💻 Running Locally (Without Docker)

1. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize and Seed the database**:
   ```bash
   python run.py --init-db --seed
   ```

4. **Run the Flask development server**:
   ```bash
   python run.py
   ```
   Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## 🔑 Demo Accounts

| Role | Email | Password | Details |
|------|-------|----------|---------|
| **Traveler** | `maya@example.com` | `password123` | Maya Rao (5 active & completed trips, Japan, NYC, Paris, etc.) |
| **Admin** | `admin@globetrotter.com` | `admin123` | Administrator (Full access to `/admin` dashboard) |

*You can also click **"Continue as guest"** on the login page to instantly explore as Maya Rao.*

---

## 🧪 Running Tests

To run the automated test suite:
```bash
python -m unittest discover -s tests
```

---

## 📁 Project Architecture

```
ODOO_LD/
├── app/
│   ├── __init__.py          # Flask app factory, extension initializations, blueprint registrations
│   ├── config.py            # Development, Production, Testing configurations
│   ├── models/              # SQLAlchemy Database Models
│   │   ├── user.py          # User (auth, profile, roles)
│   │   ├── trip.py          # Trip (dates, budget, status, share token)
│   │   ├── itinerary.py     # ItinerarySection & ItineraryItem (stops, costs, timings)
│   │   ├── destination.py   # Destination & Activity (search catalog, cost index)
│   │   └── community.py     # CommunityPost (social stories, tags, likes)
│   ├── routes/              # Modular Blueprints
│   │   ├── auth.py          # Login, Register, Logout, Guest access
│   │   ├── main.py          # Dashboard, Calendar view, Health check
│   │   ├── trips.py         # My Trips, Create Trip, Duplicate, Delete
│   │   ├── itinerary.py     # Itinerary Builder, Itinerary View, Share public link
│   │   ├── explore.py       # City/Activity Search & "+ Add to trip"
│   │   ├── community.py     # Social stories & travel tips
│   │   ├── profile.py       # User Profile update, settings, delete account
│   │   ├── admin.py         # Admin dashboard, platform metrics, user management
│   │   └── api.py           # REST endpoints for dynamic frontend interactions
│   ├── templates/           # Jinja2 Dynamic HTML Templates (refactored with base layout)
│   ├── static/              # Static Assets (CSS styles, JS app, file uploads)
│   ├── utils/               # Decorators & image upload helpers
│   └── seeder.py            # Comprehensive demo data population
├── tests/
│   └── test_backend.py      # Automated unit tests
├── Dockerfile               # Multi-stage production-ready Dockerfile
├── docker-compose.yml       # Docker Compose for Flask app + PostgreSQL 16
├── requirements.txt         # Pinned Python dependencies
├── run.py                   # Application entry point
└── README.md
```
