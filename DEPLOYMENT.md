# EazyHealth AI - Deployment Guide

Quick guide to deploy your app to production using Vercel (frontend) + Render (backend).

## Prerequisites

1. GitHub account with your code pushed
2. Vercel account (free): https://vercel.com
3. Render account (free): https://render.com
4. Your API keys ready:
   - OpenAI API key
   - Brave Search API key

---

## Part 1: Deploy Backend to Render

### Step 1: Create PostgreSQL Database (Optional but Recommended)

SQLite doesn't work well on Render's ephemeral filesystem. Use PostgreSQL instead:

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Name: `eazyhealth-db`
4. Select **Free** tier
5. Click **"Create Database"**
6. Copy the **Internal Database URL** (starts with `postgresql://`)

### Step 2: Deploy Backend

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository: `trinav-code/eazyhealth`
4. Configure:
   - **Name**: `eazyhealth-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

5. Click **"Advanced"** and add environment variables:

```
APP_NAME=EazyHealth AI
DEBUG=false
LLM_PROVIDER=openai
LLM_MODEL=gpt-4
LLM_MAX_TOKENS=4096
LLM_TEMPERATURE=0.7
SEARCH_PROVIDER=brave
TRUSTED_DOMAINS=cdc.gov,nih.gov,who.int,mayoclinic.org,hopkinsmedicine.org,health.harvard.edu,webmd.com,medlineplus.gov
RATE_LIMIT_PER_MINUTE=10

# SECRETS (click "Add Secret File" or add as env vars):
OPENAI_API_KEY=sk-proj-your-key-here
BRAVE_API_KEY=your-brave-key-here
DATABASE_URL=postgresql://... (from Step 1, or leave as sqlite:///./eazyhealth.db for testing)
CORS_ORIGINS=https://your-app.vercel.app (you'll update this after frontend deployment)
```

6. Click **"Create Web Service"**
7. Wait for deployment (5-10 minutes)
8. Copy your backend URL: `https://eazyhealth-backend.onrender.com`

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Deploy Frontend

1. Go to https://vercel.com
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repo: `trinav-code/eazyhealth`
4. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)

5. Add **Environment Variable**:
   ```
   VITE_API_URL=https://eazyhealth-backend.onrender.com/api
   ```
   (Use your actual Render backend URL from Part 1, Step 2.8)

6. Click **"Deploy"**
7. Wait for deployment (2-3 minutes)
8. Copy your frontend URL: `https://your-app.vercel.app`

### Step 2: Update Backend CORS

1. Go back to Render dashboard
2. Open your backend service
3. Go to **Environment** tab
4. Update `CORS_ORIGINS` to your Vercel URL:
   ```
   CORS_ORIGINS=https://your-app.vercel.app
   ```
5. Save and wait for automatic redeploy

---

## Part 3: Test Your Deployment

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Try asking a health question
3. Check that briefings load
4. Verify all features work

### Troubleshooting

**Backend not responding:**
- Check Render logs: Dashboard → Service → Logs
- Verify environment variables are set correctly
- Check that DATABASE_URL is valid

**CORS errors:**
- Make sure CORS_ORIGINS in backend matches your exact Vercel URL
- Include `https://` in the URL
- No trailing slash

**Database errors:**
- If using PostgreSQL, make sure DATABASE_URL is set
- Run migrations if needed (Render will auto-run on startup via lifespan)

---

## Alternative: Deploy Everything to Railway

If you want a simpler single-platform deployment:

1. Go to https://railway.app
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select `trinav-code/eazyhealth`
4. Railway will auto-detect both services
5. Add environment variables in dashboard
6. Railway provides URLs for both frontend and backend

**Cost**: $5/month after $5 free trial credit

---

## Production Checklist

- ✅ Backend deployed and accessible
- ✅ Frontend deployed and accessible
- ✅ Environment variables configured
- ✅ CORS configured correctly
- ✅ Database working (PostgreSQL recommended)
- ✅ API keys secured (not in code)
- ✅ Test all features work in production
- ⚠️ Note: Free tier backend sleeps after 15 min inactivity (first request takes ~30 sec to wake)

---

## Ongoing: Automated Briefings

Your scheduler (`scheduler.py`) runs locally via cron. For production:

**Option 1: Use Render Cron Jobs** (Paid Plan)
- Add a cron job service in Render
- Runs scheduler.py daily at 12 PM

**Option 2: GitHub Actions** (Free)
- Create `.github/workflows/daily-briefings.yml`
- Calls backend API endpoint to trigger briefing generation
- Runs on schedule

**Option 3: External Cron Service** (Free)
- Use cron-job.org or similar
- Makes HTTP request to your backend `/api/briefings/generate`
- Set to run daily at 12 PM

For now, keep running scheduler locally or manually trigger briefings via API.

---

## Support

- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app

🎉 Your app is now live!
