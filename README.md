🤖 PRPCEM Student Assistant

## AI-Powered Student Assistance & Complaint Resolution System

**PRPCEM Student Assistant** is an AI-based web application designed to help students with college-related queries and complaints.

The system provides an **AI Chatbot** for college information and a **Complaint Assistant** that analyzes student complaints and collects the required details.

---

## ✨ Features

### 🤖 AI Chatbot
- Answers PRPCEM-related questions
- Provides information about departments, programs and facilities
- Handles examination-related queries
- Uses a JSON knowledge base

### 📝 Complaint Assistant
- Accepts complaints in normal language
- Identifies the complaint category
- Determines complaint priority
- Asks relevant follow-up questions
- Generates a unique complaint ID
- Stores complaints using SQLite

---

## 🧠 AI Concepts Used

- **Natural Language Processing (NLP)**
- **Intent Detection**
- **Rule-Based Reasoning**
- **Knowledge Representation**
- **Decision Making**

---

## 📌 Complaint Categories

- Laboratory / Equipment
- Water / Sanitation
- Electrical / Infrastructure
- Faculty / Academic
- Examination
- Administrative
- Library
- Canteen
- Transportation
- Safety
- Other

---

## 🛠️ Technology Used

| Technology | Purpose |
|---|---|
| **Python** | Backend & AI Logic |
| **Flask** | Web Framework |
| **HTML/CSS/JavaScript** | Frontend |
| **JSON** | Knowledge Base |
| **SQLite** | Complaint Storage |
| **Gunicorn** | Deployment Server |

---

## 📂 Project Structure

```text
PRPCEM-Student-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
│   └── knowledge.json
│
├── static/
│   ├── style.css
│   └── college_logo.png
│
└── templates/
    ├── index.html
    ├── chatbot.html
    └── complaint.html


---

🔄 Working

Chatbot

User Question → Intent Detection → Knowledge Base → Response

Complaint Assistant

Complaint → Category Detection → Priority Detection → Follow-up Questions → Submission → Complaint ID


---

🚀 Future Scope

LLM integration

Multilingual support

Voice interaction

Admin dashboard

Complaint tracking

Email/SMS notifications



---

🌐 Live Demo

https://prpcem-student-assistant-1dx4.onrender.com

💻 GitHub Repository

https://github.com/ifrahtazeen/PRPCEM-Student-Assistant


---

👩‍💻 PRPCEM Student Assistant

AI-Powered Student Assistance & Complaint Resolution System
