import streamlit as st
import pickle
import pandas as pd
import os

# ----------------------------
# 1️⃣ PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="IPL Win Predictor", layout="wide", page_icon="🏏")

# ----------------------------
# 2️⃣ TEAMS, CITIES & COLORS
# ----------------------------
teams = [
    'Mumbai Indians', 'Kolkata Knight Riders', 'Rajasthan Royals',
    'Chennai Super Kings', 'Royal Challengers Bengaluru', 'Lucknow Super Giants',
    'Gujarat Titans', 'Punjab Kings', 'Delhi Capitals', 'Sunrisers Hyderabad'
]

cities = [
    'Ahmedabad', 'Mumbai', 'Kolkata', 'Delhi', 'Chennai', 'Hyderabad', 'Bengaluru',
    'Jaipur', 'Lucknow', 'Mohali', 'Visakhapatnam', 'Pune', 'Raipur', 'Abu Dhabi', 'Dubai'
]

TEAM_COLORS = {
    "Mumbai Indians": "#004c97",
    "Chennai Super Kings": "#f7c600",
    "Kolkata Knight Riders": "#4b1266",
    "Rajasthan Royals": "#25408f",
    "Royal Challengers Bengaluru": "#da1212",
    "Lucknow Super Giants": "#f1a10a",
    "Gujarat Titans": "#0a5275",
    "Punjab Kings": "#7b1113",
    "Delhi Capitals": "#001c58",
    "Sunrisers Hyderabad": "#ff7300"
}

# ----------------------------
# 3️⃣ LOGO HANDLING
# ----------------------------
LOGO_DIR = "logo"
DEFAULT_LOGO = os.path.join(LOGO_DIR, "default.png")

def slugify(name):
    return name.lower().replace(" ", "_").replace("-", "_")

def team_logo_path(team_name):
    path = os.path.join(LOGO_DIR, f"{slugify(team_name)}.png")
    return path if os.path.exists(path) else DEFAULT_LOGO

# ----------------------------
# 4️⃣ STYLING
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #001f3f 0%, #004080 50%, #0074D9 100%);
    color: white;
    font-family: 'Poppins', sans-serif;
}
h1 {
    text-align: center;
    font-weight: 700;
    color: #FFD700;
    text-shadow: 2px 2px 10px #000;
}
.card {
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.4);
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    transition: all 0.3s ease-in-out;
}
.card:hover {
    transform: scale(1.02);
    box-shadow: 0 0 25px rgba(255,255,255,0.4);
}
.team-block {
    text-align: center;
    padding: 10px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 20px;
}
.progress-container {
    background-color: rgba(255,255,255,0.15);
    border-radius: 10px;
    margin-top: -10px;
    height: 30px;
}
.progress-bar {
    height: 30px;
    border-radius: 10px;
    color: white;
    text-align: center;
    font-weight: bold;
    line-height: 30px;
    transition: width 0.6s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# 5️⃣ HEADER
# ----------------------------
st.image(team_logo_path("ipl_logo"), width=180)
st.markdown("<h1>🏏 IPL Win Predictor</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border:2px solid #FFD700;width:80%;margin:auto;'>", unsafe_allow_html=True)

# ----------------------------
# 6️⃣ INPUT SECTION
# ----------------------------
#st.markdown("<div class='card'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox("Select Batting Team", sorted(teams))
with col2:
    bowling_team = st.selectbox("Select Bowling Team", sorted(teams))
    
st.markdown(f"""
<div class='card' style='text-align:center; font-size:22px; font-weight:700;'>
    <span style='color:{TEAM_COLORS[batting_team]}'>{batting_team}</span>
    <span style='color:#FFD700; margin:0 15px;'>VS</span>
    <span style='color:{TEAM_COLORS[bowling_team]}'>{bowling_team}</span>
</div>
""", unsafe_allow_html=True)


selected_city = st.selectbox("Select Host City", sorted(cities))
target = st.number_input("Target Score", min_value=0, max_value=500, value=160)

col3, col4, col5 = st.columns(3)
with col3:
    score = st.number_input("Current Score", min_value=0, max_value=500, value=80)
with col4:
    overs = st.number_input("Overs Completed", min_value=0.0, max_value=20.0, value=10.0, step=0.1)
with col5:
    wickets_out = st.number_input("Wickets Out", min_value=0, max_value=10, value=3)
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# 7️⃣ PREDICTION LOGIC
# ----------------------------
if st.button("🔮 Predict Probability"):
    runs_left = target - score
    balls_left = int(120 - (overs * 6))
    wickets_left = 10 - wickets_out
    crr = score / overs if overs > 0 else 0
    rrr = (runs_left * 6 / balls_left) if balls_left > 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_city],
        'runs_left': [runs_left],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'total_runs_x': [target],
        'crr': [crr],
        'rrr': [rrr]
    })

    try:
        pipe = pickle.load(open("pipe.pkl", "rb"))
        result = pipe.predict_proba(input_df)
        win = result[0][1]
        loss = result[0][0]

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            st.image(team_logo_path(batting_team), width=130)
            st.markdown(f"<div class='team-block' style='background-color:{TEAM_COLORS[batting_team]}'>{batting_team}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='progress-container'>
                <div class='progress-bar' style='width:{win*100}%; background:linear-gradient(90deg, {TEAM_COLORS[batting_team]}, #fff);'>
                    {round(win*100)}%
                </div>
            </div>""", unsafe_allow_html=True)

        with col2:
            st.image(team_logo_path(bowling_team), width=130)
            st.markdown(f"<div class='team-block' style='background-color:{TEAM_COLORS[bowling_team]}'>{bowling_team}</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='progress-container'>
                <div class='progress-bar' style='width:{loss*100}%; background:linear-gradient(90deg, {TEAM_COLORS[bowling_team]}, #fff);'>
                    {round(loss*100)}%
                </div>
            </div>""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
