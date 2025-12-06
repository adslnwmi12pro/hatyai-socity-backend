# KitPokeMap Backend API

Backend API for KitPokeMap - Pokemon GO Map Application for Kanchanaburi, Thailand

## Tech Stack
- Flask (Python Web Framework)
- Supabase (PostgreSQL Database)
- Gunicorn (WSGI HTTP Server)

## Deployment on Railway.app

### Quick Deploy
1. Go to https://railway.app/
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose: `adslnwmi12pro/hatyai-socity-backend`
5. Add Environment Variables (see below)
6. Deploy!

### Environment Variables Required:
```
SUPABASE_URL=https://tjxxkhdvhwmpbhwayfmk.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRqeHhraGR2aHdtcGJod2F5Zm1rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDU5OTQ3MiwiZXhwIjoyMDgwMTc1NDcyfQ.sDH9_yk1BxI4YMoEyZ6NECEsJ5q0op4PYIGQva33JJA
PORT=5000
```

### Railway Configuration:
Railway will automatically detect Python and install dependencies from `requirements.txt`.

The start command is configured in `railway.json`:
```
cd src && gunicorn main:app --bind 0.0.0.0:$PORT
```

## Alternative: Render.com Deployment

### Environment Variables Required:
Same as Railway (see above)

### Render Configuration:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `cd src && gunicorn main:app --bind 0.0.0.0:$PORT`
- **Environment**: Python 3

## API Endpoints

### Health Check
- `GET /` - Welcome message
- `GET /health` - Health status

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user

### Pokemon
- `GET /api/pokemons` - Get all pokemon spawns
- `POST /api/pokemons` - Report new pokemon spawn

### Comments
- `GET /api/comments/:pokemon_id` - Get comments for pokemon
- `POST /api/comments` - Add new comment

### Admin
- `GET /api/admin/users` - Get all users (admin only)
- `GET /api/admin/stats` - Get statistics (admin only)

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
cd src && python main.py
```

## License
MIT
