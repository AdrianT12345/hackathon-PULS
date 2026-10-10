# PULS Gdańsk - Backend

This is the Django backend directory for PULS Gdańsk.

📖 **For full documentation, see the main [README](../README.md).**

## Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Run tests
python manage.py test mapa

# Create superuser (optional)
python manage.py createsuperuser
```

## Management Commands

```bash
# Load district data from GeoJSON
python manage.py load_dzielnice --file Dzielnice.geojson

# Load demographic data
python manage.py load_demografia

# Generate sample events
python manage.py generate_zdarzenia
```

