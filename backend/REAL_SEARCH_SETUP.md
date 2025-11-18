# Setting Up Real Search API

## Why You Need This

Currently, your app uses **mock search** which returns the same articles regardless of topic. To get **real, updated health articles** daily, you need a real search API.

## Recommended: Brave Search API

Brave Search API is ideal for health content because:
- ✅ Independent index (not Google)
- ✅ Privacy-focused
- ✅ 2,000 free searches/month (sufficient for daily automation)
- ✅ Good results for health/medical queries

### Step 1: Get Brave Search API Key

1. Go to: **https://brave.com/search/api/**
2. Click **"Get Started"** or **"Sign Up"**
3. Create account / Sign in
4. Go to your dashboard
5. Click **"Create API Key"** or **"New API Key"**
6. Name it: `EazyHealth`
7. **Copy the API key** (you won't see it again!)

### Step 2: Add API Key to .env

Open `/Users/trinav/personal/eazyhealth/backend/.env` and update:

```env
# Change from mock to brave
SEARCH_PROVIDER="brave"

# Add your Brave API key
BRAVE_API_KEY="your-brave-api-key-here"
```

### Step 3: Restart Backend Server

1. Stop your backend server (Ctrl+C)
2. Start it again:
   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn app.main:app --reload --port 8000
   ```

### Step 4: Test It

Generate a test briefing:
```bash
curl -X POST http://localhost:8000/api/briefings/generate \
  -H "Content-Type: application/json" \
  -d '{"source_type": "article_summary", "topic": "heart disease prevention", "reading_level": "grade8"}'
```

You should now get **real, current articles** from CDC, NIH, Mayo Clinic, etc.!

---

## Alternative: Serper API (Google-based)

If you prefer Google search results:

1. Go to: **https://serper.dev/**
2. Sign up for free account (2,500 free searches/month)
3. Get your API key
4. Update `.env`:
   ```env
   SEARCH_PROVIDER="serper"
   SERPER_API_KEY="your-serper-api-key-here"
   ```

---

## About OpenAI and Web Search

**Q: Can OpenAI search the web on its own?**

**A: No**, the OpenAI API (GPT-4, GPT-3.5) **cannot** directly search the web or browse websites. It only knows information from its training data (up to its knowledge cutoff).

**What we do instead:**
1. **Our app** searches the web using Brave/Serper API
2. **Our app** extracts article text from trusted sources
3. **OpenAI/LLM** summarizes and rewrites the content at the right reading level

This is why you need a separate search API!

---

## Pricing (if you exceed free tier)

### Brave Search API
- Free: 2,000 searches/month
- Paid: $5/month for 20,000 searches

**Your usage:**
- 7 briefings/week × 3 articles each = 21 searches/week
- = ~90 searches/month
- **Well within free tier!** ✅

### Serper API
- Free: 2,500 searches/month
- Paid: $50/month for 5,000 searches

---

## What Happens After Setup

Once you add a real search API:

1. ✅ **Daily automation** will fetch **real, current health articles**
2. ✅ **Duplicate detection** will prevent publishing similar topics within 30 days
3. ✅ **Fresh content** from CDC, NIH, Mayo Clinic, WHO, etc.
4. ✅ **Diverse topics** rotating through your 10 predefined health topics

Your briefings will truly be **up-to-date health news**, not mock data!

---

## Testing Real Search

After setup, test with different topics:

```bash
# Test diabetes search
curl -X POST http://localhost:8000/api/briefings/generate \
  -H "Content-Type: application/json" \
  -d '{"source_type": "article_summary", "topic": "diabetes prevention 2025", "reading_level": "grade8"}'

# Test mental health search
curl -X POST http://localhost:8000/api/briefings/generate \
  -H "Content-Type: application/json" \
  -d '{"source_type": "article_summary", "topic": "teen mental health", "reading_level": "high_school"}'
```

Each should return **different**, **real articles** from trusted sources!
