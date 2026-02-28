# ShadowPrice_AI 🛒🤖
### AI-Powered Budget-Aware Grocery Optimization System

ShadowPrice_AI is an intelligent retail assistant that transforms natural-language grocery requests into optimized purchase recommendations using real-time online price data and AI-driven decision logic.

The system extracts structured shopping constraints (items, quantities, budget, currency, location), retrieves live Google Shopping listings, ranks viable candidates, and selects the best-value options while respecting user-defined budget constraints.

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

ShadowPrice_AI addresses this by combining structured AI extraction, real-time shopping search, and value-based optimization logic into a single automated pipeline.

---

## ⚙️ System Architecture

User Input (Natural Language)  
⬇  
Gemini Structured Extraction  
⬇  
SerpApi Google Shopping Retrieval  
⬇  
Candidate Cleaning & Ranking (Pandas)  
⬇  
AI-Based Best-Value Selection  
⬇  
Optimized Cart Output (HTML / JSON)

---

## 🧠 Core Capabilities

- Natural-language grocery interpretation  
- Automatic extraction of items, quantities, and constraints  
- Real-time Google Shopping search  
- AI-assisted best-option selection  
- Budget-aware filtering logic  
- Structured JSON API for integration  
- Web-based result visualization  
- Docker-ready cloud deployment  

---

## 📂 Project Structure

```
├── scrap_data.py # FastAPI application & API routes
├── AI_model.py # Gemini extraction + selection logic
├── functions.py # Shopping search + data processing utilities
├── index.html # Frontend interface
├── requirements.txt # Python dependencies
├── dockerfile # Container configuration
```



---
## 🛠 Technology Stack

Backend:
- FastAPI
- Uvicorn

Artificial Intelligence:
- Google Gemini API

Data Retrieval:
- SerpApi (Google Shopping API)

Data Processing:
- Pandas

Deployment:
- Docker
- Google Cloud Run

---

## 🔌 API Endpoints

GET `/`  
Serves the web interface.

POST `/run`  
Returns formatted HTML results.

POST `/run-json`  
Returns structured JSON response:

```json
{
  "selected": [...],
  "total": 47.50,
  "constraints": {...},
  "candidates": [...],
  "ai_summary": "..."
}
```

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

https://shopping-assistant-32565067173.asia-southeast1.run.app/

---


🚀 Future Improvements

Knapsack-based full budget optimization

Caching layer for repeated searches using firebase

Multi-store comparison engine

Currency auto-detection

Mobile application integration

Inflation and affordability analytics dashboard

