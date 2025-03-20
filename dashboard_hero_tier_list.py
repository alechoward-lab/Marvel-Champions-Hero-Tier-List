"""
Dashboard version of the tier list.
"""
#%%
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import copy

# Callback function to update slider values when a preset is selected
def update_preset():
    preset = st.session_state.preset_choice
    if preset != "Custom":
        preset_vals = preset_options[preset]
        st.session_state["economy"] = int(preset_vals[0])
        st.session_state["tempo"] = int(preset_vals[1])
        st.session_state["card_value"] = int(preset_vals[2])
        st.session_state["survivability"] = int(preset_vals[3])
        st.session_state["villain_damage"] = int(preset_vals[4])
        st.session_state["threat_removal"] = int(preset_vals[5])
        st.session_state["reliability"] = int(preset_vals[6])
        st.session_state["minion_control"] = int(preset_vals[7])
        st.session_state["control"] = int(preset_vals[8])
        st.session_state["support"] = int(preset_vals[9])
        st.session_state["unique_builds"] = int(preset_vals[10])
        st.session_state["late_game"] = int(preset_vals[11])
        st.session_state["simplicity"] = int(preset_vals[12])
        st.session_state["status_cards"] = int(preset_vals[13])
        st.session_state["multiplayer_consistency"] = int(preset_vals[14])


st.title("Marvel Champions Hero Tier List")
st.markdown(
    "Adjust the weighting based on how much you value each aspect of hero strength. "
    "You can choose from preset weighting functions, "
    "adjust the sliders manually, "
    "or both! You have full control over the tier list. "
    "If a hero has a positive stat, it is a strength, and if it has a negative stat, it is a weakness. "
    "The weighting factors represent how much you personally value each of those stats. "
    "The tier list is automatically calculated based off of the weighting and hero stats to create a personalized hero tier list."
)
st.markdown(
    "For a video tutorial of how to use this, check out my youtube channel: [Daring Lime](https://www.youtube.com/channel/UCpV2UWmBTAeIKUso1LkeU2A). "
    "There you'll see a full breakdown of each hero and how to use this tool to create your own tier list."
)

# ----------------------------------------
# Layout: Two columns side by side
# ----------------------------------------
col1, col2 = st.columns(2)

# ----------------------------------------
# Column 1: Weighting settings (presets and sliders)
# ----------------------------------------
with col1:
    st.header("Weighting Factors")
    
    # Define preset weighting functions
    preset_options = {
        "General Power ~2 Player":              np.array([ 4, 2, 2, 2, 1, 2, 3, 1, 2, 2, 2, 1, 0, 0, 0]),
        "Multiplayer 3/4 Player":               np.array([ 4, 1, 2, 2, 1, 2, 3, 3, 1, 7, 2, 4, 0, 0, 8]),
        "Solo (No Rush)":                       np.array([ 8, 3, 2, 4, 2, 2, 4, 1, 2, 2, 2, 1, 0, 4,-7]),
        "Solo Rush":                            np.array([ 0, 5, 0, 2, 5, 0, 0, 0, 0, 0, 0,-3, 0, 0, 0]),
        "Solo Final Boss Steady/Stalwart":      np.array([10, 3, 3, 8, 6, 2, 2, 4, 1, 2, 2, 2, 1,-4,-7]),
        "Beginner Friendly Heroes":             np.array([ 1, 0, 1, 1, 0, 0, 5, 0, 0, 0, 0,-1,10, 0, 0])
    }
    
    # Category names for the weighting function
    weighting_categories = [
        "Economy", "Tempo", "Card Value", "Survivability", "Villain Damage",
        "Threat Removal", "Reliability", "Minion Control", "Control", "Support",
        "Unique Broken Builds", "Late Game Power", "Simplicity", "Stun/Confuse",
        "Multiplayer Consistency"
    ]
    
    # The selectbox shows the preset options first, then "Custom"
    preset_choice = st.selectbox(
        "Select Weighting Option", 
        list(preset_options.keys()) + ["Custom"],
        key="preset_choice",
        on_change=update_preset
    )
    
    # If a preset (other than "Custom") is selected, display a table mapping categories to values.
    if preset_choice != "Custom":
        st.markdown(f"**Preset: {preset_choice}**")
        df = pd.DataFrame({
            "Category": weighting_categories,
            "Value": preset_options[preset_choice]
        })
        st.table(df)
    
    # Always show the sliders so users can adjust
    economy =                   st.slider("Economy",                    min_value=-10, max_value=10, value=st.session_state.get("economy", 4), key="economy")
    tempo =                     st.slider("Tempo",                      min_value=-10, max_value=10, value=st.session_state.get("tempo", 2), key="tempo")
    card_value =                st.slider("Card Value",                 min_value=-10, max_value=10, value=st.session_state.get("card_value", 2), key="card_value")
    survivability =             st.slider("Survivability",              min_value=-10, max_value=10, value=st.session_state.get("survivability", 2), key="survivability")
    villain_damage =            st.slider("Villain Damage",             min_value=-10, max_value=10, value=st.session_state.get("villain_damage", 1), key="villain_damage")
    threat_removal =            st.slider("Threat Removal",             min_value=-10, max_value=10, value=st.session_state.get("threat_removal", 2), key="threat_removal")
    reliability =               st.slider("Reliability",                min_value=-10, max_value=10, value=st.session_state.get("reliability", 3), key="reliability")
    minion_control =            st.slider("Minion Control",             min_value=-10, max_value=10, value=st.session_state.get("minion_control", 1), key="minion_control")
    control =                   st.slider("Control",                    min_value=-10, max_value=10, value=st.session_state.get("control", 2), key="control")
    support =                   st.slider("Support",                    min_value=-10, max_value=10, value=st.session_state.get("support", 2), key="support")
    unique_builds =             st.slider("Unique Broken Builds",       min_value=-10, max_value=10, value=st.session_state.get("unique_builds", 1), key="unique_builds")
    late_game =                 st.slider("Late Game Power",            min_value=-10, max_value=10, value=st.session_state.get("late_game", 1), key="late_game")
    simplicity =                st.slider("Simplicity",                 min_value=-10, max_value=10, value=st.session_state.get("simplicity", 0), key="simplicity")
    status_cards =              st.slider("Stun/Confuse",               min_value=-10, max_value=10, value=st.session_state.get("status_cards", 0), key="status_cards")
    multiplayer_consistency =   st.slider("Multiplayer Consistency",    min_value=-10, max_value=10, value=st.session_state.get("multiplayer_consistency", 0), key="multiplayer_consistency")
    
    # Create the weighting array from slider values
    weighting = np.array([
        st.session_state.get("economy", 4),
        st.session_state.get("tempo", 2),
        st.session_state.get("card_value", 2),
        st.session_state.get("survivability", 2),
        st.session_state.get("villain_damage", 1),
        st.session_state.get("threat_removal", 2),
        st.session_state.get("reliability", 3),
        st.session_state.get("minion_control", 1),
        st.session_state.get("control", 2),
        st.session_state.get("support", 2),
        st.session_state.get("unique_builds", 1),
        st.session_state.get("late_game", 1),
        st.session_state.get("simplicity", 0),
        st.session_state.get("status_cards", 0),
        st.session_state.get("multiplayer_consistency", 0)
    ])
    
    # Determine the plot title based on preset selection
    if preset_choice != "Custom":
        plot_title = f"{preset_choice}"
    else:
        plot_title = "Custom Weighting"

# ----------------------------------------
# Column 2: Hero Stat Modification
# ----------------------------------------
with col2:
    st.header("Hero Stats")
    
    # Define default hero stats dictionary
    default_heroes = {
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
    
    # Initialize hero stats in session state if not already set
    if "heroes" not in st.session_state:
        st.session_state.heroes = copy.deepcopy(default_heroes)
        st.session_state.default_heroes = copy.deepcopy(default_heroes)
    
    # List of stat names corresponding to each index in the hero arrays
    stat_names = ["Economy", "Tempo", "Card Value", "Survivability", "Villain Damage",
                  "Threat Removal", "Reliability", "Minion Control", "Control Boon", "Support Boon",
                  "Unique Broken Builds Boon", "Late Game Power Boon", "Simplicity", "Stun/Confuse Boon",
                  "Multiplayer Consistency Boon"]
    
    # Select a hero to modify
    hero_to_modify = st.selectbox("Select a Hero to Modify", list(st.session_state.heroes.keys()), key="hero_choice")
    
    # Get the current stats for the selected hero
    current_stats = st.session_state.heroes[hero_to_modify]
    new_stats = []
    for i, stat in enumerate(stat_names):
        val = st.number_input(f"{hero_to_modify} - {stat}", value=int(current_stats[i]), min_value=-10, max_value=10, key=f"{hero_to_modify}_{stat}")
        new_stats.append(val)
    
    # Button to update the selected hero's stats
    if st.button(f"Update {hero_to_modify} Stats"):
        st.session_state.heroes[hero_to_modify] = np.array(new_stats)
        st.success(f"{hero_to_modify} stats updated.")
    
    # Button to reset only the selected hero to default
    if st.button(f"Reset {hero_to_modify} to Default"):
        st.session_state.heroes[hero_to_modify] = st.session_state.default_heroes[hero_to_modify]
        st.success(f"{hero_to_modify} stats reset to default.")
    
    # Button to reset all heroes to default
    if st.button("Reset All Heroes to Default"):
        st.session_state.heroes = copy.deepcopy(st.session_state.default_heroes)
        st.success("All heroes have been reset to their default stats.")

# Use the current hero stats from session state.
heroes = st.session_state.heroes

# ----------------------------------------
# Calculate Scores and Tiers using weighting and hero stats
# ----------------------------------------
def weight(hero, weighting):
    return np.dot(hero, weighting)

scores = {hero: weight(stats, weighting) for hero, stats in heroes.items()}
sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1]))

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

hero_to_tier = {}
for tier, heroes_list in tiers.items():
    for hero, _ in heroes_list:
        hero_to_tier[hero] = tier

tier_colors = {"S": "red", "A": "orange", "B": "green", "C": "blue", "D": "purple"}

sorted_hero_names = list(sorted_scores.keys())
sorted_hero_scores = list(sorted_scores.values())
bar_colors = [tier_colors[hero_to_tier[hero]] for hero in sorted_hero_names]

# ----------------------------------------
# Plotting
# ----------------------------------------
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)
bars = ax.bar(sorted_hero_names, sorted_hero_scores, color=bar_colors)
ax.set_ylabel("Scores", fontsize="x-large")
ax.set_title(plot_title, fontweight='bold', fontsize=18)
plt.xticks(rotation=45, ha='right')

for label in ax.get_xticklabels():
    hero = label.get_text()
    if hero in hero_to_tier:
        label.set_color(tier_colors[hero_to_tier[hero]])

legend_handles = [Patch(color=tier_colors[tier], label=f"Tier {tier}") for tier in tier_colors]
ax.legend(handles=legend_handles, title="Tier Colors", loc="upper left",
          fontsize='x-large', title_fontsize='x-large')

ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)
#%%

# Add background image with a semi-transparent black overlay using custom CSS
background_image_url = "https://raw.githubusercontent.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/refs/heads/main/images/background/marvel_champions_background_image.jpg"  # Replace with your image file path or URL

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({background_image_url});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: relative;
        padding: 40px;  /* Add padding to create a margin */
        color: white;  /* Set text color to white */
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        inset: 40px;  /* Adjust to match the padding */
        background: rgba(0, 0, 0, 0.8);  /* More opaque black overlay */
        z-index: 1;
    }}
    .stApp > div {{
        position: relative;
        z-index: 2;
    }}
    /* Set all text to white */
    .stApp, .stApp * {{
        color: white !important;
    }}
    /* Exclude dropdown menu text */
    .stApp .stSelectbox div[role="listbox"] * {{
        color: black !important;
    }}
    </style>
    """, 
    unsafe_allow_html=True
)
