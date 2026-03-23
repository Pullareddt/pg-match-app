import streamlit as st
import random

st.set_page_config(page_title="PG Match Engine", layout="wide")

st.title("🏠 PG Match Engine")

# ---------------- USER INPUT ----------------

# ✅ FIXED SLIDER (STEP VALUE)
budget = st.slider("Budget", 3000, 10000, step=500, value=6000)

food = st.selectbox("Food Required", ["Yes", "No"])
gender = st.selectbox("Gender", ["Male", "Female"])
crowd = st.selectbox("Preferred Crowd", ["Employees", "Students", "Mixed"])

# ✅ LOCATION DROPDOWN (FORM STYLE)
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

# ---------------- DYNAMIC PG DATA (50 PGs) ----------------

locations = ["ameerpet", "sr nagar", "madhapur", "kphb", "kukatpally", "hitech city"]
crowds = ["Employees", "Students", "Mixed"]

pg_data = []

for i in range(50):
    pg_data.append({
        "name": f"PG {i+1}",
        "price": random.choice(range(4000, 10001, 500)),
        "location": random.choice(locations),
        "food": random.choice(["Yes", "No"]),
        "gender": random.choice(["Male", "Female"]),
        "room": random.choice(["AC", "Non-AC"]),
        "cleanliness": random.randint(5, 10),
        "food_quality": random.randint(5, 10),
        "crowd": random.choice(crowds)
    })

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

    # Location
    if pg["location"] == user["location"]:
        score += 25
    else:
        score += 10

    # Cleanliness
    score += (pg["cleanliness"]/10) * 15
    if pg["cleanliness"] < 7:
        issues.append("⚠️ Cleanliness could be better")

    # Food quality
    score += (pg["food_quality"]/10) * 10
    if pg["food_quality"] < 6:
        issues.append("⚠️ Food quality is average/low")

    # Crowd
    if pg["crowd"] == user["crowd"]:
        score += 10
    else:
        issues.append("⚠️ Crowd may not match preference")

    # Room
    if pg["room"] == user["room"]:
        score += 5
    else:
        issues.append("⚠️ Room type mismatch")

    results.append({
        "pg": pg,
        "score": round(score, 2),
        "issues": issues
    })

# Sort
results.sort(key=lambda x: x["score"], reverse=True)

# ---------------- OUTPUT ----------------

st.subheader("🏆 Top Matches")

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

    # WHY MATCH
    st.markdown("**Why this match?**")
    st.write(f"💰 Price: ₹{pg['price']}")
    st.write(f"📍 Location: {pg['location']}")
    st.write(f"🍽️ Food: {pg['food']}")
    st.write(f"👥 Crowd: {pg['crowd']}")

    # WHY CHOOSE
    st.markdown("**Why choose this PG?**")
    if pg["cleanliness"] >= 8:
        st.write("✨ High cleanliness")
    if pg["food_quality"] >= 7:
        st.write("🍛 Good food quality")

    # THINGS TO CONSIDER
    st.markdown("**Things to consider:**")

    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("✅ No major issues — excellent match!")

    st.markdown("---")
