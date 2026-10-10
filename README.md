# 🏙️ PULS Gdańsk

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-brightgreen.svg)](https://vuejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> Interactive city map of Gdańsk with community features, demographics visualization, and infrastructure analysis.

** Smart City Hackathon Project**

![PULS Gdańsk Demo](PULS/front/public/images/logo.png)

##  Features

- ** Demographics** - Visualize demographic data by district (age groups, gender distribution)
- ** Transport** - Real-time public transport vehicle tracking (buses, trams)
- ** Community** - Report incidents and events, community engagement platform
- ** Important Places** - Interactive map of schools and pharmacies with infrastructure analysis
- ** Heatmaps** - Population density and event clustering visualization
- ** Responsive** - Works on desktop and mobile devices

##  Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/Smart-City-Hackhaton.git
cd Smart-City-Hackhaton-main/PULS
```

### 2. Backend Setup (Django)

```bash
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver
```

Backend runs at: **http://localhost:8000**

### 3. Frontend Setup (Vue.js)

```bash
# Navigate to frontend directory
cd front

# Install dependencies
npm install

# Start development server
npm run serve
```

Frontend runs at: **http://localhost:8080**

### 4. You're ready

Open **http://localhost:8080** in your browser.

##  Admin Access

Click "Zaloguj" (Login) button in the top-right corner.

**Demo password:** `admin123`

Admin features include:
-  Action proposals based on community reports
-  Infrastructure shortage analysis
-  Simulation of new school/pharmacy locations

##  Project Structure

```
PULS/
├── front/                  # Vue.js Frontend
│   ├── src/
│   │   ├── App.vue        # Main application component
│   │   └── main.js        # Vue entry point
│   ├── public/
│   │   ├── data/          # JSON data files
│   │   └── images/        # Static images
│   └── package.json
├── mapa/                   # Django App
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # DRF serializers
│   ├── urls.py            # URL routing
│   └── tests.py           # Unit tests
├── PULS/                   # Django Configuration
│   └── settings.py
├── requirements.txt        # Python dependencies
├── manage.py
└── db.sqlite3             # SQLite database (demo data included)
```

##  Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Vue.js 3, Leaflet.js, Axios |
| **Backend** | Django 4.2, Django REST Framework |
| **Database** | SQLite (development) |
| **Maps** | OpenStreetMap + Leaflet.js |
| **Real-time Data** | Gdańsk Public Transport API |

##  API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dzielnice/` | GET | List all districts |
| `/api/dzielnice-geojson/` | GET | Districts as GeoJSON |
| `/api/zdarzenia/` | GET, POST | Community events/reports |
| `/api/zdarzenia-geojson/` | GET | Events as GeoJSON |
| `/api/zdarzenia/{id}/like/` | POST | Like an event |
| `/api/zdarzenia/{id}/dislike/` | POST | Dislike an event |
| `/api/komentarze/` | GET, POST | Comments |
| `/api/admin-login/` | POST | Admin authentication |

##  Running Tests

```bash
cd PULS
python manage.py test mapa
```

##  Environment Variables

Copy `.env.example` to `.env` for custom configuration:

```bash
cp .env.example .env
```

Available variables:
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ADMIN_PASSWORD` - Admin login password
- `ALLOWED_HOSTS` - Comma-separated allowed hosts

> **Note:** The project works out-of-the-box without any configuration!

##  Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

##  Team

Built with Bambiki Team :)
 during Smart City Hackathon



