import streamlit as st

st.set_page_config(page_title="PG Match Engine", layout="wide")

st.title("🏠 PG Match Engine")

# ---------------- USER INPUT ----------------
budget = st.slider("Budget", 3000, 10000, 6000)
food = st.selectbox("Food Required", ["Yes", "No"])
gender = st.selectbox("Gender", ["Male", "Female"])
crowd = st.selectbox("Preferred Crowd", ["Employees", "Students", "Mixed"])

user = {
    "budget": budget,
    "location": "ameerpet",
    "food": food,
    "gender": gender,
    "room": "Non-AC",
    "crowd": crowd
}

# ---------------- PG DATA ----------------
pg_data = [
{"name":"Green Nest PG","price":5500,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":8,"food_quality":7,"crowd":"Employees"},
{"name":"Peace PG","price":5800,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":7,"crowd":"Employees"},
{"name":"Comfort PG","price":6200,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":6,"food_quality":7,"crowd":"Mixed"},
{"name":"City PG","price":6500,"location":"ameerpet","food":"Yes","gender":"Female","room":"Non-AC","cleanliness":8,"food_quality":7,"crowd":"Employees"},
{"name":"Happy Homes PG","price":4800,"location":"sr nagar","food":"Yes","gender":"Female","room":"Non-AC","cleanliness":6,"food_quality":6,"crowd":"Students"}
]

# ---------------- FILTER ----------------
filtered_pgs = []

for pg in pg_data:
    if pg["gender"] != user["gender"]:
        continue
    if user["food"] == "Yes" and pg["food"] != "Yes":
        continue
    filtered_pgs.append(pg)

# ---------------- SCORING + ISSUES INSIDE ----------------
results = []

for pg in filtered_pgs:

    score = 0
    issues = []   # ✅ defined inside loop (no error ever)

    # Budget scoring
    if pg["price"] <= user["budget"]:
        score += 30
    else:
        score += 15
        issues.append(f"⚠️ Above budget (₹{pg['price']})")

    # Location
    if pg["location"] == user["location"]:
        score += 25

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

    # ✅ FINAL FIXED SECTION
    st.markdown("**Things to consider:**")

    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("✅ No major issues — excellent match!")

    st.markdown("---")
