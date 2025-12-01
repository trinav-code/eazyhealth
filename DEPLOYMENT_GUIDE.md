# EazyHealth AI - Complete Deployment Guide

## 🎯 Goal
Deploy your full-stack EazyHealth AI app to production:
- **Backend**: Render.com (with PostgreSQL + automated scheduler)
- **Frontend**: Vercel (already deployed)

---

## 📋 Prerequisites

### API Keys You'll Need:
- [ ] **OpenAI API Key** (or Anthropic API Key)
  - Get from: https://platform.openai.com/api-keys
  - Recommended: Use `gpt-4o-mini` for cost-effectiveness

- [ ] **Brave Search API Key** (or Serper)
  - Brave: https://brave.com/search/api/
  - Serper: https://serper.dev/
  - Alternative: Use `SEARCH_PROVIDER=mock` for testing (no key needed)

### Accounts You'll Need:
- [ ] Render.com account (free tier available)
- [ ] Vercel account (you already have this)
- [ ] GitHub repository access

---

## 🚀 PART 1: Deploy Backend to Render

### Step 1: Commit Your Changes

First, commit the updated configuration files:

```bash
cd /Users/trinav/personal/eazyhealth

git add backend/scheduler.py backend/render.yaml
git commit -m "Configure backend for production deployment with automated scheduler"
git push origin main
```

### Step 2: Create Render Account & Connect Repo

1. Go to https://render.com and sign up/login
2. Click **"New +"** in top right
3. Select **"Blueprint"**
4. Click **"Connect Account"** to link GitHub
5. Select your `eazyhealth` repository
6. Click **"Connect"**

Render will automatically detect the `render.yaml` file!

### Step 3: Create PostgreSQL Database

**Before deploying the blueprint, create the database:**

1. From Render dashboard, click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `eazyhealth-db`
   - **Database**: `eazyhealth`
   - **User**: (auto-generated)
   - **Region**: Choose closest to you
   - **Plan**: **Free** (or Starter for production)
3. Click **"Create Database"**
4. Wait 1-2 minutes for it to initialize
5. **IMPORTANT**: Copy the **Internal Database URL**
   - Should look like: `postgresql://eazyhealth_db_user:xxxxx@dpg-xxxxx/eazyhealth_db`

### Step 4: Configure Environment Variables

Now deploy your blueprint:

1. Go back to the Blueprint deployment screen
2. Render will show 2 services:
   - `eazyhealth-backend` (web service)
   - `eazyhealth-scheduler` (cron job)

3. For **BOTH services**, add these secret environment variables:

#### Required Variables:

| Variable | Value | Where to Get It |
|----------|-------|-----------------|
| `DATABASE_URL` | `postgresql://...` | From Step 3 above |
| `OPENAI_API_KEY` | `sk-...` | https://platform.openai.com/api-keys |
| `BRAVE_API_KEY` | Your key | https://brave.com/search/api/ |
| `CORS_ORIGINS` | `https://your-app.vercel.app` | Your Vercel frontend URL |

#### For Scheduler Service ONLY:

| Variable | Value |
|----------|-------|
| `API_BASE_URL` | `https://eazyhealth-backend.onrender.com` |

**Note**: Use your actual backend URL (you'll get this after deployment)

#### Optional (defaults are fine):

```
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
SEARCH_PROVIDER=brave
```

### Step 5: Deploy!

1. Click **"Apply"** or **"Create Services"**
2. Render will:
   - Build your backend (3-5 minutes)
   - Start the web service
   - Schedule the cron job

3. Once deployed, you'll get a URL like:
   ```
   https://eazyhealth-backend.onrender.com
   ```

### Step 6: Test Backend

```bash
# Test health endpoint
curl https://your-backend-url.onrender.com/health

# Should return: {"status": "healthy"}

# Test briefings endpoint
curl https://your-backend-url.onrender.com/api/briefings

# Should return: {"items": [], "total": 0, ...}
```

---

## 🌐 PART 2: Connect Frontend to Backend

### Step 1: Update Vercel Environment Variable

1. Go to https://vercel.com/dashboard
2. Select your `eazyhealth` project
3. Go to **Settings** → **Environment Variables**
4. Add/update this variable:

   ```
   Name:  VITE_API_URL
   Value: https://your-backend-url.onrender.com/api
   ```

5. Select all environments: **Production**, **Preview**, **Development**
6. Click **Save**

### Step 2: Redeploy Frontend

**Option A - Trigger from Vercel:**
1. Go to **Deployments** tab
2. Find latest deployment
3. Click **"..."** → **"Redeploy"**

**Option B - Push to GitHub:**
```bash
git commit --allow-empty -m "Trigger redeploy with new backend URL"
git push origin main
```

### Step 3: Verify CORS Configuration

If you get CORS errors, update the backend:

1. In Render dashboard, go to your web service
2. Go to **Environment** tab
3. Update `CORS_ORIGINS` to match your Vercel URL exactly:
   ```
   CORS_ORIGINS=https://your-exact-url.vercel.app
   ```
4. Save (service will auto-redeploy)

---

## 📰 PART 3: Generate Initial Briefings

Your database is empty! Let's add some briefings:

### Option 1: Generate via API (Quick Start)

```bash
# Replace with your actual backend URL
BACKEND_URL="https://your-backend-url.onrender.com"

# Generate 3-5 briefings with different topics
curl -X POST "$BACKEND_URL/api/briefings/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "article_summary",
    "topic": "diabetes management",
    "reading_level": "grade8"
  }'

curl -X POST "$BACKEND_URL/api/briefings/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "article_summary",
    "topic": "heart health",
    "reading_level": "high_school"
  }'

curl -X POST "$BACKEND_URL/api/briefings/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "article_summary",
    "topic": "mental health wellness",
    "reading_level": "grade6"
  }'
```

### Option 2: Use Swagger UI

1. Go to: `https://your-backend-url.onrender.com/docs`
2. Find `POST /api/briefings/generate`
3. Click **"Try it out"**
4. Enter:
   ```json
   {
     "source_type": "article_summary",
     "topic": "vaccine safety",
     "reading_level": "college"
   }
   ```
5. Click **Execute**
6. Repeat with different topics

### Option 3: Wait for Automated Generation

The scheduler runs daily at **6:00 AM UTC**. It will automatically generate:
- 1 article summary briefing (Monday-Friday)
- 2 data analysis briefings (Monday & Thursday)

---

## ⏰ PART 4: Verify Automated Scheduler

### Check Scheduler Configuration

1. In Render dashboard, go to your **cron job** service
2. Verify it shows:
   - Schedule: `0 6 * * *` (daily at 6 AM UTC)
   - Status: **Running** or **Waiting**

### Update Scheduler Environment Variables

Make sure the scheduler has:

```
API_BASE_URL=https://your-backend-url.onrender.com
DATABASE_URL=<same as web service>
OPENAI_API_KEY=<same as web service>
BRAVE_API_KEY=<same as web service>
```

**Tip**: In Render, you can sync environment variables between services!

### Test Scheduler Manually

You can manually trigger the scheduler to test it:

1. Go to Render dashboard → Scheduler service
2. Click **"Manual Trigger"** (if available)
3. Check logs to see if briefings are generated

**OR** test locally first:

```bash
cd backend

# Set environment variables
export API_BASE_URL="https://your-backend-url.onrender.com"
export DATABASE_URL="your-postgres-url"

# Run scheduler
python scheduler.py
```

### View Scheduler Logs

1. In Render dashboard → Scheduler service
2. Click **"Logs"** tab
3. You'll see output like:
   ```
   [Monday] Generating article summary (Grade 6)...
   Successfully generated briefing: "Understanding Diabetes"
   ```

---

## ✅ PART 5: Final Verification

### 1. Test Your Live Site

Go to your Vercel URL: `https://your-app.vercel.app`

**Home Page Should Show:**
- ✅ Latest briefing card (if briefings exist)
- ✅ Explainer input form
- ✅ No console errors (F12 → Console)

**Briefings Page Should Show:**
- ✅ List of all briefings
- ✅ Filter buttons working
- ✅ Pagination working
- ✅ Click on briefing → see full detail

### 2. Test Explainer Feature

1. Go to home page
2. Ask a question: "What is type 2 diabetes?"
3. Select reading level: Grade 6
4. Click "Get Explanation"
5. Should see structured explainer with sources

### 3. Check API Endpoints

```bash
BACKEND_URL="https://your-backend-url.onrender.com"

# Health check
curl $BACKEND_URL/health

# List briefings
curl $BACKEND_URL/api/briefings

# Generate explainer
curl -X POST "$BACKEND_URL/api/explain" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is asthma?",
    "reading_level": "grade6"
  }'
```

---

## 🐛 Troubleshooting

### Issue: Frontend shows "No briefings found"

**Solution:**
1. Check backend API: `curl https://your-backend-url.onrender.com/api/briefings`
2. If empty, generate briefings (see Part 3)
3. Check CORS configuration
4. Check browser console for errors

### Issue: CORS errors in browser console

**Solution:**
1. In Render → Web Service → Environment
2. Set: `CORS_ORIGINS=https://your-exact-vercel-url.vercel.app`
3. No trailing slash!
4. Exact match required

### Issue: Scheduler not generating briefings

**Solution:**
1. Check scheduler logs in Render
2. Verify `API_BASE_URL` is set correctly
3. Verify API keys are synced from web service
4. Manually trigger to test
5. Check that `DATABASE_URL` is correct

### Issue: 500 errors from backend

**Solution:**
1. Check Render logs (Web Service → Logs)
2. Common issues:
   - Invalid API keys
   - Database connection failed
   - Missing environment variables
3. Verify all required env vars are set

### Issue: Explainer feature not working

**Solution:**
1. Check if you set `SEARCH_PROVIDER=mock` (for testing)
2. Or verify `BRAVE_API_KEY` is valid
3. Check backend logs for errors
4. Verify `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is set

---

## 💰 Cost Estimates

### Free Tier (Good for Testing)
- **Render Web Service**: Free (spins down after 15 min inactivity)
- **Render PostgreSQL**: Free (limited storage)
- **Render Cron Job**: Free
- **Vercel**: Free (hobby plan)
- **OpenAI API**: Pay-per-use (~$0.002 per briefing with gpt-4o-mini)
- **Brave Search**: Free tier (2,000 queries/month)

**Estimated Monthly Cost**: $0-5 (mostly API usage)

### Production Tier
- **Render Web Service**: $7/month (always on)
- **Render PostgreSQL**: $7/month (10GB)
- **Render Cron Job**: Included
- **Vercel**: Free or $20/month (Pro)
- **OpenAI API**: ~$10-30/month depending on usage
- **Brave Search**: $5/month (5,000 queries)

**Estimated Monthly Cost**: $29-69

---

## 📊 What Happens After Deployment

### Daily Automation (6 AM UTC)

The scheduler will automatically:

**Monday:**
- Generate 1 data analysis briefing (rotating level)
- Generate 1 article summary (Grade 6)

**Tuesday:**
- Generate 1 article summary (Grade 8)

**Wednesday:**
- Generate 1 article summary (High School)

**Thursday:**
- Generate 1 data analysis briefing (rotating level)
- Generate 1 article summary (College)

**Friday:**
- Generate 1 article summary (Grade 3)

**Total: 7 briefings per week automatically!**

### Topics Rotation

The scheduler rotates through these health topics:
- Diabetes management
- Heart health and cardiovascular disease
- Mental health and wellness
- Nutrition and healthy eating
- Vaccine safety and effectiveness
- Cancer prevention and screening
- Sleep and health
- Exercise and physical activity
- Antibiotic resistance
- Maternal and child health

---

## 🎉 Success Checklist

- [ ] Backend deployed to Render
- [ ] PostgreSQL database created and connected
- [ ] All environment variables configured
- [ ] Frontend connected to backend
- [ ] Scheduler cron job configured
- [ ] Initial briefings generated
- [ ] Frontend shows briefings correctly
- [ ] Explainer feature works
- [ ] No CORS errors
- [ ] Scheduler runs daily successfully

---

## 📚 Additional Resources

- **Render Documentation**: https://render.com/docs
- **Vercel Documentation**: https://vercel.com/docs
- **OpenAI API Docs**: https://platform.openai.com/docs
- **Brave Search API**: https://brave.com/search/api/docs

---

## 🆘 Need Help?

Common issues and solutions are in the Troubleshooting section above.

For project-specific issues:
1. Check Render logs (Web Service → Logs)
2. Check browser console (F12)
3. Test API endpoints directly with curl
4. Verify environment variables are set correctly

---

**You're all set! Your EazyHealth AI app is now running in production with automated daily briefings!** 🚀
