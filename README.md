# PRPCEM STUDENT ASSISTANT

AI-powered student assistance and complaint-support web application for **P. R. Pote Patil College of Engineering & Management, Amravati**.

## Features

- College-specific student chatbot
- Domain restriction for unrelated questions
- AI-style complaint category detection
- Category-specific dynamic questions
- Complaint priority scoring
- Complaint ID generation
- Responsive college-themed interface

## AI Concepts

- Natural Language Processing (NLP)
- Intent/category detection
- Rule-based reasoning
- Knowledge representation
- State-based complaint conversation
- Heuristic priority scoring

## Technology

- Python
- Flask
- HTML/CSS/JavaScript
- JSON knowledge base

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`

## Project Flow

Student → Chatbot OR Complaint Assistant → NLP/category detection → relevant questions → structured complaint.

## Future Scope

- Connect to a production LLM API
- Add database storage and complaint tracking
- Add authenticated student/admin accounts
- Add email/notification routing
- Expand the verified PRPCEM knowledge base
