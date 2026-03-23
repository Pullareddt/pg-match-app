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

st.subheader("Top Matches")

for pg in scored_pgs[:3]:
    st.write(f"### {pg['name']} — {pg['score']}% match")
    st.write(f"Price: ₹{pg['price']}")
