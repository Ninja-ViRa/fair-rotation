
import streamlit as st
import pandas as pd
import random
import itertools
from collections import defaultdict

st.set_page_config(page_title="Enhanced Badminton Player Rotation", layout="centered")
st.title("🏸 Enhanced Badminton Player Rotation App")

# Initialize session state
if "rotation_count" not in st.session_state:
    st.session_state.rotation_count = 0
if "rotation_history" not in st.session_state:
    st.session_state.rotation_history = []
if "pair_history" not in st.session_state:
    st.session_state.pair_history = defaultdict(int)
if "bench_time" not in st.session_state:
    st.session_state.bench_time = defaultdict(int)
if "court_history" not in st.session_state:
    st.session_state.court_history = defaultdict(list)
if "rest_players" not in st.session_state:
    st.session_state.rest_players = []

# Upload or input player names
uploaded_file = st.file_uploader("Upload CSV or Excel with player names", type=["csv", "xlsx"])
manual_input = st.text_area("Or enter player names (comma-separated)", "")

players = []

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    if "Name" in df.columns:
        players = df["Name"].dropna().tolist()
    else:
        st.error("Please ensure the file has a 'Name' column.")
elif manual_input:
    players = [name.strip() for name in manual_input.split(",") if name.strip()]

# Select present players
if players:
    st.subheader("✅ Select Players Present Today")
    present_players = st.multiselect("Players Present", players, default=players)
else:
    present_players = []

# Input number of courts
num_courts = st.number_input("Enter number of available courts", min_value=1, value=1)

# Select players taking rest
if present_players:
    st.subheader("🛋️ Select Players Taking Rest (Optional)")
    st.session_state.rest_players = st.multiselect("Players on Rest/Break", present_players, default=st.session_state.rest_players)

# Rotation logic with fairness scoring
def generate_rotation(active_players, num_courts, trials=100):
    best_score = float("inf")
    best_courts = []
    best_bench = []

    for _ in range(trials):
        random.shuffle(active_players)
        courts = []
        bench = []
        selected = []
        court_index = 0
        queue = active_players.copy()

        while court_index < num_courts and len(queue) >= 4:
            court_players = queue[:4]
            queue = queue[4:]
            courts.append(court_players)
            selected.extend(court_players)
            court_index += 1

        bench = queue

        # Calculate fairness score
        score = 0
        for court in courts:
            for pair in itertools.combinations(court, 2):
                score += st.session_state.pair_history[tuple(sorted(pair))] * 2  # penalize repeated pairings

        for player in bench:
            score += st.session_state.bench_time[player] * 1.5  # penalize repeated benching

        for i, court in enumerate(courts):
            for player in court:
                if i in st.session_state.court_history[player]:
                    score += 1  # penalize repeated court assignment

        if score < best_score:
            best_score = score
            best_courts = courts
            best_bench = bench

    return best_courts, best_bench

# Display courts
if present_players:
    active_players = [p for p in present_players if p not in st.session_state.rest_players]

if st.button("🔁 Rotate Players"):
    active_players = [p for p in present_players if p not in st.session_state.rest_players]
    st.session_state.rotation_count += 1
    courts, bench = generate_rotation(active_players, num_courts)

    # Update histories
    for court in courts:
        for pair in itertools.combinations(court, 2):
            st.session_state.pair_history[tuple(sorted(pair))] += 1
        for i, player in enumerate(court):
            st.session_state.court_history[player].append(courts.index(court))

    for player in bench:
        st.session_state.bench_time[player] += 1

    st.subheader(f"🎾 Match Rotation #{st.session_state.rotation_count}")
    for i, court in enumerate(courts, 1):
        st.markdown(f"**Court {i}:** {', '.join(court)}")

    if bench:
        st.info(f"🛑 Bench: {', '.join(bench)}")
    if st.session_state.rest_players:
        st.info(f"🛋️ Resting: {', '.join(st.session_state.rest_players)}")

    st.session_state.rotation_history.append({
        "rotation": st.session_state.rotation_count,
        "courts": courts,
        "bench": bench,
        "rest": st.session_state.rest_players.copy()
    })

# Show rotation history
if st.session_state.rotation_history:
    st.subheader("📝 Rotation History")
    for entry in st.session_state.rotation_history:
        st.markdown(f"### Rotation #{entry['rotation']}")
        for i, court in enumerate(entry["courts"], 1):
            st.markdown(f"- Court {i}: {', '.join(court)}")
        if entry["bench"]:
            st.markdown(f"- Bench: {', '.join(entry['bench'])}")
        if entry["rest"]:
            st.markdown(f"- Resting: {', '.join(entry['rest'])}")

# Reset button
if st.button("🔄 Reset Rotation"):
    st.session_state.rotation_count = 0
    st.session_state.rotation_history = []
    st.session_state.pair_history = defaultdict(int)
    st.session_state.bench_time = defaultdict(int)
    st.session_state.court_history = defaultdict(list)
    st.session_state.rest_players = []
