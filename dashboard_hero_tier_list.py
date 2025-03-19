import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd

# Dashboard title and instructions
st.title("Marvel Champions Hero Tier List")
st.markdown("Adjust the sliders based on how much you value each aspect of hero strength to create your own custom tier list.")

# Create sliders for each weighting parameter
economy = st.slider("Economy", min_value=-20, max_value=20, value=4)
tempo = st.slider("Tempo", min_value=-20, max_value=20, value=2)
card_value = st.slider("Card Value", min_value=-20, max_value=20, value=2)
survivability = st.slider("Survivability", min_value=-20, max_value=20, value=2)
villain_damage = st.slider("Villain Damage", min_value=-20, max_value=20, value=1)
threat_removal = st.slider("Threat Removal", min_value=-20, max_value=20, value=2)
reliability = st.slider("Reliability", min_value=-20, max_value=20, value=3)
minion_control = st.slider("Minion Control", min_value=-20, max_value=20, value=1)
control = st.slider("Control", min_value=-20, max_value=20, value=2)
support = st.slider("Support", min_value=-20, max_value=20, value=2)
unique_builds = st.slider("Unique Broken Builds", min_value=-20, max_value=20, value=1)
late_game = st.slider("Late Game Power", min_value=-20, max_value=20, value=1)
simplicity = st.slider("Simplicity", min_value=-20, max_value=20, value=0)
status_cards = st.slider("Stun/Confuse", min_value=-20, max_value=20, value=0)
multiplayer_consistency = st.slider("Multiplayer Consistency", min_value=-20, max_value=20, value=0)

# Create the weighting array (ensure it matches your hero stat length of 15)
weighting = np.array([
    economy, tempo, card_value, survivability, villain_damage,
    threat_removal, reliability, minion_control, control, support,
    unique_builds, late_game, simplicity, status_cards, multiplayer_consistency
])

# Define your heroes dictionary (each hero's array must have 15 elements)
heroes = {
    "Captain Marvel":       np.array([ 4, 3, -1, 3, 4, 2, 4, 1, 1, 2, 0, 0, 5, 1, 0]),
    "Iron Man":             np.array([ 4, -5, 4, 2, 5, 2, 0, 3, 0, 0, 1, 4, -5, 0, 5]),
    "Spider-Man Peter":     np.array([ 4, 0, 3, 5, 3, -2, 2, 0, 4, 1, 2, 0, 0, 0, 0]),
    "Black Panther":        np.array([ 3, -1, 4, 3, 3, 1, 1, 5, 0, 0, 0, 3, -1, 0, 0]),
    "She-Hulk":             np.array([ 1, 3, -3, 3, 4, -2, 0, 4, 1, 0, 1, 0, -3, 1, 0]),
    "Captain America":      np.array([ 4, 4, 3, 3, 3, 4, 5, 5, 1, 1, 0, 0, 5, 2, 0]),
    "Ms. Marvel":           np.array([ 3, -2, 1, 3, 0, 3, 3, 1, 0, 0, 3, 3, 0, 0, 0]),
    "Thor":                 np.array([ 2, -4, -4, 3, 3, -1, -2, 5, -1, 0, 1, 0, 3, 0, 2]),
    "Black Widow":          np.array([ 2, 0, 3, -2, -4, 3, 2, 3, 4, 0, 0, 0, -5, 4, 0]),
    "Doctor Strange":       np.array([ 4, 3, 5, 4, 2, 5, 5, 0, 5, 5, 5, 5, 3, 5, 4]),
    "Hulk":                 np.array([-3, 5, -2, 4, 4, -5, -5, 3, 0, 0, 1, 0, 2, 0, 0]),
    "Hawkeye":              np.array([ 1, -1, 4, -3, 2, 1, -2, 5, 3, 0, 0, 0, -3, 5, 0]),
    "Spider-Woman":         np.array([ 3, 3, 4, 3, 2, 4, 3, 2, 3, 1, 2, 0, -3, 5, 0]),
    "Ant-Man":              np.array([ 2, 0, 3, 3, 4, 1, 2, 4, 2, 0, 0, 2, -3, 1, 0]),
    "Wasp":                 np.array([ 1, 3, 0, 1, 4, 2, 3, 4, 0, 1, 1, 0, -5, 0, 0]),
    "Quicksilver":          np.array([ 1, -3, 3, -1, 3, 4, 3, 3, 0, 1, 0, 3, 0, 0, 0]),
    "Scarlet Witch":        np.array([ 2, 3, 5, 3, 3, 2, 3, 1, 3, 4, 1, 0, -3, 2, 0]),
    "Star-Lord":            np.array([ 4, 5, 3, 1, 5, 3, 2, 3, -3, 0, 1, 0, -5, 0, 0]),
    "Groot":                np.array([ 0, -3, 2, 4, 3, 2, -2, 2, 0, 3, 0, 1, 2, 0, 0]),
    "Rocket":               np.array([ 3, -1, 0, 0, -2, 2, -2, 4, 0, 0, 1, 1, -3, 0, 0]),
    "Gamora":               np.array([ 1, 4, 3, 1, 3, 4, 4, 3, 0, 0, 1, 0, 3, 0, 0]),
    "Drax":                 np.array([ 2, -3, 4, 2, 4, -1, -5, 3, 0, 1, 1, 0, -2, 0, 0]),
    "Venom (Flash)":        np.array([ 3, 2, 4, 3, 3, 4, 5, 5, 3, 0, 0, 1, -3, 5, 0]),
    "Spectrum":             np.array([ 3, 3, 2, 2, 2, 3, -2, 3, 0, 0, 2, 0, -5, 0, 0]),
    "Adam Warlock":         np.array([ 3, -3, 2, 3, 2, 4, -1, 1, 3, 2, 3, 2, -5, 0, 0]),
    "Nebula":               np.array([ 2, 1, 2, 1, -3, 2, 3, 1, 1, 0, 0, 0, -5, 0, 0]),
    "War Machine":          np.array([ 1, -2, 1, 2, 4, 0, -2, 5, 0, 0, 0, 1, -3, 0, 0]),
    "Valkyrie":             np.array([ 1, 3, -2, 2, 2, 0, -1, 4, 0, 0, 0, 0, -3, 0, 0]),
    "Vision":               np.array([ 2, 3, 3, 3, 4, 3, 4, 2, 2, 0, 1, 0, 0, 1, 0]),
}

# Define the weighting function
def weight(hero, weighting):
    return np.dot(hero, weighting)

# Calculate scores and sort heroes by score
scores = {hero: weight(stats, weighting) for hero, stats in heroes.items()}
sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1]))

# Calculate statistics for tier assignments
hero_scores = np.array(list(scores.values()))
mean_score = np.mean(hero_scores)
std_score = np.std(hero_scores)
threshold_S = mean_score + 1.5 * std_score
threshold_A = mean_score + 0.5 * std_score
threshold_B_lower = mean_score - 0.5 * std_score
threshold_C = mean_score - 1.5 * std_score

tiers = {"S": [], "A": [], "B": [], "C": [], "D": []}
for hero, score in scores.items():
    if score >= threshold_S:
        tiers["S"].append((hero, score))
    elif score >= threshold_A:
        tiers["A"].append((hero, score))
    elif score >= threshold_B_lower:
        tiers["B"].append((hero, score))
    elif score >= threshold_C:
        tiers["C"].append((hero, score))
    else:
        tiers["D"].append((hero, score))

for tier in tiers:
    tiers[tier] = sorted(tiers[tier], key=lambda x: x[1], reverse=True)

# Create a mapping from hero to tier for coloring
hero_to_tier = {}
for tier, heroes_list in tiers.items():
    for hero, _ in heroes_list:
        hero_to_tier[hero] = tier

# Define tier colors
tier_colors = {"S": "red", "A": "orange", "B": "green", "C": "blue", "D": "purple"}

# Prepare sorted hero names, scores, and colors for plotting
sorted_hero_names = list(sorted_scores.keys())
sorted_hero_scores = list(sorted_scores.values())
bar_colors = [tier_colors[hero_to_tier[hero]] for hero in sorted_hero_names]

# Plotting the tier list
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
bars = ax.bar(sorted_hero_names, sorted_hero_scores, color=bar_colors)
ax.set_ylabel("Scores", fontsize="x-large")
ax.set_title("Generalized Hero Power Ranking", fontweight='bold', fontsize=18)
plt.xticks(rotation=45, ha='right')

# Set tick label colors to match hero tiers
for label in ax.get_xticklabels():
    hero = label.get_text()
    if hero in hero_to_tier:
        label.set_color(tier_colors[hero_to_tier[hero]])

# Legend
legend_handles = [Patch(color=tier_colors[tier], label=f"Tier {tier}") for tier in tier_colors]
ax.legend(handles=legend_handles, title="Tier Colors", loc="upper left",
          fontsize='x-large', title_fontsize='x-large')

ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

# ----------------------------------------------------------------
# Advanced: Allow users to customize hero arrays
# Place this section below the plot within an expander to keep it optional.
with st.expander("Edit Hero Values (Advanced)"):
    st.markdown("If you have your own opinions about hero stats, adjust the values below.")
    # Define column headers corresponding to each stat:
    columns = ["Economy", "Tempo", "Card Value", "Survivability", "Villain Damage",
               "Threat Removal", "Reliability", "Minion Control", "Control",
               "Support", "Unique Builds", "Late Game Power", "Simplicity",
               "Stun/Confuse", "Multiplayer Consistency"]
    
    # Convert the heroes dictionary into a DataFrame for editing
    data = {hero: stats.tolist() for hero, stats in heroes.items()}
    df = pd.DataFrame.from_dict(data, orient='index', columns=columns)
    
    # Use Streamlit's experimental data editor to allow changes
    edited_df = st.experimental_data_editor(df, num_rows="dynamic", key="hero_editor")
    
    # Optionally, provide a button to apply the custom hero values
    if st.button("Apply Custom Hero Values"):
        # Update the heroes dictionary with the new values from the DataFrame
        new_heroes = {hero: np.array(edited_df.loc[hero].tolist()) for hero in edited_df.index}
        st.session_state["custom_heroes"] = new_heroes
        st.success("Custom hero values applied! Refresh or rerun the script to update the tier list based on these values.")
