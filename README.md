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
