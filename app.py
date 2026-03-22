# =========================
# 🏠 PG MATCH ENGINE (FINAL PRO)
# =========================

import ipywidgets as widgets
from IPython.display import display, clear_output
import matplotlib.pyplot as plt


# =========================
# 📊 PG DATA
# =========================

pg_data = [
    {"name":"PG A","price":6200,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":9,"food_quality":8,"crowd":"Employees"},
    {"name":"PG B","price":4800,"location":"sr nagar","food":"No","gender":"Male","room":"Non-AC","cleanliness":6,"food_quality":5,"crowd":"Students"},
    {"name":"PG C","price":7500,"location":"begumpet","food":"Yes","gender":"Male","room":"AC","cleanliness":9,"food_quality":9,"crowd":"Employees"},
    {"name":"PG D","price":5300,"location":"ameerpet","food":"Yes","gender":"Male","room":"Non-AC","cleanliness":7,"food_quality":6,"crowd":"Mixed"},
    {"name":"PG E","price":6800,"location":"sr nagar","food":"Yes","gender":"Male","room":"AC","cleanliness":8,"food_quality":7,"crowd":"Employees"},
    {"name":"PG F","price":4500,"location":"kukatpally","food":"No","gender":"Male","room":"Non-AC","cleanliness":5,"food_quality":4,"crowd":"Students"}
]


# =========================
# 📍 DISTANCE MAP
# =========================

distance_map = {
    "ameerpet": {"ameerpet": 0, "sr nagar": 1, "begumpet": 2, "kukatpally": 4},
    "sr nagar": {"ameerpet": 1, "sr nagar": 0, "begumpet": 2, "kukatpally": 3},
    "begumpet": {"ameerpet": 2, "sr nagar": 2, "begumpet": 0, "kukatpally": 5},
    "kukatpally": {"ameerpet": 4, "sr nagar": 3, "begumpet": 5, "kukatpally": 0}
}


# =========================
# 🧾 SIMPLE CARD DISPLAY
# =========================

def show_card(title, content):
    print("="*50)
    print(title)
    print("-"*50)
    print(content)
    print("="*50 + "\n")


# =========================
# 📊 GRAPH FUNCTION
# =========================

def show_graph(breakdown, name):
    labels = list(breakdown.keys())
    values = list(breakdown.values())

    plt.figure(figsize=(6,3))
    plt.bar(labels, values)
    plt.title(f"{name} Score Breakdown")
    plt.xticks(rotation=30)
    plt.show()


# =========================
# 🎛️ UI
# =========================

budget = widgets.IntText(value=6000, description='Budget ₹')

location = widgets.Dropdown(
    options=['ameerpet', 'sr nagar', 'begumpet', 'kukatpally'],
    description='Location'
)

food = widgets.ToggleButtons(options=['Yes', 'No'], description='Food')
gender = widgets.ToggleButtons(options=['Male', 'Female'], description='Gender')
room = widgets.ToggleButtons(options=['Non-AC', 'AC'], description='Room')
crowd = widgets.Dropdown(options=['Employees', 'Students', 'Mixed'], description='Crowd')

button = widgets.Button(description="Find PG 🔍")
output = widgets.Output()

display(budget, location, food, gender, room, crowd, button, output)


# =========================
# 🧠 MAIN LOGIC
# =========================

def on_button_click(b):
    with output:
        clear_output()

        user = {
            "budget": budget.value,
            "location": location.value.lower(),
            "food": food.value,
            "gender": gender.value,
            "room": room.value,
            "crowd": crowd.value
        }

        filtered_pgs = []

        for pg in pg_data:
            if pg["gender"] != user["gender"]:
                continue
            filtered_pgs.append(pg)

        scored_pgs = []
        MAX_SCORE = 150

        for pg in filtered_pgs:
            score = 0

            breakdown = {
                "Budget": 0,
                "Distance": 0,
                "Cleanliness": 0,
                "Food": 0,
                "Crowd": 0,
                "Room": 0,
                "Boost": 0
            }

            # 💰 Budget
            diff = pg["price"] - user["budget"]
            if diff <= 0:
                score += 30
                breakdown["Budget"] = 30
            elif diff <= 300:
                score += 20
                breakdown["Budget"] = 20
            elif diff <= 800:
                score += 10
                breakdown["Budget"] = 10

            # 📍 Distance
            distance = distance_map.get(user["location"], {}).get(pg["location"], 5)

            if distance == 0:
                score += 25
                breakdown["Distance"] = 25
            elif distance == 1:
                score += 20
                breakdown["Distance"] = 20
            elif distance == 2:
                score += 15
                breakdown["Distance"] = 15
            elif distance <= 3:
                score += 10
                breakdown["Distance"] = 10
            else:
                score += 5
                breakdown["Distance"] = 5

            # 🧼 Cleanliness
            clean_score = (pg["cleanliness"] / 10) * 20
            score += clean_score
            breakdown["Cleanliness"] = round(clean_score, 1)

            # 🍽️ Food
            food_score = (pg["food_quality"] / 10) * 10
            score += food_score
            breakdown["Food"] = round(food_score, 1)

            if user["food"] == "Yes" and pg["food"] == "Yes":
                score += 10
                breakdown["Food"] += 10

            # 👥 Crowd
            if pg["crowd"] == user["crowd"]:
                score += 10
                breakdown["Crowd"] = 10
            else:
                score += 5
                breakdown["Crowd"] = 5

            # 🛏️ Room
            if pg["room"] == user["room"]:
                score += 5
                breakdown["Room"] = 5

            # 🔥 BOOST
            perfect_match = 0
            if pg["price"] <= user["budget"]:
                perfect_match += 1
            if pg["location"] == user["location"]:
                perfect_match += 1
            if user["food"] == "Yes" and pg["food"] == "Yes":
                perfect_match += 1
            if pg["crowd"] == user["crowd"]:
                perfect_match += 1

            if perfect_match >= 3:
                score += 15
                breakdown["Boost"] = 15
            elif perfect_match == 2:
                score += 8
                breakdown["Boost"] = 8

            percentage = min((score / MAX_SCORE) * 100, 100)

            scored_pgs.append({
                "name": pg["name"],
                "score": round(percentage, 2),
                "price": pg["price"],
                "breakdown": breakdown
            })

        # SORT
        scored_pgs.sort(key=lambda x: x["score"], reverse=True)
        top_3 = scored_pgs[:3]

        print("\n🏆 Top PG Recommendations\n")

        rank = 1

        for pg in top_3:
            name = pg["name"]
            score = pg["score"]
            price = pg["price"]
            bd = pg["breakdown"]

            original = next(x for x in filtered_pgs if x["name"] == name)

            content = f"""
₹{price} | Score: {score}%

Location: {original['location']}
Food: {original['food']}
Crowd: {original['crowd']}

Breakdown:
{bd}
"""

            if rank == 1:
                title = f"🥇 Best Match — {name}"
            elif rank == 2:
                title = f"🥈 Good Match — {name}"
            else:
                title = f"🥉 Option — {name}"

            show_card(title, content)
            show_graph(bd, name)

            rank += 1


button.on_click(on_button_click)
