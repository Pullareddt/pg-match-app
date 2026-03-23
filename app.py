import streamlit as st

st.title("🏠 PG Match Engine")

# ------------------ PG DATA ------------------
pg_data = [
{"name":"Green Nest PG","price":5500,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":8,"food_quality":7,"crowd":"Employees"},
{"name":"Urban Stay PG","price":7000,"location":"ameerpet","food":"Yes","gender":"Female","room":"AC","cleanliness":9,"food_quality":8,"crowd":"Employees"},
{"name":"Happy Homes PG","price":4800,"location":"sr nagar","food":"Yes","gender":"Female","room":"Non-AC","cleanliness":6,"food_quality":6,"crowd":"Students"},
{"name":"Comfort PG","price":6200,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":7,"crowd":"Mixed"},
{"name":"Elite Stay","price":8500,"location":"madhapur","food":"Yes","gender":"Female","room":"AC","cleanliness":9,"food_quality":9,"crowd":"Employees"},
{"name":"Budget PG","price":4000,"location":"kphb","food":"No","gender":"Male","room":"Non-AC","cleanliness":5,"food_quality":5,"crowd":"Students"},
{"name":"Royal PG","price":7500,"location":"ameerpet","food":"Yes","gender":"Female","room":"AC","cleanliness":8,"food_quality":8,"crowd":"Employees"},
{"name":"Metro Stay","price":6000,"location":"sr nagar","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":6,"crowd":"Mixed"},
{"name":"Lake View PG","price":9000,"location":"madhapur","food":"Yes","gender":"Female","room":"AC","cleanliness":9,"food_quality":9,"crowd":"Employees"},
{"name":"Simple Stay","price":4500,"location":"kukatpally","food":"No","gender":"Male","room":"Non-AC","cleanliness":6,"food_quality":5,"crowd":"Students"},
{"name":"City PG","price":6500,"location":"ameerpet","food":"Yes","gender":"Female","room":"Non-AC","cleanliness":8,"food_quality":7,"crowd":"Employees"},
{"name":"Tech Stay","price":8000,"location":"hitech city","food":"Yes","gender":"Male","room":"AC","cleanliness":9,"food_quality":8,"crowd":"Employees"},
{"name":"Student Hub","price":5000,"location":"dilsukhnagar","food":"Yes","gender":"Female","room":"Non-AC","cleanliness":6,"food_quality":6,"crowd":"Students"},
{"name":"Peace PG","price":5800,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":7,"crowd":"Employees"},
{"name":"Luxury Stay","price":10000,"location":"jubilee hills","food":"Yes","gender":"Female","room":"AC","cleanliness":10,"food_quality":9,"crowd":"Employees"},
{"name":"Easy Stay","price":5200,"location":"sr nagar","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":6,"crowd":"Mixed"},
{"name":"Fast PG","price":6100,"location":"ameerpet","food":"Yes","gender":"Female","room":"Non-AC","cleanliness":8,"food_quality":7,"crowd":"Employees"},
{"name":"Prime Stay","price":7800,"location":"madhapur","food":"Yes","gender":"Male","room":"AC","cleanliness":9,"food_quality":8,"crowd":"Employees"},
{"name":"Basic PG","price":4200,"location":"kphb","food":"No","gender":"Female","room":"Non-AC","cleanliness":5,"food_quality":5,"crowd":"Students"},
{"name":"Comfort Zone","price":6700,"location":"ameerpet","food":"Yes","gender":"Female","room":"Non-AC","cleanliness":8,"food_quality":8,"crowd":"Employees"}
]

# ------------------ USER INPUT ------------------
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

# ------------------ LOCATION DISTANCE ------------------
location_distance = {
    "ameerpet": 0,
    "sr nagar": 1,
    "kphb": 3,
    "kukatpally": 3,
    "madhapur": 4,
    "hitech city": 5,
    "jubilee hills": 5,
    "dilsukhnagar": 6
}

# ------------------ FILTER ------------------
filtered_pgs = []

for pg in pg_data:
    if pg["gender"] != user["gender"]:
        continue
    if user["food"] == "Yes" and pg["food"] != "Yes":
        continue
    filtered_pgs.append(pg)

# ------------------ SCORING ------------------
scored_pgs = []

for pg in filtered_pgs:
    score = 0

    # Budget
    diff = pg["price"] - user["budget"]
    if diff <= 0:
        score += 30
    elif diff <= 500:
        score += 25
    elif diff <= 1000:
        score += 15
    else:
        score += 5

    # Location
    dist = abs(location_distance.get(pg["location"], 10) - location_distance.get(user["location"], 10))
    if dist == 0:
        score += 25
    elif dist <= 2:
        score += 15
    else:
        score += 5

    # Other factors
    score += (pg["cleanliness"]/10) * 15
    score += (pg["food_quality"]/10) * 10

    if pg["crowd"] == user["crowd"]:
        score += 10
    else:
        score += 5

    if pg["room"] == user["room"]:
        score += 5

    scored_pgs.append({
        "name": pg["name"],
        "score": round(score, 2),
        "price": pg["price"]
    })

scored_pgs.sort(key=lambda x: x["score"], reverse=True)

# ------------------ OUTPUT ------------------
st.subheader("🏆 Top Matches")

for pg in scored_pgs[:3]:

    original = next(x for x in filtered_pgs if x["name"] == pg["name"])

    # TAGS
    tags = []
    if original["cleanliness"] >= 8:
        tags.append("✨ Clean")
    if original["food_quality"] >= 7:
        tags.append("🍽️ Good Food")
    if pg["price"] <= user["budget"]:
        tags.append("💰 Budget Friendly")

    tag_str = " | ".join(tags)

    st.markdown(f"### 🏠 {pg['name']} — {pg['score']}% Match")
    st.markdown(f"**{tag_str}**")

    # WHY MATCH
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
