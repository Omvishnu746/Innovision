import json
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://Teamuser:Team1234@pm-cluster.ezvd3su.mongodb.net/pm_internship"
client = MongoClient(MONGO_URI)
db = client["pm_internship"]

# 1. Fix Internships.json to use integer internship_id instead of string _id
with open("Internships.json", "r") as f:
    internships = json.load(f)

for i, inter in enumerate(internships, start=1):
    if "_id" in inter:
        del inter["_id"]
    inter["internship_id"] = i

with open("Internships.json", "w") as f:
    json.dump(internships, f, indent=2)

print("Internships.json fixed: converted _id to integer internship_id.")

# 2. Load Student data
with open("Student.json", "r") as f:
    students = json.load(f)

# 3. Seed MongoDB
print("Clearing old data from MongoDB collections...")
db["Student"].delete_many({})
db["student"].delete_many({})
db["internships"].delete_many({})

if students:
    db["Student"].insert_many(students)
    db["student"].insert_many(students)  # Adding to both to support both app.py versions
    print(f"Inserted {len(students)} students.")

if internships:
    db["internships"].insert_many(internships)
    print(f"Inserted {len(internships)} internships.")

print("Database seeding completed.")
