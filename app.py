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

    text = message.lower().strip()

    intent_keywords = {

        # --------------------------------------
        # DEPARTMENTS
        # --------------------------------------

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
            "streams",
            "engineering branch",
            "engineering branches",
            "courses available",
            "branches available"
        ],

        # --------------------------------------
        # FACILITIES
        # --------------------------------------

        "facilities": [
            "facility",
            "facilities",
            "library",
            "canteen",
            "transport",
            "transportation",
            "classroom",
            "classrooms",
            "laboratory",
            "laboratories",
            "lab",
            "auditorium",
            "sports",
            "hostel",
            "wifi",
            "internet",
            "seminar",
            "seminar hall"
        ],

        # --------------------------------------
        # AIML
        # --------------------------------------

        "aiml": [
            "aiml",
            "ai ml",
            "ai and ml",
            "artificial intelligence",
            "machine learning",
            "artificial intelligence and machine learning",
            "cse aiml",
            "cse (aiml)"
        ],

        # --------------------------------------
        # EXAMINATION
        # --------------------------------------

        "examination": [
            "exam",
            "examination",
            "examinations",
            "timetable",
            "time table",
            "result",
            "results",
            "marks",
            "mark",
            "hall ticket",
            "hallticket",
            "question paper",
            "paper",
            "revaluation",
            "semester exam"
        ],

        # --------------------------------------
        # COLLEGE
        # --------------------------------------

        "college": [
            "college name",
            "college",
            "prpcem",
            "p.r. pote",
            "p r pote",
            "pote patil",
            "full name",
            "about college",
            "about prpcem",
            "which college"
        ]
    }

    scores = {}

    # --------------------------------------
    # SCORE EACH INTENT
    # --------------------------------------

    for intent, keywords in intent_keywords.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[intent] = score

    # --------------------------------------
    # GET BEST INTENT
    # --------------------------------------

    best_intent = max(
        scores,
        key=scores.get
    )

    # --------------------------------------
    # NO MATCH
    # --------------------------------------

    if scores[best_intent] == 0:
        return "unknown"

    return best_intent


# ==========================================
# CHATBOT RESPONSE
# ==========================================

def chatbot_answer(message):

    text = message.lower().strip()

    # ======================================
    # GREETINGS
    # ======================================

    greetings = [
        "hello",
        "hi",
        "hey",
        "hii",
        "hiii",
        "namaste",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if (
        text in greetings
        or any(
            text.startswith(greeting + " ")
            for greeting in greetings
        )
    ):

        return (
            "Hello! 👋 Welcome to PRPCEM Student Assistant.\n\n"
            "I can help you with PRPCEM-related information such as "
            "departments, facilities, CSE (AIML), examinations and "
            "college information.\n\n"
            "What would you like to know?"
        )

    # ======================================
    # THANK YOU
    # ======================================

    if text in [
        "thank you",
        "thanks",
        "thank u",
        "thx",
        "thankyou"
    ]:

        return (
            "You're welcome! 😊\n\n"
            "I'm happy to help with PRPCEM-related queries."
        )

    # ======================================
    # GOODBYE
    # ======================================

    if text in [
        "bye",
        "goodbye",
        "see you",
        "ok bye",
        "okay bye"
    ]:

        return (
            "Goodbye! 👋\n\n"
            "Have a great day!"
        )

    # ======================================
    # HOW ARE YOU
    # ======================================

    if text in [
        "how are you",
        "how are you?",
        "how r u",
        "how r u?",
        "how are u"
    ]:

        return (
            "I'm doing great! 🤖😊\n\n"
            "I'm ready to help you with PRPCEM-related "
            "information. What would you like to know?"
        )

    # ======================================
    # WHO ARE YOU
    # ======================================

    if text in [
        "who are you",
        "what are you",
        "what is this chatbot",
        "what is this"
    ]:

        return (
            "I'm the PRPCEM Student Assistant 🤖.\n\n"
            "I'm an AI-based student support system designed "
            "to provide information about PRPCEM and assist "
            "students with college-related queries."
        )

    # ======================================
    # DETECT INTENT
    # ======================================

    intent = detect_intent(text)

    # ======================================
    # COLLEGE INFORMATION
    # ======================================

    if intent == "college":

        return (
            "P. R. Pote Patil College of Engineering & "
            "Management, Amravati (PRPCEM)."
        )

    # ======================================
    # DEPARTMENTS
    # ======================================

    if intent == "departments":

        departments = KNOWLEDGE.get(
            "departments",
            []
        )

        if departments:

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

        return (
            "PRPCEM offers engineering programs including "
            "Computer Science, CSE (AIML), Artificial Intelligence "
            "and Data Science, Electrical, Mechanical, Civil and EXTC."
        )

    # ======================================
    # FACILITIES
    # ======================================

    if intent == "facilities":

        facilities = KNOWLEDGE.get(
            "facilities",
            []
        )

        if facilities:

            answer = (
                "PRPCEM provides facilities such as:\n\n"
            )

            for facility in facilities:

                answer += (
                    f"• {facility}\n"
                )

            return answer

        return (
            "PRPCEM provides facilities such as laboratories, "
            "library, classrooms, auditorium, sports facilities, "
            "canteen, transportation and other student-support facilities."
        )

    # ======================================
    # AIML
    # ======================================

    if intent == "aiml":

        return (
            "CSE (AIML) is an engineering department at PRPCEM.\n\n"
            "It focuses on Computer Science, Artificial Intelligence "
            "and Machine Learning."
        )

    # ======================================
    # EXAMINATION
    # ======================================

    if intent == "examination":

        return (
            "For examination-related information, students should "
            "refer to the official PRPCEM examination resources.\n\n"
            "I can help with general examination-related queries "
            "such as examination timetable, results, marks, hall "
            "tickets and other examination information."
        )

    # ======================================
    # UNKNOWN QUERY
    # ======================================

    return (
        "I'm PRPCEM Student Assistant. 🤖\n\n"
        "I can help only with PRPCEM-related questions such as:\n\n"
        "• Departments and courses\n"
        "• College information\n"
        "• Facilities\n"
        "• CSE (AIML)\n"
        "• Examination information\n\n"
        "Please ask me a PRPCEM-related question."
    )


# ==========================================
# COMPLAINT INPUT VALIDATION
# ==========================================

def is_meaningful_complaint(description):

    text = description.strip()

    # --------------------------------------
    # EMPTY OR VERY SHORT INPUT
    # --------------------------------------

    if len(text) < 8:
        return False

    # --------------------------------------
    # EXTRACT WORDS
    # --------------------------------------

    words = re.findall(
        r"[A-Za-z]+",
        text.lower()
    )

    # Need at least 2 words

    if len(words) < 2:
        return False

    # --------------------------------------
    # CHECK ALPHABETIC CONTENT
    # --------------------------------------

    letters = re.findall(
        r"[A-Za-z]",
        text
    )

    if len(letters) < 5:
        return False

    if len(letters) / max(len(text), 1) < 0.45:
        return False

    # --------------------------------------
    # RANDOM / MEANINGLESS INPUTS
    # --------------------------------------

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

    # --------------------------------------
    # REPEATED LETTER DETECTION
    # --------------------------------------

    unique_letters = set(
        cleaned_words
    )

    if len(cleaned_words) >= 5:

        if len(unique_letters) <= 2:
            return False

    # --------------------------------------
    # MEANINGFUL CONTEXT WORDS
    # --------------------------------------

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
        "misbehaved",
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

        # Common Hinglish
        "mujhe",
        "mere",
        "meri",
        "mera",
        "nhi",
        "nahi",
        "kar",
        "rahi",
        "raha",
        "hai"
    ]

    # --------------------------------------
    # KNOWN CONTEXT = VALID
    # --------------------------------------

    if any(
        word in words
        for word in meaningful_context_words
    ):
        return True

    # --------------------------------------
    # UNKNOWN BUT PROPER SENTENCE
    # --------------------------------------

    if len(words) >= 3:
        return True

    return False


# ==========================================
# COMPLAINT CATEGORY DETECTION
# ==========================================

def detect_category(description):

    text = description.lower().strip()

    categories = {

        # --------------------------------------
        # LABORATORY
        # --------------------------------------

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

        # --------------------------------------
        # WATER / SANITATION
        # --------------------------------------

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

        # --------------------------------------
        # ELECTRICAL / INFRASTRUCTURE
        # --------------------------------------

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

        # --------------------------------------
        # FACULTY / ACADEMIC
        # --------------------------------------

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

        # --------------------------------------
        # EXAMINATION
        # --------------------------------------

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

        # --------------------------------------
        # ADMINISTRATIVE
        # --------------------------------------

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

        # --------------------------------------
        # LIBRARY
        # --------------------------------------

        "Library": [
            "library",
            "book",
            "librarian",
            "reading room"
        ],

        # --------------------------------------
        # CANTEEN
        # --------------------------------------

        "Canteen": [
            "canteen",
            "food",
            "meal",
            "hygiene"
        ],

        # --------------------------------------
        # TRANSPORTATION
        # --------------------------------------

        "Transportation": [
            "bus",
            "transport",
            "vehicle",
            "route",
            "driver",
            "conductor"
        ],

        # --------------------------------------
        # SAFETY
        # --------------------------------------

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

    # --------------------------------------
    # SCORE CATEGORIES
    # --------------------------------------

    scores = {}

    for category, keywords in categories.items():

        score = 0

        for keyword in keywords:

            # Multi-word phrases
            if " " in keyword:

                if keyword in text:
                    score += 1

            # Single words
            else:

                if re.search(
                    r"\b" + re.escape(keyword) + r"\b",
                    text
                ):
                    score += 1

        scores[category] = score

    # --------------------------------------
    # BEST CATEGORY
    # --------------------------------------

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

    # --------------------------------------
    # SAFETY = HIGH
    # --------------------------------------

    if category == "Ragging / Harassment / Safety":
        return "HIGH"

    # --------------------------------------
    # EMERGENCY = HIGH
    # --------------------------------------

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

    # --------------------------------------
    # IMPORTANT TECHNICAL ISSUE = MEDIUM
    # --------------------------------------

    if any(
        phrase in complete_text
        for phrase in [
            "not working",
            "many students",
            "whole class",
            "entire lab",
            "urgent"
        ]
    ):
        return "MEDIUM"

    # --------------------------------------
    # NORMAL = LOW
    # --------------------------------------

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

    # --------------------------------------
    # EMPTY MESSAGE
    # --------------------------------------

    if not message:

        return jsonify({
            "reply": "Please enter a question."
        })

    # --------------------------------------
    # GENERATE RESPONSE
    # --------------------------------------

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
    # EMPTY INPUT
    # --------------------------------------

    if not description:

        return jsonify({
            "error": "Please describe your complaint."
        }), 400

    # --------------------------------------
    # VALIDATE COMPLAINT
    # --------------------------------------

    if not is_meaningful_complaint(
        description
    ):

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
    # GET QUESTIONS
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

    # --------------------------------------
    # EMPTY DESCRIPTION
    # --------------------------------------

    if not description:

        return jsonify({
            "error": "Complaint description is required."
        }), 400

    # --------------------------------------
    # VALIDATE AGAIN
    # --------------------------------------

    if not is_meaningful_complaint(
        description
    ):

        return jsonify({
            "error": (
                "Invalid complaint. "
                "Please provide meaningful details."
            )
        }), 400

    # --------------------------------------
    # CALCULATE PRIORITY
    # --------------------------------------

    priority = calculate_priority(
        category,
        description,
        answers
    )

    # --------------------------------------
    # GENERATE COMPLAINT ID
    # --------------------------------------

    complaint_id = (
        "PRPCEM-"
        + str(uuid.uuid4())[:8].upper()
    )

    # --------------------------------------
    # DATE & TIME
    # --------------------------------------

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    # --------------------------------------
    # SAVE TO SQLITE
    # --------------------------------------

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

    # --------------------------------------
    # RESPONSE
    # --------------------------------------

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