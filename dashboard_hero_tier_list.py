"""
Dashboard version of the tier list.
"""
#%%
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import copy

# ----------------------------------------
# Weighting sliders (for overall weighting factors)
# ----------------------------------------
st.title("Marvel Champions Hero Tier List")
st.markdown("Adjust the sliders based on how much you value each aspect of hero strength to create your own custom tier list.")

economy = st.slider("Economy", min_value=-10, max_value=10, value=4)
tempo = st.slider("Tempo", min_value=-10, max_value=10, value=2)
card_value = st.slider("Card Value", min_value=-10, max_value=10, value=2)
survivability = st.slider("Survivability", min_value=-10, max_value=10, value=2)
villain_damage = st.slider("Villain Damage", min_value=-10, max_value=10, value=1)
threat_removal = st.slider("Threat Removal", min_value=-10, max_value=10, value=2)
reliability = st.slider("Reliability", min_value=-10, max_value=10, value=3)
minion_control = st.slider("Minion Control", min_value=-10, max_value=10, value=1)
control = st.slider("Control", min_value=-10, max_value=10, value=2)
support = st.slider("Support", min_value=-10, max_value=10, value=2)
unique_builds = st.slider("Unique Broken Builds", min_value=-10, max_value=10, value=1)
late_game = st.slider("Late Game Power", min_value=-10, max_value=10, value=1)
simplicity = st.slider("Simplicity", min_value=-10, max_value=10, value=0)
status_cards = st.slider("Stun/Confuse", min_value=-10, max_value=10, value=0)
multiplayer_consistency = st.slider("Multiplayer Consistency", min_value=-10, max_value=10, value=0)

# Create the weighting array (ensure it matches your hero stats length)
weighting = np.array([economy, tempo, card_value, survivability, villain_damage,
                      threat_removal, reliability, minion_control, control, support,
                      unique_builds, late_game, simplicity, status_cards, multiplayer_consistency])

# ----------------------------------------
# Define default hero stats (dictionary)
# ----------------------------------------
default_heroes = {
    # category headers:                    ec te cv s  vd th re m  c  sp b  lg si sc mc   
    "Captain Marvel":       np.array([ 4, 3,-1, 3, 4, 2, 4, 1, 1, 2, 0, 0, 5, 1, 0]),
    "Iron Man":             np.array([ 4,-5, 4, 2, 5, 2, 0, 3, 0, 0, 1, 4,-5, 0, 5]),
    "Spider-Man Peter":     np.array([ 4, 0, 3, 5, 3,-2, 2, 0, 4, 1, 2, 0, 0, 0, 0]),
    "Black Panther":        np.array([ 3,-1, 4, 3, 3, 1, 1, 5, 0, 0, 0, 3,-1, 0, 0]),
    "She-Hulk":             np.array([ 1, 3,-3, 3, 4,-2, 0, 4, 1, 0, 1, 0,-3, 1, 0]),
    "Captain America":      np.array([ 4, 4, 3, 3, 3, 4, 5, 5, 1, 1, 0, 0, 5, 2, 0]),
    "Ms. Marvel":           np.array([ 3,-2, 1, 3, 0, 3, 3, 1, 0, 0, 3, 3, 0, 0, 0]),
    "Thor":                 np.array([ 2,-4,-4, 3, 3,-1,-2, 5,-1, 0, 1, 0, 3, 0, 2]),
    "Black Widow":          np.array([ 2, 0, 3,-2,-4, 3, 2, 3, 4, 0, 0, 0,-5, 4, 0]),
    "Doctor Strange":       np.array([ 4, 3, 5, 4, 2, 5, 5, 0, 5, 5, 5, 5, 3, 5, 4]),
    "Hulk":                 np.array([-3, 5,-2, 4, 4,-5,-5, 3, 0, 0, 1, 0, 2, 0, 0]),
    "Hawkeye":              np.array([ 1,-1, 4,-3, 2, 1,-2, 5, 3, 0, 0, 0,-3, 5, 0]),
    "Spider-Woman":         np.array([ 3, 3, 4, 3, 2, 4, 3, 2, 3, 1, 2, 0,-3, 5, 0]),
    "Ant-Man":              np.array([ 2, 0, 3, 3, 4, 1, 2, 4, 2, 0, 0, 2,-3, 1, 0]),
    "Wasp":                 np.array([ 1, 3, 0, 1, 4, 2, 3, 4, 0, 1, 1, 0,-5, 0, 0]),
    "Quicksilver":          np.array([ 1,-3, 3,-1, 3, 4, 3, 3, 0, 1, 0, 3, 0, 0, 0]),
    "Scarlet Witch":        np.array([ 2, 3, 5, 3, 3, 2, 3, 1, 3, 4, 1, 0,-3, 2, 0]),
    "Star-Lord":            np.array([ 4, 5, 3, 1, 5, 3, 2, 3,-3, 0, 1, 0,-5, 0, 0]),
    "Groot":                np.array([ 0,-3, 2, 4, 3, 2,-2, 2, 0, 3, 0, 1, 2, 0, 0]),
    "Rocket":               np.array([ 3,-1, 0, 0,-2, 2,-2, 4, 0, 0, 1, 1,-3, 0, 0]),
    "Gamora":               np.array([ 1, 4, 3, 1, 3, 4, 4, 3, 0, 0, 1, 0, 3, 0, 0]),
    "Drax":                 np.array([ 2,-3, 4, 2, 4,-1,-5, 3, 0, 1, 1, 0,-2, 0, 0]),
    "Venom (Flash)":        np.array([ 3, 2, 4, 3, 3, 4, 5, 5, 3, 0, 0, 1,-3, 5, 0]),
    "Spectrum":             np.array([ 3, 3, 2, 2, 2, 3,-2, 3, 0, 0, 2, 0,-5, 0, 0]),
    "Adam Warlock":         np.array([ 3,-3, 2, 3, 2, 4,-1, 1, 3, 2, 3, 2,-5, 0, 0]),
    "Nebula":               np.array([ 2, 1, 2, 1,-3, 2, 3, 1, 1, 0, 0, 0,-5, 0, 0]),
    "War Machine":          np.array([ 1,-2, 1, 2, 4, 0,-2, 5, 0, 0, 0, 1,-3, 0, 0]),
    "Valkyrie":             np.array([ 1, 3,-2, 2, 2, 0,-1, 4, 0, 0, 0, 0,-3, 0, 0]),
    "Vision":               np.array([ 2, 3, 3, 3, 4, 3, 4, 2, 2, 0, 1, 0, 0, 1, 0]),
    "Ghost Spider":         np.array([ 3, 3, 3, 3, 3, 2, 2, 2, 4, 1, 1, 0,-3, 0, 0]),
    "Spider-Man (Miles)":   np.array([ 2, 4, 5, 3, 5, 4, 5, 1, 4, 0, 1, 0, 3, 5, 0]),
    "Nova":                 np.array([ 4, 4, 4, 1, 2, 3, 4, 3, 0, 1, 2, 0, 2, 0, 2]),
    "Ironheart":            np.array([ 2,-3, 4, 3, 5, 5, 0, 3, 0, 0, 2, 5,-3, 0, 3]),
    "SP//dr":               np.array([ 2,-1, 5, 3, 3, 5, 0, 1, 1, 0, 2, 2,-5, 0, 0]),
    "Spider-Ham":           np.array([ 5, 3, 4, 5, 2, 4, 5, 2, 4, 0, 2, 1,-1, 5, 0]),
    "Colossus":             np.array([ 1,-1, 4, 5, 3,-5,-2, 2, 4, 0, 0, 0,-3, 5, 0]),
    "Shadowcat":            np.array([ 3, 4, 2, 3, 1, 3, 5, 3, 3, 0, 0, 0,-5, 3, 0]),
    "Cyclops":              np.array([ 1,-2, 5, 3, 4, 4, 3, 3, 0, 2, 2, 1,-3, 0, 0]),
    "Phoenix":              np.array([ 2, 3, 3, 3, 4, 4, 3, 4, 3, 1, 2, 0, 0, 4, 0]),
    "Wolverine":            np.array([ 3, 5, 3, 4, 5, 3, 4, 5, 0, 0, 1, 0, 1, 0, 0]),
    "Storm":                np.array([ 1, 3, 3, 1, 4, 4, 3, 3, 1, 3, 1, 0,-3, 0, 2]),
    "Gambit":               np.array([ 1,-1, 2, 2, 3, 3, 2, 4, 2, 1, 0, 0,-1, 4, 0]),
    "Rogue":                np.array([ 0, 3, 3, 3, 3, 3, 1, 2, 2, 0, 1, 0, 0, 1, 2]),
    "Cable":                np.array([ 2, 3, 4, 3, 3, 5, 5, 2, 3, 3, 2, 3,-5, 0,-5]),
    "Domino":               np.array([ 3,-2, 4, 1, 4, 3, 2, 4, 1, 0, 0, 3,-5, 0, 0]),
    "Psylocke":             np.array([ 4, 4, 4, 1, 1, 5, 4, 3, 5, 0, 2, 0,-3, 5, 0]),
    "Angel":                np.array([ 2, 5, 2, 2, 3, 5, 5, 2, 1, 0, 2, 0,-1, 0, 0]),
    "X-23":                 np.array([ 1, 5, 4, 3, 5, 5, 5, 4, 0, 0, 1, 2,-2, 0, 0]),
    "Deadpool":             np.array([ 1, 5, 5, 5, 5, 5,-3, 2, 1, 3, 1, 0,-1, 1, 0]),
    "Bishop":               np.array([ 5, 2, 4, 4, 5, 1, 3, 2, 0, 0, 1, 1,-3, 0, 0]),
    "Magik":                np.array([ 4, 1, 4, 3, 2, 4, 3, 3, 3, 0, 1, 1,-5, 5, 0]),
    "Iceman":               np.array([ 3, 2, 3, 3, 2, 2, 3, 5, 3, 2, 0, 0, 0, 0, 0]),
    "Jubilee":              np.array([ 3,-1, 4, 0, 2, 4, 3, 3, 4, 1, 0, 1,-1, 5, 0]),
    "Nightcrawler":         np.array([ 1, 2, 3, 3, 0, 3, 4, 4, 1, 3, 0, 0,-1, 1, 0]),
    "Magneto":              np.array([ 3, 3, 3, 4, 3, 4, 5, 4, 2, 0, 0, 1, 3, 0, 1]),
    "Maria Hill":           np.array([ 2, 1, 5, 1, 2, 5, 5, 1, 1, 2, 2, 5,-3, 0, 0]),
    "Nick Fury":            np.array([ 1, 2, 1, 3, 2, 4, 4, 5, 2, 0, 0, 0,-3, 0, 0]),
}

# ----------------------------------------
# Initialize hero stats in session state if not already set
# ----------------------------------------
if "heroes" not in st.session_state:
    st.session_state.heroes = copy.deepcopy(default_heroes)
    st.session_state.default_heroes = copy.deepcopy(default_heroes)

# ----------------------------------------
# Section: Modify Hero Stats
# ----------------------------------------
st.header("Modify Hero-Specific Stats")
# List of stat names corresponding to each index in the hero arrays
stat_names = ["Economy", "Tempo", "Card Value", "Survivability", "Villain Damage",
              "Threat Removal", "Reliability", "Minion Control", "Control", "Support",
              "Unique Broken Builds", "Late Game Power", "Simplicity", "Stun/Confuse",
              "Multiplayer Consistency"]

# Select a hero to modify
hero_to_modify = st.selectbox("Select a Hero to Modify", list(st.session_state.heroes.keys()))

# Get the current stats for the selected hero
current_stats = st.session_state.heroes[hero_to_modify]
new_stats = []
for i, stat in enumerate(stat_names):
    # Use a unique key for each input to maintain state
    val = st.number_input(f"{hero_to_modify} - {stat}", value=int(current_stats[i]), min_value=-10, max_value=10, key=f"{hero_to_modify}_{stat}")
    new_stats.append(val)

# Update the hero's stats when the user clicks the "Update Hero Stats" button
if st.button(f"Update {hero_to_modify} Stats"):
    st.session_state.heroes[hero_to_modify] = np.array(new_stats)
    st.success(f"{hero_to_modify} stats updated.")

# Add a reset button to restore all hero stats to defaults
if st.button("Reset All Hero Stats to Default"):
    st.session_state.heroes = copy.deepcopy(st.session_state.default_heroes)
    st.success("All hero stats have been reset to default.")

# For the rest of the code, use the current hero stats from session state.
heroes = st.session_state.heroes

# ----------------------------------------
# Calculate Scores and Tiers using weighting and hero stats
# ----------------------------------------
# Define your weight function
def weight(hero, weighting):
    return np.dot(hero, weighting)

# Calculate scores
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

# Prepare sorted names, scores, and colors
sorted_hero_names = list(sorted_scores.keys())
sorted_hero_scores = list(sorted_scores.values())
bar_colors = [tier_colors[hero_to_tier[hero]] for hero in sorted_hero_names]

# ----------------------------------------
# Plotting
# ----------------------------------------
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
bars = ax.bar(sorted_hero_names, sorted_hero_scores, color=bar_colors)
ax.set_ylabel("Scores", fontsize="x-large")
ax.set_title("Generalized Hero Power Ranking", fontweight='bold', fontsize=18)
plt.xticks(rotation=45, ha='right')

# Set tick label colors to match tiers
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
#%%
