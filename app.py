import streamlit as st

st.title("🏠 PG Match Engine")

pg_data = [
    {"name":"PG A","price":6200,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":9,"food_quality":8,"crowd":"Employees"},
    {"name":"PG B","price":6000,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":7,"crowd":"Mixed"},
    {"name":"PG C","price":5500,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":6,"food_quality":5,"crowd":"Students"}
]

budget = st.slider("Budget", 3000, 10000, 6000)
food = st.selectbox("Food Required", ["Yes", "No"])
crowd = st.selectbox("Preferred Crowd", ["Employees", "Students", "Mixed"])

user = {
    "budget": budget,
    "location": "ameerpet",
    "food": food,
    "gender": "Male",
    "room": "Non-AC",
    "crowd": crowd
}

filtered_pgs = []

for pg in pg_data:
    if user["food"] == "Yes" and pg["food"] != "Yes":
        continue
    filtered_pgs.append(pg)

scored_pgs = []

for pg in filtered_pgs:
    score = 0

    diff = pg["price"] - user["budget"]

    if diff <= 0:
        score += 30
    elif diff <= 500:
        score += 25
    elif diff <= 1000:
        score += 15
    else:
        score += 5

    if pg["location"] == user["location"]:
        score += 25

    score += (pg["cleanliness"]/10) * 15
    score += (pg["food_quality"]/10) * 10

    if pg["crowd"] == user["crowd"]:
        score += 10
    else:
        score += 5

    scored_pgs.append({
        "name": pg["name"],
        "score": round(score, 2),
        "price": pg["price"]
    })

scored_pgs.sort(key=lambda x: x["score"], reverse=True)

st.subheader("🏆 Top Matches")

for pg in scored_pgs[:3]:

    original = next(x for x in filtered_pgs if x["name"] == pg["name"])

    st.markdown(f"### 🏠 {pg['name']} — {pg['score']}% Match")

    # WHY THIS MATCH
    st.markdown("**Why this match?**")

    if pg["price"] <= user["budget"]:
        st.write(f"✔️ Within budget (₹{pg['price']})")
    else:
        st.write(f"⚠️ Above budget (₹{pg['price']})")

    if original["location"] == user["location"]:
        st.write("📍 Exact location match")

    if original["food"] == "Yes":
        st.write("🍽️ Food available")

    if original["crowd"] == user["crowd"]:
        st.write("👥 Preferred crowd match")

    # WHY CHOOSE
    st.markdown("**Why choose this PG?**")

    if original["cleanliness"] >= 8:
        st.write("✨ High cleanliness")

    if original["food_quality"] >= 7:
        st.write("🍛 Good food quality")

    # DRAWBACKS
    st.markdown("**Things to consider:**")

    if pg["price"] > user["budget"]:
        st.write("⚠️ Slightly above budget")

    if original["cleanliness"] < 7:
        st.write("⚠️ Cleanliness could be better")

    if original["food_quality"] < 6:
        st.write("⚠️ Food quality is average/low")

    if original["crowd"] != user["crowd"]:
        st.write("⚠️ Mixed crowd")

    st.divider()
