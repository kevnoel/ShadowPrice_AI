# ShadowPrice_AI 🛒🤖
### AI-Powered Budget-Aware Grocery Optimization System

ShadowPrice_AI is an intelligent retail assistant that transforms natural-language grocery requests into optimized purchase recommendations using real-time online price data and AI-driven decision logic.

The system extracts structured shopping constraints (items, quantities, budget, currency, location), retrieves live Google Shopping listings, ranks viable candidates, and selects the best-value options while respecting user-defined budget constraints.

**KitaHack 2026** | **Team Magic Carp** | Universiti Malaya
**SDG 1: No Poverty** | Target 1.4

---

## 🌍 Live Deployments

Cloud API + Web Interface:  
https://shopping-assistant-32565067173.asia-southeast1.run.app/

Project Page (GitHub Pages):  
https://kevnoel.github.io/ShadowPrice_AI/

---

## 🎯 Problem Statement

Consumers frequently struggle with:
- Fragmented pricing across retailers  
- Difficulty identifying best value per unit  
- Budget limitations without clear price comparison  
- Rapid price fluctuations  

In Malaysia, a worker must work **58 minutes** to afford 1 litre of milk, compared to just 4 minutes in the Netherlands (UM SWRC). CPI is only updated monthly, missing daily price spikes that B40 households feel immediately. There is currently no tool that compares grocery prices across online stores in real time.

ShadowPrice_AI addresses this by combining structured AI extraction, real-time shopping search, and value-based optimization logic into a single automated pipeline.

---

## ⚙️ System Architecture

```
User Input (Natural Language, BM / EN / mixed)
        |
   [ Gemini 2.5 Flash ]       <-- Stage 1: NLP Extraction
   temp=0.0, JSON schema         Extracts items, qty, budget, location
        |
   [ SerpAPI Google Shopping ] <-- Per-item real-time price lookup
   gl="my", location-aware       10 candidates per item
        |
   [ Pandas Processing ]       <-- Clean prices, rank by unit cost
        |
   [ Gemini 2.5 Flash ]       <-- Stage 2: Smart Selection
   Budget-aware picking           1 best option per product
        |
   Optimized Cart Output (HTML / JSON)
```

---

## 🧠 Core Capabilities

- Natural-language grocery interpretation (BM, English, mixed)
- Automatic extraction of items, quantities, and constraints  
- Real-time Google Shopping search via SerpAPI
- AI-assisted best-option selection with budget awareness
- Structured JSON API for Flutter frontend integration  
- Web-based result visualization  
- Docker-ready cloud deployment on Google Cloud Run

---

## 🔧 Implementation Details

### Stage 1: NLP Extraction (`AI_model.py`)

- Gemini receives raw user text with a strict JSON schema enforced at API level
- `temperature: 0.0` for deterministic, reproducible output
- `response_mime_type: "application/json"` for native JSON response
- Extracts `items[]` (name, quantity, notes), `constraints` (budget, currency, location)
- `normalize_budget()` handles messy input like `"RM 50"`, `"50,000"`, etc.
- Defaults location to `"Malaysia"` when not specified

### Stage 2: Price Retrieval (`functions.py`)

- SerpAPI queries Google Shopping per item with `gl: "my"` (Malaysia)
- `to_money()` strips currency symbols, handles various number formats
- `top_n_per_product(n=10)` keeps only the 10 cheapest candidates per item
- Calculates `row_total = unit_price * quantity`, drops rows with missing prices

### Stage 3: AI Selection (`AI_model.py`)

- Candidate DataFrame sent to Gemini (payload truncated to 200K chars)
- Gemini picks ONE best option per product considering:
  - Price (primary factor)
  - Quality signals like rating and review count (tiebreaker)
  - Overall budget constraint (subset selection if budget is tight)
- Returns `selected[]` array and `total`

---

## 🧩 Google Technologies (8)

| Technology | Role |
|---|---|
| Gemini API | NLP extraction + smart product selection (2 calls per request) |
| Flutter | Mobile PWA frontend |
| Firebase Auth | Google sign-in |
| Firestore | NoSQL document store |
| Cloud Run | Auto-scaling container deployment |
| API Gateway | Request routing and rate limiting |
| Secret Manager | API key storage (Gemini, SerpAPI) |
| Cloud Tasks | Async job processing |

---

## 📂 Project Structure

```
├── scrap_data.py         # FastAPI application & API routes
├── AI_model.py           # Gemini extraction + selection logic
├── functions.py          # Shopping search + data processing utilities
├── index.html            # Frontend interface
├── requirements.txt      # Python dependencies
├── dockerfile            # Container configuration
├── backup/               # Earlier versions
└── LICENSE               # MIT
```

---

## 🛠 Technology Stack

**Backend:** FastAPI, Uvicorn  
**Artificial Intelligence:** Google Gemini API (2.5 Flash)  
**Data Retrieval:** SerpApi (Google Shopping API)  
**Data Processing:** Pandas  
**Deployment:** Docker, Google Cloud Run  

---

## 🔌 API Endpoints

GET `/`  
Serves the web interface.

POST `/run`  
Returns formatted HTML results.

POST `/run-json`  
Returns structured JSON response (for Flutter frontend):

```json
{
  "selected": [...],
  "total": 47.50,
  "constraints": {...},
  "candidates": [...],
  "ai_summary": "..."
}
```

---

## 🚧 Challenges Faced

### 1. AI Search Accuracy
Users got wrong products during testing. Someone typed "ayam" and got canned chicken rendang instead of fresh whole chicken. "Rice 5kg" returned basmati 1kg.

**Root cause:** Gemini returned short generic names like "chicken" which SerpAPI interpreted loosely.

**What we did:** Refined the prompt to extract very specific product names with exact quantities. Added the `notes` field for disambiguation (e.g. "fresh, whole" vs "canned"). This is still the hardest problem, and we're exploring adding a disambiguation step between extraction and search.

### 2. SerpAPI Rate Limits (250 calls/month)
Each request makes N SerpAPI calls (one per item). A 5-item list burns 5 calls. During user testing with 20 people, we hit limits and had to rotate API keys.

**What we did:** Limited candidates to top 10 per product. Set Gemini API budget cap at $20. Tracked usage carefully (55/250 after initial testing rounds).

### 3. No Bundle Comparison
Users wanted cheapest total from ONE store, not cheapest per-item spread across 5 different stores (multiple delivery fees). SerpAPI returns mixed sources, so grouping by store was tricky.

**What we did (post-feedback):** Grouped results by `source` field. Added basket total per store. Added delivery fee tracking.

### 4. Live Demo Latency
Full pipeline (Gemini call + SerpAPI * N items + Gemini selection) takes 10-15 seconds. For a 5-minute video demo, that's a lot of waiting.

**What we did:** Pre-typed demo queries. Used shorter grocery lists (2-3 items) for demo to reduce wait time.

### 5. Team Coordination and API Secrets
Three people across backend (Python/Cloud Run), frontend (Flutter), and infrastructure (Firebase). API keys needed to stay out of public repos.

**What we did:** Used Google Secret Manager for production keys. Environment variables for local dev. Added CORS middleware when Flutter needed to call Cloud Run backend. Ryan handled Docker deploys; Leo added `/run-json` endpoint for Flutter compatibility.

---

## 💻 Local Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set environment variables

Windows (PowerShell):

```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
$env:serpapi_shopping_api="YOUR_KEY"
```

Mac/Linux:

```bash
export GEMINI_API_KEY="YOUR_KEY"
export serpapi_shopping_api="YOUR_KEY"
```

### 3. Run the app

```bash
uvicorn scrap_data:app --reload --host 0.0.0.0 --port 8000
```

Open:

```
http://127.0.0.1:8000
```

---

## ☁ Cloud Deployment

Deployed on Google Cloud Run:

```bash
gcloud run deploy shopping-assistant --source . --region asia-southeast1
```

Live at: https://shopping-assistant-32565067173.asia-southeast1.run.app/

---

## 🚀 Future Roadmap

**Current (post-feedback iteration):**
- Refined Gemini prompts for better product extraction accuracy
- Bundle comparison: group results by store, show basket total
- Delivery fee tracking in price comparison
- Improved UI with AI Summary card and onboarding guide

**Next:**
- Firestore caching layer for repeated searches (reduce SerpAPI costs)
- Knapsack-based full budget optimization (replace greedy selection)
- Multi-store comparison engine
- Currency auto-detection
- Mobile application integration via Flutter
- Location-based pricing at neighborhood level
- Inflation and affordability analytics dashboard

---

## 👥 Team

| Member | Role | Stack |
|---|---|---|
| Leo (Leonal Sigar) | Frontend Lead | Flutter PWA, UI/UX |
| Ryan (Chadli Rayane) | Backend Lead | Python, Gemini, SerpAPI, Cloud Run |
| Kevin Noel | Strategy + Auth | Firebase, Firestore, Presentation |

---

## 📜 License

MIT License
