from flask import Flask, render_template, request, jsonify
import json
import sqlite3
import uuid
import re
from datetime import datetime


app = Flask(__name__)

# ---------------------------------------------------------
# LOAD KNOWLEDGE BASE
# ---------------------------------------------------------

with open("data/knowledge.json", "r", encoding="utf-8") as file:
    KNOWLEDGE = json.load(file)


# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------

DB_NAME = "complaints.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT UNIQUE,
            description TEXT,
            category TEXT,
            answers TEXT,
            priority TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


# ---------------------------------------------------------
# CHATBOT - INTENT DETECTION
# ---------------------------------------------------------

def detect_intent(message):
    text = message.lower().strip()

    intents = {
         "introduction" :[
            "hello",
            "hi",
            "namaste",
            "welcome"
        ],
        
        "departments": [
            "department",
            "departments",
            "branch",
            "branches",
            "course",
            "courses",
            "program",
            "programs",
            "stream",
            "streams"
        ],

        "facilities": [
            "facility",
            "facilities",
            "library",
            "canteen",
            "transport",
            "transportation",
            "classroom",
            "classrooms",
            "lab",
            "labs",
            "laboratory",
            "auditorium",
            "sports",
            "hostel",
            "wifi",
            "campus"
        ],

        "aiml": [
            "aiml",
            "ai ml",
            "ai and ml",
            "artificial intelligence",
            "machine learning",
            "ai/ml"
        ],

        "examination": [
            "exam",
            "examination",
            "exams",
            "timetable",
            "time table",
            "result",
            "results",
            "marks",
            "hall ticket",
            "question paper",
            "paper",
            "semester exam"
        ],

        "documents": [
            "bonafide",
            "bonafide certificate",
            "bonafide certificate",
            "certificate",
            "certificates",
            "document",
            "documents",
            "tc",
            "transfer certificate",
            "leaving certificate",
            "lc",
            "application",
            "issue certificate",
            "student certificate"
        ],

        "college": [
            "college name",
            "college",
            "prpcem",
            "pote patil",
            "p r pote",
            "full name",
            "about college"
            "what is prpcem"
            "pr. pote patil college"
            "tell me about college"
        ]
    }

    scores = {}

    for intent, keywords in intents.items():
        score = 0

        for keyword in keywords:

            # Phrase matching
            if " " in keyword or "/" in keyword:
                if keyword in text:
                    score += 2

            # Single word matching
            else:
                if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                    score += 1

        scores[intent] = score

    best_intent = max(scores, key=scores.get)

    if scores[best_intent] == 0:
        return "unknown"

    return best_intent


# ---------------------------------------------------------
# CHATBOT RESPONSE
# ---------------------------------------------------------

def chatbot_answer(intent):

    if intent == "introduction":

        return (
            "Hey!👋"
            "I'm the PRPCEM Student Assistant. Ask me anything related to the college."
        )
    elif intent == "college":

        return (
            "🏫 P. R. Pote Patil College of Engineering and Management, Amravati was established in 2008 on a 10-acre campus."
            "It provides quality education through various UG, PG, MBA and MCA programmes"
            "The college focuses on developing skilled and versatile engineers for the competitive industry."
        )

    elif intent == "departments":

        departments = KNOWLEDGE.get("departments", [])

        if isinstance(departments, list):
            department_text = "\n".join(
                [f"• {department}" for department in departments]
            )

            return (
                "📚 PRPCEM offers the following departments/programs:\n\n"
                + department_text
            )

        return (
            "📚 PRPCEM offers multiple engineering and management "
            "programs. Please contact the college for complete details."
        )

    elif intent == "facilities":

        facilities = KNOWLEDGE.get("facilities", [])

        if isinstance(facilities, list):
            facility_text = "\n".join(
                [f"• {facility}" for facility in facilities]
            )

            return (
                "🏫 Some facilities available at PRPCEM include:\n\n"
                + facility_text
            )

        return (
            "The PRPCEM has modern facilities including smart classrooms, Wi-Fi, laboratories, digital library and auditorium."
        )

    elif intent == "aiml":

        return (
            "🤖 The Department of Computer Science & Engineering (AIML)"
            " is a specialized branch within Computer Science and Engineering "
            "focuses on the principles and applications of Artificial Intelligence (AI) "
            "and Machine Learning (ML). It offers a comprehensive curriculum that includes "
            "foundational Computer Science courses alongside specialized AI and ML topics, "
            "preparing students for careers in academia, industry, and research. "
        )

    elif intent == "examination":

        return (
            "📝 For examination-related information/queries, please contact to the COE office(2nd floor, Main Building). "
        )

    elif intent == "documents":

        return (
            "📄 For any documents related queries you can visit Reception Desk/Fee Section/ Scholarship Section, "
            " Or you can contact to your designated departmental coordinator/HOD  "
        )

    else:

        return (
            "I'm PRPCEM Student Assistant. 🤖\n\n"
            "I can help only with PRPCEM-related questions / queries.\n\n"
            "If my answer/response doesn't help/meet to resolve your query / question. "
            " So, you can visit to college official website or contact/report directly to the college! "
        )


# ---------------------------------------------------------
# COMPLAINT VALIDATION
# ---------------------------------------------------------

def is_meaningful_complaint(text):

    text = text.strip()

    # Too short
    if len(text) < 8:
        return False

    # Extract alphabetic words
    words = re.findall(r"[A-Za-z]+", text)

    if len(words) < 2:
        return False

    # At least 5 alphabetic characters
    letters = re.findall(r"[A-Za-z]", text)

    if len(letters) < 5:
        return False

    # Alphabetic character ratio
    alpha_ratio = len(letters) / max(len(text), 1)

    if alpha_ratio < 0.45:
        return False

    # Reject obvious random strings
    random_strings = {
        "dgdgd",
        "asdf",
        "asdfgh",
        "qwerty",
        "qwertyui",
        "abcabc",
        "testtest",
        "xxxxx",
        "aaaaaa",
        "bbbbbb",
        "hhhhhh",
        "lolol",
        "random"
    }

    normalized = re.sub(r"[^a-z]", "", text.lower())

    if normalized in random_strings:
        return False

    # Very low character diversity
    if len(normalized) >= 5 and len(set(normalized)) <= 2:
        return False

    # Common meaningful context words
    meaningful_words = {
        "problem",
        "issue",
        "complaint",
        "not",
        "working",
        "work",
        "broken",
        "damage",
        "damaged",
        "faculty",
        "teacher",
        "professor",
        "sir",
        "madam",
        "class",
        "classroom",
        "college",
        "lab",
        "laboratory",
        "projector",
        "computer",
        "equipment",
        "electricity",
        "light",
        "fan",
        "water",
        "washroom",
        "toilet",
        "exam",
        "examination",
        "marks",
        "attendance",
        "library",
        "book",
        "canteen",
        "food",
        "bus",
        "transport",
        "safety",
        "harassment",
        "ragging",
        "danger",
        "unsafe",
        "urgent",
        "office",
        "admin",
        "administration",
        "document",
        "certificate",
        "bonafide"
    }

    if any(word.lower() in meaningful_words for word in words):
        return True

    # If it contains 3 or more normal words, accept it
    if len(words) >= 3:
        return True

    return False


# ---------------------------------------------------------
# COMPLAINT CATEGORY DETECTION
# ---------------------------------------------------------

def detect_category(text):

    text = text.lower()

    categories = {

        "Laboratory / Equipment": [
            "lab",
            "laboratory",
            "projector",
            "computer",
            "equipment",
            "machine",
            "instrument",
            "printer",
            "ac",
            "air conditioner"
        ],

        "Water / Sanitation": [
            "water",
            "washroom",
            "toilet",
            "sanitation",
            "tap",
            "drinking water",
            "leakage",
            "dirty washroom",
            "cleaning"
        ],

        "Electrical / Infrastructure": [
            "electricity",
            "electrical",
            "light",
            "fan",
            "switch",
            "socket",
            "power",
            "building",
            "classroom",
            "bench",
            "door",
            "window",
            "infrastructure"
        ],

        "Faculty / Academic": [
            "faculty",
            "teacher",
            "professor",
            "sir",
            "madam",
            "teaching",
            "attendance",
            "marks",
            "academic",
            "behavior",
            "behaviour",
            "rude",
            "misbehave",
            "misbehaved",
            "treat",
            "treated",
            "treating"
        ],

        "Examination": [
            "exam",
            "examination",
            "timetable",
            "hall ticket",
            "question paper",
            "result",
            "marksheet",
            "marks"
        ],

        "Administrative": [
            "admin",
            "administration",
            "office",
            "admission",
            "document",
            "certificate",
            "bonafide",
            "fee",
            "fees",
            "form",
            "application"
        ],

        "Library": [
            "library",
            "book",
            "books",
            "issue book",
            "return book"
        ],

        "Canteen": [
            "canteen",
            "food",
            "meal",
            "snacks",
            "hygiene food"
        ],

        "Transportation": [
            "bus",
            "transport",
            "transportation",
            "route",
            "driver",
            "bus stop"
        ],

        "Ragging / Harassment / Safety": [
            "ragging",
            "harassment",
            "harass",
            "threat",
            "danger",
            "unsafe",
            "safety",
            "bullying",
            "abuse",
            "fight"
        ]
    }

    scores = {}

    for category, keywords in categories.items():

        score = 0

        for keyword in keywords:

            if " " in keyword:
                if keyword in text:
                    score += 2

            else:
                if re.search(r"\b" + re.escape(keyword) + r"\b", text):
                    score += 1

        scores[category] = score

    best_category = max(scores, key=scores.get)

    if scores[best_category] == 0:
        return "Other"

    return best_category


# ---------------------------------------------------------
# FOLLOW-UP QUESTIONS
# ---------------------------------------------------------

QUESTION_RULES = {

    "Laboratory / Equipment": [
        "Which department is this related to?",
        "Which lab, room or floor is affected?",
        "What equipment or problem is involved?",
        "Since when has the problem been occurring?"
    ],

    "Water / Sanitation": [
        "Which building, block or floor is affected?",
        "Is it related to a washroom, drinking water or another area?",
        "Please describe the exact problem.",
        "Since when has the problem been occurring?"
    ],

    "Electrical / Infrastructure": [
        "Where is the problem located?",
        "Which equipment or infrastructure is affected?",
        "Please describe the exact problem.",
        "Since when has the problem been occurring?"
    ],

    "Faculty / Academic": [
        "What is the faculty member's name?",
        "Which department or subject is involved?",
        "When did the issue occur?",
        "Please describe the issue clearly."
    ],

    "Examination": [
        "Which exam or subject is involved?",
        "Which semester or year are you in?",
        "What exactly is the examination-related issue?",
        "When did you notice the issue?"
    ],

    "Administrative": [
        "Which office or service is involved?",
        "Which semester or year are you in?",
        "Which document, form or service is related to the issue?",
        "Please describe the issue clearly."
    ],

    "Library": [
        "Which library service or book is involved?",
        "What exactly is the problem?",
        "When did you notice the issue?"
    ],

    "Canteen": [
        "What is the issue with the canteen service or food?",
        "When and where did the issue occur?",
        "Please provide any additional details."
    ],

    "Transportation": [
        "Which bus or route is involved?",
        "What exactly is the transportation issue?",
        "When did the issue occur?"
    ],

    "Ragging / Harassment / Safety": [
        "What is the date and location of the incident?",
        "Please provide a factual description of what happened.",
        "If known, who or which group was involved?",
        "Are you currently unsafe or in need of immediate assistance?"
    ],

    "Other": [
        "Which department or area is related to the complaint?",
        "Where did the issue occur?",
        "When did the issue occur?",
        "Please provide any additional details."
    ]
}


# ---------------------------------------------------------
# PRIORITY DETECTION
# ---------------------------------------------------------

def calculate_priority(text, category):

    text = text.lower()

    high_priority_words = [
        "danger",
        "dangerous",
        "unsafe",
        "emergency",
        "threat",
        "ragging",
        "harassment",
        "bullying",
        "abuse",
        "safety"
    ]

    medium_priority_words = [
        "not working",
        "doesn't work",
        "does not work",
        "many students",
        "whole class",
        "entire class",
        "entire lab",
        "all students",
        "urgent",
        "broken",
        "major problem"
    ]

    for word in high_priority_words:
        if word in text:
            return "HIGH"

    if category == "Ragging / Harassment / Safety":
        return "HIGH"

    for word in medium_priority_words:
        if word in text:
            return "MEDIUM"

    return "LOW"


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------------------------------------------------
# CHATBOT PAGE
# ---------------------------------------------------------

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


# ---------------------------------------------------------
# COMPLAINT PAGE
# ---------------------------------------------------------

@app.route("/complaint")
def complaint():
    return render_template("complaint.html")


# ---------------------------------------------------------
# CHATBOT API
# ---------------------------------------------------------

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "reply": "Please enter a question."
        })

    intent = detect_intent(message)

    response = chatbot_answer(intent)

    return jsonify({
        "reply": response,
        "intent": intent
    })


# ---------------------------------------------------------
# ANALYZE COMPLAINT API
# ---------------------------------------------------------

@app.route("/api/analyze-complaint", methods=["POST"])
def analyze_complaint():

    data = request.get_json(silent=True) or {}

    description = data.get("description", "").strip()

    if not description:
        return jsonify({
            "success": False,
            "error": "Please enter a complaint."
        }), 400

    if not is_meaningful_complaint(description):
        return jsonify({
            "success": False,
            "error": "Please enter a meaningful complaint with enough details."
        }), 400

    category = detect_category(description)

    priority = calculate_priority(
        description,
        category
    )

    questions = QUESTION_RULES.get(
        category,
        QUESTION_RULES["Other"]
    )

    return jsonify({
        "success": True,
        "category": category,
        "priority": priority,
        "questions": questions
    })


# ---------------------------------------------------------
# SUBMIT COMPLAINT API
# ---------------------------------------------------------

@app.route("/api/submit-complaint", methods=["POST"])
def submit_complaint():

    data = request.get_json(silent=True) or {}

    description = data.get("description", "").strip()
    category = data.get("category", "Other")
    answers = data.get("answers", [])
    priority = data.get("priority", "LOW")

    if not description:
        return jsonify({
            "success": False,
            "error": "Complaint description is required."
        }), 400

    if not is_meaningful_complaint(description):
        return jsonify({
            "success": False,
            "error": "Please enter a meaningful complaint."
        }), 400

    if not isinstance(answers, list):
        answers = []

    # Prevent empty follow-up answers
    if any(str(answer).strip() == "" for answer in answers):
        return jsonify({
            "success": False,
            "error": "Please answer all the questions before submitting."
        }), 400

    complaint_id = "PRPCEM-" + uuid.uuid4().hex[:8].upper()

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    answers_text = json.dumps(
        answers,
        ensure_ascii=False
    )

    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        INSERT INTO complaints
        (
            complaint_id,
            description,
            category,
            answers,
            priority,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        complaint_id,
        description,
        category,
        answers_text,
        priority,
        created_at
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "complaint_id": complaint_id,
        "category": category,
        "priority": priority,
        "message": "Complaint submitted successfully."
    })


# ---------------------------------------------------------
# VIEW COMPLAINTS API
# ---------------------------------------------------------

@app.route("/api/complaints", methods=["GET"])
def get_complaints():

    conn = sqlite3.connect(DB_NAME)

    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT
            complaint_id,
            description,
            category,
            answers,
            priority,
            created_at
        FROM complaints
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    complaints = []

    for row in rows:

        complaints.append({
            "complaint_id": row["complaint_id"],
            "description": row["description"],
            "category": row["category"],
            "answers": json.loads(row["answers"]),
            "priority": row["priority"],
            "created_at": row["created_at"]
        })

    return jsonify({
        "success": True,
        "complaints": complaints
    })


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
