# EazyHealth AI

**Health information that finds you and answers you.**

EazyHealth AI is a full-stack web application that makes health information accessible through:

1. **Auto-Generated Briefings** - Weekly/daily summaries of disease trends and health news from trusted sources
2. **On-Demand Explainers** - Instant, easy-to-understand explanations of any health topic with adjustable reading levels

---

## Features

### On-Demand Explainers
- **Ask any health question** and get answers from trustworthy sources (CDC, NIH, Mayo Clinic, etc.)
- **Paste article URLs** to get simplified summaries
- **Choose reading level** from 3rd grade to college level
- Structured explanations with sections: Overview, Key Points, Symptoms, What to Do, etc.
- Source attribution for transparency

### Auto-Generated Briefings
- **Data Analysis Posts** - Analyze disease surveillance data and explain trends
- **Article Summary Posts** - Summarize recent health research and news
- Automatically find and verify trustworthy sources
- Adjustable reading levels for all content

### Key Capabilities
- Web search integration to discover relevant health content
- Article extraction from URLs
- LLM-powered summarization with reading level control
- SQLite database for storing briefings and logs
- Responsive React frontend with Tailwind CSS

---

## Tech Stack

### Backend
- **Python 3.9+**
- **FastAPI** - Modern web framework
- **SQLAlchemy** - ORM for database
- **SQLite** - Database (easy local setup)
- **Anthropic Claude / OpenAI GPT** - LLM providers
- **Trafilatura** - Article extraction
- **Requests** - HTTP client

### Frontend
- **React 18** with TypeScript
- **Vite** - Build tool
- **React Router** - Client-side routing
- **Tailwind CSS** - Styling
- **React Markdown** - Markdown rendering

---

## Project Structure

```
eazyhealth/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Configuration & settings
│   │   ├── database.py          # Database setup
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── briefing.py
│   │   │   ├── explainer_log.py
│   │   │   └── trusted_source.py
│   │   ├── routers/             # API endpoints
│   │   │   ├── explain.py
│   │   │   └── briefings.py
│   │   └── services/            # Business logic
│   │       ├── llm_client.py    # LLM integration
│   │       ├── source_finder.py # Web search
│   │       ├── article_extractor.py
│   │       └── briefing_generator.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API client
│   │   ├── types/               # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

---

## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn

### 1. Clone the Repository

```bash
git clone <repository-url>
cd eazyhealth
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
cd backend
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

pip install -r requirements.txt
```

#### Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# Required: Choose LLM provider and add API key
LLM_PROVIDER="anthropic"  # or "openai"
ANTHROPIC_API_KEY="your-key-here"
# OPENAI_API_KEY="your-key-here"

# Optional: Web search (use "mock" for development)
SEARCH_PROVIDER="mock"  # or "brave" or "serper"
# BRAVE_API_KEY="your-key-here"
# SERPER_API_KEY="your-key-here"
```

#### Initialize Database

The database will be automatically created when you first run the server.

#### Run Backend Server

```bash
# From backend/ directory
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

### 3. Frontend Setup

#### Install Dependencies

```bash
cd frontend
npm install
```

#### Run Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## Usage

### Running the Full Application

1. **Start the backend** (in one terminal):
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **Start the frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

3. **Open your browser** to `http://localhost:5173`

### Using the Application

#### Generate a Demo Briefing

You can generate a demo briefing with mock data using the API:

```bash
curl -X POST http://localhost:8000/api/briefings/generate \
  -H "Content-Type: application/json" \
  -d '{
    "source_type": "data_analysis",
    "use_mock_data": true,
    "reading_level": "grade8"
  }'
```

Or use the Swagger UI at `http://localhost:8000/docs`

#### Ask a Health Question

1. Go to the home page
2. Type a question like "What is atrial fibrillation?"
3. Select your preferred reading level
4. Click "Get Explanation"

The system will:
- Search for trustworthy sources (or use mock data in dev mode)
- Extract and summarize the information
- Present a structured, easy-to-read explainer

#### Explain an Article

1. Switch to "Explain an Article" tab
2. Paste a URL from a health website
3. Select reading level
4. Get a simplified summary

---

## API Endpoints

### Explainer

**POST /api/explain**

Generate a health explainer.

Request body:
```json
{
  "query": "What is diabetes?",
  "reading_level": "grade6"
}
```

Or:
```json
{
  "url": "https://www.cdc.gov/diabetes/basics/diabetes.html",
  "reading_level": "high_school"
}
```

### Briefings

**GET /api/briefings**

List all briefings with pagination.

Query parameters:
- `limit` (default: 10)
- `offset` (default: 0)
- `source_type` (optional: "data_analysis" or "article_summary")

**GET /api/briefings/{slug}**

Get a specific briefing.

**POST /api/briefings/generate**

Generate a new briefing.

Request body:
```json
{
  "source_type": "data_analysis",
  "use_mock_data": true,
  "reading_level": "grade8"
}
```

Or for article summaries:
```json
{
  "source_type": "article_summary",
  "topic": "diabetes research 2025",
  "reading_level": "college"
}
```

---

## Reading Levels

The app supports 5 reading levels:

| Level | Description | Target Audience |
|-------|-------------|----------------|
| `grade3` | Very simple words, short sentences | Age 8-9 |
| `grade6` | Simple language, easy to understand | Age 11-12 |
| `grade8` | Clear and straightforward | Age 13-14 |
| `high_school` | Standard vocabulary with medical terms | Age 15-18 |
| `college` | Advanced vocabulary and terminology | 18+ |

---

## Development

### Backend Development

Run tests (when implemented):
```bash
cd backend
pytest
```

Check code style:
```bash
black app/
flake8 app/
```

### Frontend Development

Build for production:
```bash
cd frontend
npm run build
```

Lint code:
```bash
npm run lint
```

---

## Configuration

### Trusted Sources

By default, the app uses these trusted health domains:
- cdc.gov (Centers for Disease Control)
- nih.gov (National Institutes of Health)
- who.int (World Health Organization)
- mayoclinic.org (Mayo Clinic)
- hopkinsmedicine.org (Johns Hopkins Medicine)
- health.harvard.edu (Harvard Health)
- webmd.com (WebMD)
- medlineplus.gov (MedlinePlus)

You can modify this list in the `.env` file:
```env
TRUSTED_DOMAINS="cdc.gov,nih.gov,custom-domain.org"
```

### LLM Configuration

Switch between providers:
```env
LLM_PROVIDER="anthropic"  # or "openai"
LLM_MODEL="claude-3-5-sonnet-20241022"  # or "gpt-4"
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=4096
```

### Search Configuration

For production, use a real search API:
```env
SEARCH_PROVIDER="brave"  # or "serper"
BRAVE_API_KEY="your-brave-api-key"
```

For development, use mock mode (no API key required):
```env
SEARCH_PROVIDER="mock"
```

---

## Important Disclaimers

**This application is for educational and informational purposes only.**

- It is **NOT** a medical diagnostic tool
- It does **NOT** provide personalized medical advice
- Users should **always** consult qualified healthcare professionals for medical guidance
- The information provided may be incomplete or outdated
- Generated content should be verified with trusted medical sources

All generated content includes disclaimers, and the app is designed to:
- Hedge with cautious language ("may", "generally", etc.)
- Cite trustworthy sources
- Avoid making definitive medical claims
- Encourage users to seek professional medical care

---

## Future Enhancements

Potential features to add:
- [ ] User authentication and personalized briefings
- [ ] Email/SMS notifications for new briefings
- [ ] Advanced data visualization (charts for disease trends)
- [ ] Multi-language support
- [ ] Voice input for accessibility
- [ ] PDF export for briefings
- [ ] Scheduled cron jobs for auto-generating briefings
- [ ] Admin dashboard for managing sources and content

---

## Troubleshooting

### Backend Issues

**"Module not found" errors:**
```bash
# Make sure you've activated the virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**"API key not configured" errors:**
- Check that your `.env` file exists in the `backend/` directory
- Ensure you've set either `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
- Make sure `LLM_PROVIDER` matches your API key provider

**Database errors:**
- Delete `eazyhealth.db` and restart the server to recreate the database

### Frontend Issues

**"Cannot connect to backend" errors:**
- Ensure the backend is running on port 8000
- Check that you're accessing the frontend at `http://localhost:5173`
- Verify CORS settings in `backend/app/config.py`

**Build errors:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## License

This project is for educational purposes. Please add appropriate licensing before deploying to production.

---

## Contributing

Contributions are welcome! Please ensure:
1. Code follows existing style conventions
2. All tests pass
3. New features include appropriate disclaimers
4. Medical information is accurate and from trusted sources

---

## Contact

For questions or issues, please open a GitHub issue.

---

**Remember: This is an educational tool. Always consult healthcare professionals for medical advice.**
