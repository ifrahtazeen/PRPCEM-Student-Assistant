from flask import Flask, render_template, request, jsonify
import json
import uuid
import sqlite3
import re
from datetime import datetime


app = Flask(__name__)


# ==========================================
# LOAD COLLEGE KNOWLEDGE BASE
# ==========================================

with open("data/knowledge.json", "r", encoding="utf-8") as file:
    KNOWLEDGE = json.load(file)


# ==========================================
# DATABASE
# ==========================================

DB_NAME = "complaints.db"


def init_database():
    connection = sqlite3.connect(DB_NAME)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            answers TEXT,
            priority TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


init_database()


# ==========================================
# CHATBOT - INTENT DETECTION
# ==========================================

def detect_intent(message):

    text = message.lower()

    intent_keywords = {

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
            "classroom",
            "laboratory",
            "lab",
            "auditorium",
            "sports",
            "hostel"
        ],

        "aiml": [
            "aiml",
            "ai ml",
            "machine learning",
            "artificial intelligence"
        ],

        "examination": [
            "exam",
            "examination",
            "timetable",
            "result",
            "marks",
            "hall ticket",
            "paper"
        ],

        "college": [
            "college name",
            "college",
            "prpcem",
            "pote patil",
            "full name",
            "about college"
        ]
    }

    # Score each possible intent
    scores = {}

    for intent, keywords in intent_keywords.items():

        scores[intent] = sum(
            1 for keyword in keywords
            if keyword in text
        )

    best_intent = max(
        scores,
        key=scores.get
    )

    if scores[best_intent] == 0:
        return "unknown"

    return best_intent


def chatbot_answer(message):

    intent = detect_intent(message)

    # --------------------------------------
    # COLLEGE
    # --------------------------------------

    if intent == "college":

        return (
            "P. R. Pote Patil College of Engineering & "
            "Management, Amravati (PRPCEM)."
        )


    # --------------------------------------
    # DEPARTMENTS
    # --------------------------------------

    if intent == "departments":

        departments = KNOWLEDGE["departments"]

        answer = (
            "PRPCEM has the following engineering "
            "departments:\n\n"
        )

        for i, department in enumerate(
            departments,
            1
        ):

            answer += (
                f"{i}. {department}\n"
            )

        return answer


    # --------------------------------------
    # FACILITIES
    # --------------------------------------

    if intent == "facilities":

        facilities = KNOWLEDGE["facilities"]

        answer = (
            "PRPCEM provides facilities such as:\n\n"
        )

        for facility in facilities:

            answer += (
                f"• {facility}\n"
            )

        return answer


    # --------------------------------------
    # AIML
    # --------------------------------------

    if intent == "aiml":

        return (
            "CSE (AIML) is one of the engineering "
            "departments at PRPCEM. It focuses on "
            "Computer Science, Artificial Intelligence "
            "and Machine Learning."
        )


    # --------------------------------------
    # EXAMINATION
    # --------------------------------------

    if intent == "examination":

        return (
            "For examination-related information, "
            "students should refer to the official "
            "PRPCEM examination resources. I can help "
            "with general examination queries available "
            "in my knowledge base."
        )


    # --------------------------------------
    # UNKNOWN
    # --------------------------------------

    return (
        "I'm PRPCEM Student Assistant. 🤖\n\n"
        "I can help only with PRPCEM-related questions "
        "such as departments, programs, facilities, "
        "examinations and student support."
    )


# ==========================================
# COMPLAINT INPUT VALIDATION
# ==========================================

def is_meaningful_complaint(description):

    text = description.strip()

    # Empty or very short input
    if len(text) < 8:
        return False

    # Remove extra spaces
    words = re.findall(r"[A-Za-z]+", text.lower())

    # Need at least 2 actual words
    if len(words) < 2:
        return False

    # Reject strings containing very little alphabetic content
    letters = re.findall(r"[A-Za-z]", text)

    if len(letters) < 5:
        return False

    if len(letters) / max(len(text), 1) < 0.45:
        return False

    # Common meaningless/random inputs
    invalid_inputs = {
        "asdf",
        "asdfgh",
        "asdfghjkl",
        "qwerty",
        "qwertyuiop",
        "zxcvbnm",
        "abc",
        "abcd",
        "abcde",
        "abcdef",
        "xyz",
        "xyza",
        "test",
        "testing",
        "random",
        "blah",
        "blahblah",
        "dgdgd",
        "dgdgdgd"
    }

    cleaned_words = "".join(words)

    for invalid in invalid_inputs:
        if cleaned_words == invalid:
            return False

    # Detect obvious repeated/random patterns
    unique_letters = set(cleaned_words)

    if len(cleaned_words) >= 5:
        if len(unique_letters) <= 2:
            return False

    # Complaint/context words.
    # These help recognize meaningful Hinglish/English complaints.
    meaningful_context_words = [

        # General complaint words
        "complaint",
        "issue",
        "problem",
        "trouble",
        "concern",
        "not",
        "working",
        "wrong",
        "broken",
        "bad",
        "poor",
        "need",
        "help",
        "please",
        "report",

        # Faculty / academic
        "faculty",
        "teacher",
        "professor",
        "sir",
        "madam",
        "hod",
        "subject",
        "class",
        "lecture",
        "treat",
        "treated",
        "treating",
        "behavior",
        "behaviour",
        "rude",
        "misbehave",
        "attendance",
        "marks",

        # Infrastructure
        "fan",
        "light",
        "electricity",
        "power",
        "switch",
        "socket",
        "classroom",
        "building",
        "bench",
        "chair",
        "ac",

        # Laboratory
        "lab",
        "laboratory",
        "computer",
        "projector",
        "equipment",
        "printer",
        "machine",
        "practical",

        # Water / sanitation
        "water",
        "washroom",
        "toilet",
        "tap",
        "sanitation",
        "clean",
        "dirty",
        "leakage",

        # Examination
        "exam",
        "examination",
        "paper",
        "result",
        "timetable",
        "marksheet",
        "hall",
        "ticket",
        "revaluation",

        # Administrative
        "office",
        "admission",
        "certificate",
        "document",
        "form",
        "fees",
        "fee",
        "scholarship",
        "id",

        # Library
        "library",
        "book",
        "librarian",
        "reading",

        # Canteen
        "canteen",
        "food",
        "meal",

        # Transportation
        "bus",
        "transport",
        "route",
        "driver",
        "conductor",

        # Safety
        "ragging",
        "harassment",
        "bullying",
        "bully",
        "threat",
        "unsafe",
        "safety",
        "abuse",

        # Common Hinglish words
        "mujhe",
        "mere",
        "meri",
        "mera",
        "faculty",
        "nhi",
        "nahi",
        "kar",
        "rahi",
        "raha",
        "hai",
        "issue",
        "problem"
    ]

    # If complaint contains known meaningful context,
    # consider it valid.
    if any(
        word in words
        for word in meaningful_context_words
    ):
        return True

    # For unknown complaints, require at least 3 words.
    # This allows genuine sentences to reach "Other"
    # while rejecting short random text.
    if len(words) >= 3:
        return True

    return False


# ==========================================
# COMPLAINT CATEGORY DETECTION
# ==========================================

def detect_category(description):

    text = description.lower().strip()

    categories = {

        "Laboratory / Equipment": [
            "projector",
            "laboratory",
            "lab",
            "computer",
            "pc",
            "equipment",
            "printer",
            "machine",
            "practical"
        ],

        "Water / Sanitation": [
            "water",
            "tap",
            "washroom",
            "toilet",
            "leakage",
            "sanitation",
            "dirty",
            "cleanliness"
        ],

        "Electrical / Infrastructure": [
            "electricity",
            "light",
            "fan",
            "ac",
            "air conditioner",
            "socket",
            "power",
            "switch",
            "classroom",
            "building",
            "bench",
            "chair",
            "infrastructure"
        ],

        "Faculty / Academic": [
            "faculty",
            "teacher",
            "professor",
            "sir",
            "madam",
            "hod",
            "lecture",
            "subject",
            "class",
            "treat",
            "treated",
            "treating",
            "behavior",
            "behaviour",
            "rude",
            "misbehave",
            "misbehaved",
            "academic",
            "attendance",
            "marks",
            "teaching"
        ],

        "Examination": [
            "exam",
            "examination",
            "marks",
            "result",
            "timetable",
            "hall ticket",
            "paper",
            "marksheet",
            "revaluation"
        ],

        "Administrative": [
            "office",
            "id card",
            "admission",
            "certificate",
            "fees",
            "fee",
            "document",
            "form",
            "scholarship"
        ],

        "Library": [
            "library",
            "book",
            "librarian",
            "reading room"
        ],

        "Canteen": [
            "canteen",
            "food",
            "meal",
            "hygiene"
        ],

        "Transportation": [
            "bus",
            "transport",
            "vehicle",
            "route",
            "driver",
            "conductor"
        ],

        "Ragging / Harassment / Safety": [
            "ragging",
            "harassment",
            "harass",
            "bullying",
            "bully",
            "threat",
            "unsafe",
            "safety",
            "abuse"
        ]
    }

    # Score categories
    scores = {}

    for category, keywords in categories.items():

        score = 0

        for keyword in keywords:

            # For multi-word phrases, use direct matching.
            if " " in keyword:

                if keyword in text:
                    score += 1

            # For single words, check complete words.
            else:

                if re.search(
                    r"\b" + re.escape(keyword) + r"\b",
                    text
                ):
                    score += 1

        scores[category] = score

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:

        return "Other"

    return best_category


# ==========================================
# DYNAMIC QUESTIONS
# ==========================================

QUESTION_RULES = {

    "Laboratory / Equipment": [

        "Which department is this laboratory related to?",

        "Which floor is the laboratory located on?",

        "What is the laboratory or room number?",

        "What equipment is affected and what exactly is the problem?",

        "Since when has the problem been occurring?"
    ],

    "Water / Sanitation": [

        "Which building or block is affected?",

        "Which floor and washroom is affected?",

        "What exactly is the water or sanitation problem?",

        "Since when has the problem been occurring?"
    ],

    "Electrical / Infrastructure": [

        "Where is the problem located? Please enter building, floor or room.",

        "Which electrical equipment or infrastructure is affected?",

        "What exactly is the problem?",

        "Since when has the problem been occurring?"
    ],

    "Faculty / Academic": [

        "What is the faculty member's name?",

        "Which department and subject are involved?",

        "When did the incident or problem occur?",

        "Please describe the issue clearly."
    ],

    "Examination": [

        "Which examination or subject is this related to?",

        "Which semester/year are you in?",

        "What exactly is the examination-related issue?",

        "When did you notice the issue?"
    ],

    "Administrative": [

        "Which office or administrative service is involved?",

        "Which semester/year are you in?",

        "What document, form or service is involved?",

        "Please describe the issue clearly."
    ],

    "Library": [

        "Which library service or book is involved?",

        "What exactly is the problem?",

        "When did the issue occur?"
    ],

    "Canteen": [

        "What is the canteen-related issue?",

        "When and where did it occur?",

        "Please provide any additional useful details."
    ],

    "Transportation": [

        "Which route or bus is involved?",

        "What exactly is the transportation issue?",

        "When did it occur?"
    ],

    "Ragging / Harassment / Safety": [

        "When and where did the incident occur?",

        "Please describe what happened in factual terms.",

        "Who or what group was involved, if known?",

        "Do you currently feel unsafe or require immediate assistance?"
    ],

    "Other": [

        "Which department or area is this related to?",

        "Where did the issue occur?",

        "When did it occur?",

        "Please provide any other details needed to understand the problem."
    ]
}


# ==========================================
# PRIORITY DETECTION
# ==========================================

def calculate_priority(
    category,
    description,
    answers
):

    complete_text = (
        description
        + " "
        + " ".join(answers)
    ).lower()

    # Safety complaints
    if category == "Ragging / Harassment / Safety":

        return "HIGH"

    # Emergency situations
    if any(
        word in complete_text
        for word in [
            "danger",
            "unsafe",
            "emergency",
            "threat"
        ]
    ):

        return "HIGH"

    # Important technical issues
    if any(
        word in complete_text
        for word in [
            "not working",
            "many students",
            "whole class",
            "entire lab",
            "urgent"
        ]
    ):

        return "MEDIUM"

    return "LOW"


# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================
# CHATBOT PAGE
# ==========================================

@app.route("/chatbot")
def chatbot():

    return render_template(
        "chatbot.html"
    )


# ==========================================
# COMPLAINT PAGE
# ==========================================

@app.route("/complaint")
def complaint():

    return render_template(
        "complaint.html"
    )


# ==========================================
# CHATBOT API
# ==========================================

@app.route(
    "/api/chat",
    methods=["POST"]
)
def chat():

    data = request.get_json() or {}

    message = data.get(
        "message",
        ""
    ).strip()

    if not message:

        return jsonify({
            "reply": "Please enter a question."
        })

    response = chatbot_answer(
        message
    )

    return jsonify({
        "reply": response
    })


# ==========================================
# ANALYZE COMPLAINT
# ==========================================

@app.route(
    "/api/analyze-complaint",
    methods=["POST"]
)
def analyze_complaint():

    data = request.get_json() or {}

    description = data.get(
        "description",
        ""
    ).strip()

    # --------------------------------------
    # CHECK EMPTY INPUT
    # --------------------------------------

    if not description:

        return jsonify({
            "error": "Please describe your complaint."
        }), 400


    # --------------------------------------
    # VALIDATE COMPLAINT
    # --------------------------------------

    if not is_meaningful_complaint(description):

        return jsonify({
            "error": (
                "Please enter a meaningful complaint "
                "describing your actual issue."
            )
        }), 400


    # --------------------------------------
    # DETECT CATEGORY
    # --------------------------------------

    category = detect_category(
        description
    )


    # --------------------------------------
    # GET CATEGORY QUESTIONS
    # --------------------------------------

    questions = QUESTION_RULES.get(
        category,
        QUESTION_RULES["Other"]
    )


    return jsonify({

        "category": category,

        "questions": questions

    })


# ==========================================
# SUBMIT + SAVE COMPLAINT
# ==========================================

@app.route(
    "/api/submit-complaint",
    methods=["POST"]
)
def submit_complaint():

    data = request.get_json() or {}

    category = data.get(
        "category",
        "Other"
    )

    description = data.get(
        "description",
        ""
    ).strip()

    answers = data.get(
        "answers",
        []
    )


    if not description:

        return jsonify({
            "error": "Complaint description is required."
        }), 400


    # --------------------------------------
    # VALIDATE AGAIN BEFORE SAVING
    # --------------------------------------

    if not is_meaningful_complaint(description):

        return jsonify({
            "error": (
                "Invalid complaint. "
                "Please provide meaningful details."
            )
        }), 400


    priority = calculate_priority(
        category,
        description,
        answers
    )


    complaint_id = (
        "PRPCEM-"
        + str(uuid.uuid4())[:8].upper()
    )


    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    # SAVE TO SQLITE
    connection = sqlite3.connect(
        DB_NAME
    )


    connection.execute("""
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
        json.dumps(
            answers,
            ensure_ascii=False
        ),
        priority,
        created_at
    ))


    connection.commit()
    connection.close()


    return jsonify({

        "success": True,

        "complaint_id": complaint_id,

        "category": category,

        "priority": priority

    })


# ==========================================
# GET SAVED COMPLAINTS
# ==========================================

@app.route(
    "/api/complaints",
    methods=["GET"]
)
def get_complaints():

    connection = sqlite3.connect(
        DB_NAME
    )

    connection.row_factory = sqlite3.Row

    rows = connection.execute("""
        SELECT
            complaint_id,
            description,
            category,
            priority,
            created_at
        FROM complaints
        ORDER BY id DESC
    """).fetchall()

    connection.close()


    complaints = [
        dict(row)
        for row in rows
    ]


    return jsonify({
        "complaints": complaints
    })


# ==========================================
# START APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(
        debug=True
    )