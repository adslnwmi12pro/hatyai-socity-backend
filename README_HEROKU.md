# Deploy Backend to Heroku

## Prerequisites

1. Create a Heroku account: https://signup.heroku.com/
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
3. Install Git (if not already installed)

## Deployment Steps

### 1. Login to Heroku

```bash
heroku login
```

### 2. Initialize Git Repository (if not already initialized)

```bash
cd /path/to/hatyai-socity-fast-backend
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### 3. Create Heroku App

```bash
heroku create hatyai-socity-backend
```

Or use a custom name:

```bash
heroku create your-custom-app-name
```

### 4. Set Environment Variables

```bash
heroku config:set SUPABASE_URL=https://tjxxkhdvhwmpbhwayfmk.supabase.co
heroku config:set SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRqeHhraGR2aHdtcGJod2F5Zm1rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDU5OTQ3MiwiZXhwIjoyMDgwMTc1NDcyfQ.sDH9_yk1BxI4YMoEyZ6NECEsJ5q0op4PYIGQva33JJA
```

### 5. Deploy to Heroku

```bash
git push heroku main
```

Or if your branch is named `master`:

```bash
git push heroku master
```

### 6. Check Deployment Status

```bash
heroku logs --tail
```

### 7. Open Your App

```bash
heroku open
```

## Update Frontend API URL

After deployment, you'll get a Heroku URL like: `https://hatyai-socity-backend.herokuapp.com`

Update the `API_URL` in all Frontend files to point to this new URL:

- `src/pages/LandingPage.jsx`
- `src/pages/Dashboard.jsx`
- `src/pages/AdminDashboard.jsx`
- `src/pages/SubscriptionPage.jsx`
- `src/components/CommentSection.jsx`

Then re-deploy the Frontend to Vercel.

## Troubleshooting

### View Logs

```bash
heroku logs --tail
```

### Restart App

```bash
heroku restart
```

### Check Environment Variables

```bash
heroku config
```

### Run Commands on Heroku

```bash
heroku run bash
```

## Important Notes

1. Heroku free tier has limitations:
   - Apps sleep after 30 minutes of inactivity
   - Limited to 550-1000 dyno hours per month
   - Consider upgrading to Hobby tier ($7/month) for always-on apps

2. Make sure to add `Procfile`, `requirements.txt`, and `runtime.txt` to your repository

3. The `Procfile` specifies how to run your app:
   ```
   web: cd src && gunicorn main:app
   ```

4. The `runtime.txt` specifies the Python version:
   ```
   python-3.11.0
   ```
