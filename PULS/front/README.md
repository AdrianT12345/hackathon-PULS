# PULS Gdańsk - Frontend

This is the Vue.js frontend for PULS Gdańsk.

📖 **For full documentation, see the main [README](../../README.md).**

## Quick Commands

```bash
# Install dependencies
npm install

# Start development server (with hot-reload)
npm run serve

# Build for production
npm run build

# Lint and fix files
npm run lint
```

## Environment Variables

Copy `.env.example` to `.env.local` for custom configuration:

```bash
cp .env.example .env.local
```

## Development

The frontend expects the Django backend to be running at `http://localhost:8000`.

Make sure to start the backend first:

```bash
cd ../
python manage.py runserver
```

Then start the frontend:

```bash
npm run serve
```

Open **http://localhost:8080** in your browser.
