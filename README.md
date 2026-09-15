# 🧠 Smart Retail Query and Alert System for Apparel & Footwear Using Gen AI

## 📌 Project Overview
The **Smart Retail Query and Alert System** is an AI-powered solution designed for apparel and footwear retail businesses.  
It enables users to interact with retail data using natural language and provides intelligent insights along with real-time alerts.

This system aims to improve:
- Inventory management
- Sales monitoring
- Decision-making efficiency

---

## 🎯 Objectives
- Enable natural language-based querying of retail data  
- Provide real-time alerts for inventory and sales  
- Deliver intelligent insights using Generative AI  

---

## 🚀 Key Features

### 💬 Natural Language Query System
- Users can ask queries like:
  - "Show low stock products"
  - "Top selling footwear this week"
- System processes queries and returns relevant results

### 🚨 Alert System
- Low stock alerts  
- High demand alerts  
- Slow-moving product alerts  

### 📊 Data Insights
- Sales trends analysis  
- Inventory status monitoring  
- Product performance insights  

---




## 📄 Use Case

This system can be used by:
- Retail store managers  
- Inventory analysts  
- Business decision-makers  

---


## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub!

# 🛍️ Smart Retail AI Alert System

An AI-powered fashion recommendation and retail assistant built using **Python, Flask, SQLite, Ollama, and Phi-3 Mini**.

The application allows users to describe their fashion requirements in natural language or select preferences through a form. The system extracts preferences such as color, style, budget, and occasion, stores them as user memory, and uses a locally running AI model to generate personalized fashion recommendations.

---

## 🚀 Project Overview

The **Smart Retail AI Alert System** is a web-based AI fashion assistant designed for apparel and footwear retail scenarios.

The system combines:

- Natural-language user queries
- Preference extraction
- Persistent user memory
- AI-powered recommendations
- Chat history
- Local Large Language Model (LLM)
- SQLite database
- Flask web application

The application uses **Phi-3 Mini**, running locally through **Ollama**, to generate fashion recommendations.

---

## ✨ Features

### 👕 AI Fashion Recommendations

Users can enter queries such as:

> "Suggest a black casual outfit for office."

The AI generates:

- Recommended clothing items
- Accessories
- Fashion tips
- Outfit description
- Confidence level

---

### 🧠 Preference Memory

The application automatically extracts fashion preferences from user input.

Currently supported:

**Colors**
- Black
- White
- Blue
- Red
- Green
- Yellow
- Pink
- Grey

**Styles**
- Casual
- Formal
- Party
- Ethnic

**Budget**
- Low
- Medium
- High

**Occasions**
- Office
- Wedding
- Party
- Travel

These preferences are stored in SQLite and reused in future AI prompts.

---

### 💬 Chat History

Every request and AI response is stored in the database.

Users can access previous conversations through the:

`/history`

route.

---

### 📝 Two Input Methods

The application supports:

1. Natural-language chat input
2. Structured fashion preference form

Users can either type a complete request or select:

- Category
- Style
- Occasion
- Season
- Budget
- Color

---

### 🤖 Local AI

The application uses:

**Ollama + Phi-3 Mini**

The AI model runs locally instead of requiring a paid cloud AI API.

---

### 🛡️ AI Response Fallback

If the AI model fails or returns invalid JSON, the application provides a fallback recommendation instead of crashing.

---

## 🏗️ System Architecture

```text
                         USER
                           │
                           ▼
                ┌────────────────────┐
                │     FRONTEND       │
                │ HTML + Bootstrap   │
                │ Jinja Templates    │
                └─────────┬──────────┘
                          │
                       HTTP
                    GET / POST
                          │
                          ▼
                ┌────────────────────┐
                │       FLASK        │
                │      app.py        │
                │                    │
                │ Routes             │
                │ Business Logic     │
                │ Preference Memory  │
                │ AI Integration     │
                └──────┬─────┬───────┘
                       │     │
                       │     │
                 SQLite│     │Ollama
                       │     │
                       ▼     ▼
              ┌────────────┐ ┌──────────────┐
              │ fashion.db │ │    Ollama    │
              │            │ │              │
              │ chats      │ │ Phi-3 Mini   │
              │ memory     │ │              │
              └────────────┘ └──────┬───────┘
                                    │
                                    ▼
                              AI JSON Response
                                    │
                                    ▼
                               Flask Parsing
                                    │
                                    ▼
                              Jinja Template
                                    │
                                    ▼
                                 Browser
