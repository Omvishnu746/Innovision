# app.py
import os
import json
from flask import Flask, jsonify, request
import mongomock

app = Flask(__name__)

# DB Mock to bypass Atlas connection issues
client = mongomock.MongoClient()
db = client["pm_internship"]

def seed_mock_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(base_dir, "Student.json"), "r") as f:
            students = json.load(f)
            db["student"].insert_many(students)
            db["Student"].insert_many(students)
        with open(os.path.join(base_dir, "Internships.json"), "r") as f:
            internships = json.load(f)
            db["internships"].insert_many(internships)
        print("Mock Database Seeded Successfully.")
    except Exception as e:
        print(f"Mock DB Seed Warning: {e}")

seed_mock_db()
# --- ROUTES ---

@app.route("/students", methods=["GET"])
def get_students():
    """Fetch all students"""
    students = list(db["student"].find({}, {"_id": 0}))  # ✅ use 'student'
    return jsonify(students)

@app.route("/internships", methods=["GET"])
def get_internships():
    """Fetch all internships"""
    internships = list(db["internships"].find({}, {"_id": 0}))
    return jsonify(internships)

@app.route("/register_student", methods=["POST"])
def register_student():
    """Register a new student"""
    data = request.json
    if not data or "student_id" not in data:
        return {"error": "student_id missing"}, 400
    db["student"].insert_one(data)  # ✅ use 'student'
    return {"message": "Student added"}, 201

@app.route("/recommendations", methods=["GET"])
def recommendations():
    student_id = request.args.get("student_id")
    if not student_id:
        return {"error": "student_id query param required"}, 400

    # Try int match first, then string match, then id field fallback
    student = db["student"].find_one({"student_id": int(student_id)}, {"_id": 0}) \
              or db["student"].find_one({"student_id": student_id}, {"_id": 0}) \
              or db["student"].find_one({"id": int(student_id)}, {"_id": 0}) \
              or db["student"].find_one({"id": student_id}, {"_id": 0})

    if not student:
        return {"error": "student not found"}, 404

    candidates = list(db["internships"].find({}, {"_id": 0}))
    scored = []

    s_skills = set([k.lower() for k in student.get("skills", [])])

    for c in candidates:
        c_skills = set([k.lower() for k in c.get("skills_required", [])])
        match = len(s_skills & c_skills)
        scored.append({"internship": c, "score": match})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return jsonify(scored[:10])


# --- MAIN ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)
