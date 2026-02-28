# ShadowPrice_AI 🛒🤖  
AI-Powered Smart Shopping Assistant with Budget Awareness

ShadowPrice_AI is an intelligent grocery assistant that converts natural language shopping requests into optimized purchase recommendations using real-time online prices and AI-based decision logic.

🔗 Live Deployments  
- Google Cloud Run (API + Web UI):  
  https://shopping-assistant-32565067173.asia-southeast1.run.app/

- GitHub Pages (Project Page):  
  https://kevnoel.github.io/ShadowPrice_AI/

---

## 🚀 What This Project Does

ShadowPrice_AI solves a real problem:

Consumers often don’t know which product gives the best value within their budget.

This system:
1. Extracts grocery items and constraints from natural language.
2. Searches live Google Shopping listings.
3. Uses AI (Gemini) to select the best-value product per item.
4. Ensures selections respect the user’s budget when possible.
5. Returns results in HTML or JSON format.

Example input:
> “I need 2 bags of rice and coffee under 50 ringgit in Malaysia”

---

## 🧠 How It Works (Pipeline)

User Text  
⬇  
Gemini Structured Extraction (items, quantity, budget, currency, location)  
⬇  
SerpApi Google Shopping Search  
⬇  
Candidate Data Processing (pandas ranking + cleaning)  
⬇  
Gemini Best-Option Selection  
⬇  
Final Optimized Cart Output  

---

## 📂 Project Structure
```
.
├── scrap_data.py        # FastAPI server + endpoints
├── AI_model.py          # Gemini extraction & decision logic
├── functions.py         # SerpApi search + dataframe utilities
├── index.html           # Simple frontend UI
├── requirements.txt     # Python dependencies
├── dockerfile           # Docker container config
```

---

## 🛠 Tech Stack

- FastAPI
- Google Gemini API
- SerpApi (Google Shopping API)
- Pandas
- Uvicorn
- Docker

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

https://shopping-assistant-32565067173.asia-southeast1.run.app/

---


