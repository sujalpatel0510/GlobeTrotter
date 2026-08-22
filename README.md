# 🌍 GlobeTrotter — Smart Travel Planning & Itinerary Platform

A full-stack travel-planning web application designed with a **vintage atlas & boarding-pass aesthetic**, powered by **Python Flask**, **PostgreSQL**, **SQLAlchemy ORM**, and containerized with **Docker & Docker Compose**.

---

## 🌟 Key Application Features

### 1. 🔐 Authentication & Traveler Profiles
- **Secure Authentication**: User registration and login powered by Werkzeug password hashing and Flask-Login session management.
- **Profile Management**: Upload custom avatar photos with instant preview, manage travel statistics (trips planned, countries explored, wishlist counts), update personal bios, and configure settings.
- **Role-Based Access Control**: Standard traveler roles vs. platform administrators (`is_admin`).
- **One-Click Guest Access**: Instant demo explore button to experience the platform as traveler **Maya Rao**.

### 2. 🗺️ Trip Planning & Itinerary Builder
- **Trip Creation**: Plan new journeys with destination name, start/end dates, cover visual themes (`pat-1`, `pat-2`, `teal`), budget goals, and notes.
- **Interactive Itinerary Builder**: Dynamically organize multi-stop itineraries with day-by-day section budgets, notes, and drag-and-drop stop sequences.
- **Flight-Node Timeline & Budget Analytics**: Visual timeline connecting itinerary items, real-time category spending breakdowns (*Transport*, *Stays*, *Tours & Activities*, *Food & Dining*), and over-budget alerts.
- **Trip Duplication & Sharing**: Clone any public or completed itinerary into your personal account with one click, or generate shareable public tokens (`/trips/share/<token>`).

### 3. 🏙️ Destination Catalog & Activity Explorer
- **Search & Filter**: Discover destinations and curated activities across categories (*Adventure*, *Culture*, *Food & Drink*, *Experience*).
- **Interactive Modals**: Add curated activities or new city stops directly into existing personal trips.
- **"+ Add New City" to Catalog**: Add brand new destinations to the global PostgreSQL catalog with cost ratings ($ / $$ / $$$), visual themes, and highlights.

### 4. 💬 Community Travel Dispatches & Feed
- **Travel Stories & Dispatches**: Social feed where travelers share authentic recommendations, hidden spots, and budget lessons.
- **Trip Attachment**: Link dispatches directly to an itinerary so others can explore the full route.
- **Live Heart Likes**: Real-time AJAX like toggles with animated counters.
- **Filter Tags**: Filter dispatches by trending tags (`#Japan`, `#BudgetTip`, `#Italy`, `#Museums`, `#Food`).
- **Community Analytics Sidebar**: Global verified insights, top curators, and cultural travel guidelines.

### 5. 📅 Calendar Matrix View
- Visual month/year calendar matrix mapping out ongoing, upcoming, and completed journeys with color-coded event bars and direct trip links.

### 6. 📊 Admin & Analytics Dashboard
- Comprehensive platform analytics: total itineraries created, active travelers, top destinations, average trip budgets, and shared links.
- User management panel with one-click user activation/deactivation.

---

## 🗄️ PostgreSQL Database Schema

```mermaid
erDiagram
    USERS ||--o{ TRIPS : creates
    USERS ||--o{ COMMUNITY_POSTS : writes
    TRIPS ||--o{ ITINERARY_SECTIONS : contains
    ITINERARY_SECTIONS ||--o{ ITINERARY_ITEMS : contains
    TRIPS ||--o{ COMMUNITY_POSTS : links
    DESTINATIONS ||--o{ ACTIVITIES : features

    USERS {
        int id PK
        string email UK
        string first_name
        string last_name
        string avatar_url
        boolean is_admin
        boolean is_active
    }
    TRIPS {
        int id PK
        int user_id FK
        string name
        date start_date
        date end_date
        float total_budget
        string status
        string share_token UK
    }
    ITINERARY_SECTIONS {
        int id PK
        int trip_id FK
        int section_order
        string title
        float allocated_budget
    }
    ITINERARY_ITEMS {
        int id PK
        int section_id FK
        string title
        string time_label
        string category
        float cost
        int day_number
    }
    DESTINATIONS {
        int id PK
        string name UK
        string country
        string cost_index
        int trips_count
    }
    ACTIVITIES {
        int id PK
        int destination_id FK
        string name
        string category
        float price
    }
    COMMUNITY_POSTS {
        int id PK
        int user_id FK
        int trip_id FK
        text content
        string tags
        int likes_count
    }
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+**
- **PostgreSQL 14+** (or Docker)

### Environment Configuration (`.env`)
Create a `.env` file in the root directory:
```env
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=globetrotter-super-secret-key-change-in-production

POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=globetrotter_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgresql://postgres:your_password@localhost:5432/globetrotter_db
UPLOAD_FOLDER=app/static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Local Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd ODOO_LD
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows:
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux:
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize and seed PostgreSQL database**:
   ```bash
   python run.py --init-db
   ```

5. **Start the Flask development server**:
   ```bash
   python run.py
   ```
   Open **[http://localhost:5000](http://localhost:5000)** in your browser.

---

## 🐳 Running with Docker & Docker Compose

To launch both the Flask application and a dedicated PostgreSQL container:

```bash
docker compose up --build
```

- Web Application: **[http://localhost:5000](http://localhost:5000)**
- Health Check: **[http://localhost:5000/health](http://localhost:5000/health)**

---

## 🔑 Demo Credentials

| Role | Email | Password | Access Details |
| :--- | :--- | :--- | :--- |
| **Traveler** | `maya@example.com` | `password123` | Maya Rao (5 planned/completed trips, custom avatars, budget data) |
| **Admin** | `admin@globetrotter.com` | `admin123` | Administrator (Access to `/admin` analytics & user management) |

*(You can also click **"Continue as guest"** on the login page to explore Maya's account instantly.)*

---

## 🧪 Automated Testing Suite

The application includes an automated test suite verifying models, authentication, budget mathematics, and route endpoints:

```bash
python -m unittest discover -s tests
```

---

## 📁 Repository Structure

```
ODOO_LD/
├── app/
│   ├── __init__.py          # Flask app factory, extension initializations, blueprint registrations
│   ├── config.py            # Development, Production, Testing configurations
│   ├── seeder.py            # Database seeder with demo trips, users, and catalog
│   ├── models/              # SQLAlchemy Database Models
│   │   ├── user.py          # User model & auth hashing
│   │   ├── trip.py          # Trip model & budget math properties
│   │   ├── itinerary.py     # ItinerarySection & ItineraryItem models
│   │   ├── destination.py   # Destination & Activity catalog models
│   │   └── community.py     # CommunityPost model
│   ├── routes/              # Modular Flask Blueprints
│   │   ├── auth.py          # Login, Register, Logout, Guest access
│   │   ├── main.py          # Dashboard, Calendar matrix, Health check
│   │   ├── trips.py         # Trip CRUD, duplication, budget calculation
│   │   ├── itinerary.py     # Builder, itinerary view, sharing tokens
│   │   ├── explore.py       # Activity search & Add City to catalog
│   │   ├── community.py     # Community feed, story creation, AJAX likes
│   │   ├── profile.py       # Profile settings & photo uploads
│   │   ├── admin.py         # Admin dashboard & user status toggle
│   │   └── api.py           # REST endpoints
│   └── utils/               # Decorators & image upload helpers
├── templates/               # Jinja2 Dynamic HTML Templates
│   ├── base.html            # Global layout, sticky navbar, footer
│   ├── index.html           # Login page
│   ├── register.html        # Registration page with live avatar preview
│   ├── dashboard.html       # Main travel hub & active trips
│   ├── my-trips.html        # All trips filter & management
│   ├── create-trip.html     # Plan a new trip form
│   ├── itinerary-builder.html # Interactive drag/drop itinerary builder
│   ├── itinerary-view.html  # Timeline & budget category breakdown
│   ├── search.html          # Destination & activity explorer with Add City modal
│   ├── community.html       # Social feed & travel dispatches
│   ├── calendar.html        # Annual travel calendar matrix
│   ├── profile.html         # User profile & statistics
│   ├── admin.html           # Admin analytics panel
│   ├── shared-itinerary.html# Public shareable trip view
│   ├── css/style.css        # Vintage atlas theme, boarding-pass UI styling
│   └── js/app.js            # Modals, AJAX liking, image preview helpers
├── tests/
│   └── test_backend.py      # Unit & integration test suite
├── Dockerfile               # Production container definition
├── docker-compose.yml       # Flask + PostgreSQL container stack
├── requirements.txt         # Pinned Python package dependencies
├── run.py                   # Server entry point
└── README.md                # Project documentation
```
