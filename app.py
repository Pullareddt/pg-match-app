import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="PG Finder", layout="wide")

st.title("PG Finder")
st.write("Find best PG based on your needs")

# 🔹 USER INPUT
budget = st.number_input("Budget", value=6000)
location = st.selectbox("Location", ["ameerpet", "sr nagar", "begumpet"])
food = st.selectbox("Food", ["Yes", "No"])
gender = st.selectbox("Gender", ["Male", "Female"])

# 🔹 PG DATA
pg_data = [
    {"name": "PG A", "price": 6000, "location": "ameerpet", "food": "Yes", "gender": "Male", "cleanliness": 9, "food_quality": 8},
    {"name": "PG B", "price": 5000, "location": "sr nagar", "food": "No", "gender": "Male", "cleanliness": 6, "food_quality": 5},
    {"name": "PG C", "price": 7500, "location": "begumpet", "food": "Yes", "gender": "Male", "cleanliness": 8, "food_quality": 9},
]

# 🔹 BUTTON
if st.button("Find PG"):

    results = []

    for pg in pg_data:
        if pg["gender"] != gender:
            continue

        score = 0

        # Budget score
        if pg["price"] <= budget:
            score += 30

        # Cleanliness
        score += (pg["cleanliness"] / 10) * 20

        # Food quality
        score += (pg["food_quality"] / 10) * 10

        # Food preference
        if food == "Yes" and pg["food"] == "Yes":
            score += 10

        percentage = min((score / 100) * 100, 100)

        results.append((pg, percentage))

    # Sort
    results.sort(key=lambda x: x[1], reverse=True)

    st.subheader("Top Results")

    for pg, score in results:

        st.markdown(f"""
        ### {pg['name']} - {round(score,1)}%

        Price: ₹{pg['price']}  
        Location: {pg['location']}  
        Food: {pg['food']}
        """)

        # Graph
        labels = ["Cleanliness", "Food"]
        values = [pg["cleanliness"], pg["food_quality"]]

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        st.pyplot(fig)
