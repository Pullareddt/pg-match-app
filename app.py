import streamlit as st
import pandas as pd
import math
import random

st.set_page_config(page_title="PG Match Engine", layout="wide")

st.title("🏠 PG Match Engine")

# ---------------- LOAD CSV ----------------
df = pd.read_csv("pg_data.csv")
pg_data = df.to_dict(orient="records")

# ---------------- USER INPUT ----------------
budget = st.slider("Budget", 3000, 10000, step=500, value=6000)

food = st.selectbox("Food Required", ["Yes", "No"])
gender = st.selectbox("Gender", ["Male", "Female"])
crowd = st.selectbox("Preferred Crowd", ["Employees", "Students", "Mixed"])

location = st.selectbox(
    "Preferred Location",
    ["ameerpet", "sr nagar", "madhapur", "kphb", "kukatpally", "hitech city"]
)

user = {
    "budget": budget,
    "location": location,
    "food": food,
    "gender": gender,
    "room": "Non-AC",
    "crowd": crowd
}

# ---------------- LOCATION COORDS ----------------
location_coords = {
    "ameerpet": (17.4375, 78.4483),
    "sr nagar": (17.4410, 78.4485),
    "madhapur": (17.4485, 78.3908),
    "kphb": (17.4933, 78.3997),
    "kukatpally": (17.4948, 78.3996),
    "hitech city": (17.4484, 78.3915)
}

def calculate_distance(loc1, loc2):
    lat1, lon1 = location_coords.get(loc1, (0,0))
    lat2, lon2 = location_coords.get(loc2, (0,0))
    return math.sqrt((lat1-lat2)**2 + (lon1-lon2)**2)

# ---------------- FILTER ----------------
filtered_pgs = []

for pg in pg_data:
    if pg["gender"] != user["gender"]:
        continue
    if user["food"] == "Yes" and pg["food"] != "Yes":
        continue
    filtered_pgs.append(pg)

# ---------------- SCORING ----------------
results = []

for pg in filtered_pgs:

    score = 0
    issues = []

    # Budget
    if pg["price"] <= user["budget"]:
        score += 30
    else:
        score += 15
        issues.append(f"⚠️ Above budget (₹{pg['price']})")

    # Distance
    dist = calculate_distance(pg["location"], user["location"])

    if dist == 0:
        score += 25
    elif dist < 0.01:
        score += 15
    else:
        score += 5

    # Cleanliness
    score += (pg["cleanliness"]/10) * 15
    if pg["cleanliness"] < 7:
        issues.append("⚠️ Cleanliness could be better")

    # Food Quality
    score += (pg["food_quality"]/10) * 10
    if pg["food_quality"] < 6:
        issues.append("⚠️ Food quality is average/low")

    # Crowd
    if pg["crowd"] == user["crowd"]:
        score += 10
    else:
        issues.append("⚠️ Crowd may not match preference")

    results.append({
        "pg": pg,
        "score": round(score, 2),
        "issues": issues
    })

# Sort
results.sort(key=lambda x: x["score"], reverse=True)

# ---------------- OUTPUT ----------------
st.subheader("🏆 Top Matches")

reviews = [
    "Good place 👍",
    "Food is decent 🍛",
    "Clean rooms ✨",
    "Affordable 💰",
    "Nice environment 😊"
]

for item in results[:3]:

    pg = item["pg"]
    score = item["score"]
    issues = item["issues"]

    # TAGS
    tags = []
    if pg["cleanliness"] >= 8:
        tags.append("✨ Clean")
    if pg["food_quality"] >= 7:
        tags.append("🍽️ Good Food")
    if pg["price"] <= user["budget"]:
        tags.append("💰 Budget Friendly")

    st.markdown(f"### 🏠 {pg['name']} — {score}% Match")
    st.markdown(" | ".join(tags))

    # DETAILS
    st.write(f"💰 Price: ₹{pg['price']}")
    st.write(f"📍 Location: {pg['location']}")
    st.write(f"⭐ Rating: {pg['rating']}/5")

    # REVIEW
    st.write("🗣️ Review:")
    st.write(random.choice(reviews))

    # ISSUES
    st.markdown("**Things to consider:**")
    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("✅ No major issues — excellent match!")

    st.markdown("---")
