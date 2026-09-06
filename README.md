# PRPCEM STUDENT ASSISTANT

### AI-Powered Student Assistance & Complaint Resolution System

PRPCEM Student Assistant is a domain-specific AI-based web application designed to provide students with quick college-related information and simplify the complaint registration process.

The system provides two main services:

- 🤖 **AI Chatbot** – Answers PRPCEM-related queries.
- 📝 **AI Complaint Assistant** – Understands a student's complaint, identifies its category, asks relevant questions, determines priority, and stores the complaint.

---

## 🎯 Problem Statement

Students frequently need information about college departments, facilities, examinations and other campus-related services. They may also face problems related to laboratories, faculty, infrastructure, library, transportation and other areas.

Traditional complaint systems may require students to manually select categories and provide information in a fixed format.

PRPCEM Student Assistant provides a conversational interface where students can describe their queries and complaints naturally.

---

## 💡 Objectives

- Develop an AI-based student assistance system.
- Provide quick answers to PRPCEM-related queries.
- Process student input written in natural language.
- Automatically identify complaint categories.
- Ask category-specific follow-up questions.
- Determine complaint priority.
- Store structured complaint information.
- Provide a simple and user-friendly interface.

---

## 🤖 AI Concepts Used

### 1. Natural Language Processing (NLP)

The system processes natural-language text entered by students and identifies relevant words and phrases.

### 2. Intent Detection

The chatbot identifies the intent behind a student's query and provides an appropriate response.

### 3. Rule-Based Reasoning

Predefined rules are used to classify complaints and determine their priority.

### 4. Knowledge Representation

College-related information is represented in a structured JSON knowledge base.

### 5. Decision Making

The Complaint Assistant makes decisions regarding complaint category, follow-up questions and priority.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────────┐
                    │        STUDENT          │
                    └────────────┬────────────┘
                                 │
                                 ▼
              ┌──────────────────────────────────┐
              │      PRPCEM STUDENT ASSISTANT    │
              │          Web Interface           │
              └───────────────┬──────────────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        ┌─────────────────┐       ┌────────────────────┐
        │   AI CHATBOT    │       │ COMPLAINT ASSISTANT│
        └────────┬────────┘       └──────────┬─────────┘
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐       ┌────────────────────┐
        │ Intent Detection│       │ Complaint Category │
        │ & NLP Processing│       │    Detection       │
        └────────┬────────┘       └──────────┬─────────┘
                 │                           │
                 ▼                           ▼
        ┌─────────────────┐       ┌────────────────────┐
        │ Knowledge Base  │       │ Relevant Questions │
        │     (JSON)      │       └──────────┬─────────┘
        └────────┬────────┘                  │
                 │                           ▼
                 ▼                  ┌────────────────────┐
        ┌─────────────────┐         │ Priority Detection │
        │  AI Response    │         └──────────┬─────────┘
        └─────────────────┘                    │
                                              ▼
                                   ┌────────────────────┐
                                   │ SQLite Database    │
                                   │ Complaint Storage   │
                                   └────────────────────┘
