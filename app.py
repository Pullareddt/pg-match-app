import streamlit as st
import pandas as pd

st.set_page_config(page_title="PG Match Engine", layout="wide")

st.title("🏠 PG Match Engine")

# ---------------- DARK MODE ----------------
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown("""
    <style>
    body { background-color: #0e1117; color: white; }
    </style>
    """, unsafe_allow_html=True)

# ---------------- STYLING ----------------
st.markdown("""
<style>
.card {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    transition: transform 0.3s ease;
}
.card:hover {
    transform: scale(1.02);
}
.tag {
    display: inline-block;
    background-color: #e0f7fa;
    padding: 5px 10px;
    border-radius: 8px;
    margin-right: 5px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- PG DATA ----------------
pg_data = [
{"name":"Green Nest PG","price":5500,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":8,"food_quality":7,"crowd":"Employees","image":"https://images.unsplash.com/photo-1554995207-c18c203602cb"},
{"name":"Urban Stay PG","price":7000,"location":"ameerpet","food":"Yes","gender":"Female","room":"AC","cleanliness":9,"food_quality":8,"crowd":"Employees","image":"https://images.unsplash.com/photo-1560448204-e02f11c3d0e2"},
{"name":"Happy Homes PG","price":4800,"location":"sr nagar","food":"Yes","gender":"Female","room":"Non-AC","cleanliness":6,"food_quality":6,"crowd":"Students","image":"https://images.unsplash.com/photo-1505691938895-1758d7feb511"},
{"name":"Comfort PG","price":6200,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":7,"crowd":"Mixed","image":"https://images.unsplash.com/photo-1502672260266-1c1ef2d93688"},
{"name":"Elite Stay","price":8500,"location":"madhapur","food":"Yes","gender":"Female","room":"AC","cleanliness":9,"food_quality":9,"crowd":"Employees","image":"https://images.unsplash.com/photo-1505693416388-ac5ce068fe85"},
{"name":"Budget PG","price":4000,"location":"kphb","food":"No","gender":"Male","room":"Non-AC","cleanliness":5,"food_quality":5,"crowd":"Students","image":"https://images.unsplash.com/photo-1484154218962-a197022b5858"},
{"name":"Royal PG","price":7500,"location":"ameerpet","food":"Yes","gender":"Female","room":"AC","cleanliness":8,"food_quality":8,"crowd":"Employees","image":"https://images.unsplash.com/photo-1493809842364-78817add7ffb"},
{"name":"Metro Stay","price":6000,"location":"sr nagar","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":6,"crowd":"Mixed","image":"https://images.unsplash.com/photo-1494526585095-c41746248156"},
{"name":"Lake View PG","price":9000,"location":"madhapur","food":"Yes","gender":"Female","room":"AC","cleanliness":9,"food_quality":9,"crowd":"Employees","image":"https://images.unsplash.com/photo-1501183638710-841dd1904471"},
{"name":"Simple Stay","price":4500,"location":"kukatpally","food":"No","gender":"Male","room":"Non-AC","cleanliness":6,"food_quality":5,"crowd":"Students","image":"https://images.unsplash.com/photo-1472220625704-91e1462799b2"}
]

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

# ---------------- LOCATION ----------------
location_coords = {
    "ameerpet": [17.4375, 78.4483],
    "sr nagar": [17.4410, 78.4485],
    "madhapur": [17.4485, 78.3908],
    "kphb": [17.4933, 78.3997],
    "kukatpally": [17.4948, 78.3996]
}

# ---------------- FILTER ----------------
filtered_pgs = []

for pg in pg_data:
    if pg["gender"] != user["gender"]:
        continue
    if user["food"] == "Yes" and pg["food"] != "Yes":
        continue
    filtered_pgs.append(pg)

# ---------------- SCORING ----------------
scored_pgs = []

for pg in filtered_pgs:
    score = 0

    diff = pg["price"] - user["budget"]
    if diff <= 0:
        score += 30
    elif diff <= 500:
        score += 25
    else:
        score += 10

    score += (pg["cleanliness"]/10) * 15
    score += (pg["food_quality"]/10) * 10

    if pg["crowd"] == user["crowd"]:
        score += 10

    scored_pgs.append({
        "name": pg["name"],
        "score": round(score, 2),
        "price": pg["price"]
    })

scored_pgs.sort(key=lambda x: x["score"], reverse=True)

# ---------------- OUTPUT ----------------
st.subheader("🏆 Top Matches")

for pg in scored_pgs[:3]:

    original = next(x for x in filtered_pgs if x["name"] == pg["name"])

    # TAGS
    tags = ""
    if original["cleanliness"] >= 8:
        tags += '<span class="tag">✨ Clean</span>'
    if original["food_quality"] >= 7:
        tags += '<span class="tag">🍽️ Good Food</span>'
    if pg["price"] <= user["budget"]:
        tags += '<span class="tag">💰 Budget</span>'

    st.image(original["image"], use_column_width=True)

    st.markdown(f"""
    <div class="card">
        <h3>🏠 {pg['name']} — {pg['score']}% Match</h3>
        {tags}

        <p><b>💰 Price:</b> ₹{pg['price']}</p>
        <p><b>📍 Location:</b> {original['location']}</p>
        <p><b>👥 Crowd:</b> {original['crowd']}</p>
    </div>
    """, unsafe_allow_html=True)

    # MAP
    coords = location_coords.get(original["location"], [17.43, 78.44])
    map_data = pd.DataFrame([{"lat": coords[0], "lon": coords[1]}])
    st.map(map_data)

    st.divider()
