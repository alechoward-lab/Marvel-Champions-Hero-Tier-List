"""
The Living Marvel Champions Tier List
"""
#%%
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import pandas as pd
import copy
import os
from PIL import Image
import json
from hero_image_urls import hero_image_urls
from default_heroes import default_heroes
# ----------------------------------------
# Define preset weighting options so update_preset can use them
# ----------------------------------------
preset_options = {  #          e, t, cv, s, d, th, re, mi, c, su, br, lg, si, sc, mu
    "General Power ~2 Player":              np.array([4, 2, 2, 2, 1, 2, 3, 1, 2, 2, 2, 1, 0, 0, 1]),
    "Multiplayer 3 Player":                 np.array([4, 1, 2, 2, 1, 5, 2, 3, 1, 7, 2, 5, 0, 0, 6]),
    "Multiplayer 4 Player":                 np.array([4, 1, 2, 2, 1, 5, 2, 3, 1, 7, 2, 5, 0, 0, 10]),
    "Solo (No Rush)":                       np.array([8, 3, 2, 4, 2, 2, 4, 1, 2, 2, 2, 1, 0, 4, -7]),
    "Solo Rush":                            np.array([0, 5, 0, 2, 5, 0, 0, 0, 0, 0, 0, -3, 0, 0, 0]),
    "Solo Final Boss Steady/Stalwart":      np.array([10, 3, 3, 8, 6, 2, 2, 4, 1, 2, 2, 2, 1, -4, -7]),
    "Beginner Friendly Heroes":             np.array([2, 1, 0, 1, 0, 0, 5, 0, 0, 0, 0, -1, 10, 1, 0])
}

# ----------------------------------------
# Define update_preset callback early so it is available to the selectbox
# ----------------------------------------
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

# ----------------------------------------
# Early load settings from file if available
# ----------------------------------------
uploaded_file = st.file_uploader("Upload saved settings", type="json", key="upload_settings")
if uploaded_file is not None:
    settings = json.load(uploaded_file)
    st.session_state.heroes = {hero: np.array(stats) for hero, stats in settings["heroes"].items()}
    st.session_state.default_heroes = {hero: np.array(stats) for hero, stats in settings["default_heroes"].items()}
    st.session_state.preset_choice = settings["preset_choice"]
    st.session_state.economy = settings["economy"]
    st.session_state.tempo = settings["tempo"]
    st.session_state.card_value = settings["card_value"]
    st.session_state.survivability = settings["survivability"]
    st.session_state.villain_damage = settings["villain_damage"]
    st.session_state.threat_removal = settings["threat_removal"]
    st.session_state.reliability = settings["reliability"]
    st.session_state.minion_control = settings["minion_control"]
    st.session_state.control = settings["control"]
    st.session_state.support = settings["support"]
    st.session_state.unique_builds = settings["unique_builds"]
    st.session_state.late_game = settings["late_game"]
    st.session_state.simplicity = settings["simplicity"]
    st.session_state.status_cards = settings["status_cards"]
    st.session_state.multiplayer_consistency = settings["multiplayer_consistency"]
    st.session_state.weighting = np.array(settings["weighting"])
    st.success("Settings loaded successfully!")

# ----------------------------------------
# Main App Content
# ----------------------------------------
st.title("The Living Tier List")
st.subheader("For Marvel Champions Heroes by Daring Lime")

st.markdown(
    "Adjust the weighting based on how much you value each aspect of hero strength. "
    "You can choose from preset weighting functions, adjust the sliders manually, or both! "
    "You have full control over the tier list. If a hero has a positive stat, it is a strength, "
    "and if it has a negative stat, it is a weakness. The weighting factors represent how much you "
    "personally value each of those stats. The tier list is automatically calculated based off of the "
    "weighting and hero stats to create a personalized hero tier list. There are a plethora of premade "
    "weighting factors to choose from, as well as a custom option. Any of these weighting functions can "
    "be modified and the tier list will automatically update."
)
st.markdown(
    "For a video tutorial of how to use this, check out my YouTube channel: [Daring Lime](https://www.youtube.com/channel/UCpV2UWmBTAeIKUso1LkeU2A). "
    "There you'll see a full breakdown of each hero and how to use this tool to create your own tier list. "
    "If you enjoy this tool, please consider subscribing to my channel and/or joining as a channel member to support me creating more Marvel Champions content."
)

# ----------------------------------------
# Layout: Two columns side by side
# ----------------------------------------
col1, col2 = st.columns(2)

# ----------------------------------------
# Column 1: Weighting settings (presets and sliders)
# ----------------------------------------
with col1:
    with st.expander("Weighting Factors (click to expand)"):
        st.header("Weighting Factors")
        
        # Category names for the weighting function
        weighting_categories = [
            "Economy", "Tempo", "Card Value", "Survivability", "Villain Damage",
            "Threat Removal", "Reliability", "Minion Control", "Control Boon", "Support Boon",
            "Unique Broken Builds Boon", "Late Game Power Boon", "Simplicity", "Stun/Confuse Boon",
            "Multiplayer Consistency Boon"
        ]
        
        # The selectbox shows the preset options first, then "Custom"
        preset_choice = st.selectbox(
            "Select Weighting Option", 
            list(preset_options.keys()) + ["Custom"],
            key="preset_choice",
            on_change=update_preset
        )
        
        # Always show the sliders so users can adjust
        economy = st.slider("Economy", min_value=-10, max_value=10, value=st.session_state.get("economy", 4), key="economy")
        tempo = st.slider("Tempo", min_value=-10, max_value=10, value=st.session_state.get("tempo", 2), key="tempo")
        card_value = st.slider("Card Value", min_value=-10, max_value=10, value=st.session_state.get("card_value", 2), key="card_value")
        survivability = st.slider("Survivability", min_value=-10, max_value=10, value=st.session_state.get("survivability", 2), key="survivability")
        villain_damage = st.slider("Villain Damage", min_value=-10, max_value=10, value=st.session_state.get("villain_damage", 1), key="villain_damage")
        threat_removal = st.slider("Threat Removal", min_value=-10, max_value=10, value=st.session_state.get("threat_removal", 2), key="threat_removal")
        reliability = st.slider("Reliability", min_value=-10, max_value=10, value=st.session_state.get("reliability", 3), key="reliability")
        minion_control = st.slider("Minion Control", min_value=-10, max_value=10, value=st.session_state.get("minion_control", 1), key="minion_control")
        control = st.slider("Control Boon", min_value=-10, max_value=10, value=st.session_state.get("control", 2), key="control")
        support = st.slider("Support Boon", min_value=-10, max_value=10, value=st.session_state.get("support", 2), key="support")
        unique_builds = st.slider("Unique Broken Builds Boon", min_value=-10, max_value=10, value=st.session_state.get("unique_builds", 1), key="unique_builds")
        late_game = st.slider("Late Game Power Boon", min_value=-10, max_value=10, value=st.session_state.get("late_game", 1), key="late_game")
        simplicity = st.slider("Simplicity", min_value=-10, max_value=10, value=st.session_state.get("simplicity", 0), key="simplicity")
        status_cards = st.slider("Stun/Confuse Boon", min_value=-10, max_value=10, value=st.session_state.get("status_cards", 0), key="status_cards")
        multiplayer_consistency = st.slider("Multiplayer Consistency Boon", min_value=-10, max_value=10, value=st.session_state.get("multiplayer_consistency", 0), key="multiplayer_consistency")
        
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
    with st.expander("Hero Stats (click to expand)"):
        st.header("Hero Stats")
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

# ----------------------------------------
# Settings Save Functionality
# ----------------------------------------
st.header("Save Your Settings")
if st.button("Save Settings"):
    settings = {
        "heroes": {hero: stats.tolist() for hero, stats in st.session_state.heroes.items()},
        "default_heroes": {hero: stats.tolist() for hero, stats in st.session_state.default_heroes.items()},
        "preset_choice": st.session_state.preset_choice,
        "weighting": weighting.tolist(),
        "economy": st.session_state.economy,
        "tempo": st.session_state.tempo,
        "card_value": st.session_state.card_value,
        "survivability": st.session_state.survivability,
        "villain_damage": st.session_state.villain_damage,
        "threat_removal": st.session_state.threat_removal,
        "reliability": st.session_state.reliability,
        "minion_control": st.session_state.minion_control,
        "control": st.session_state.control,
        "support": st.session_state.support,
        "unique_builds": st.session_state.unique_builds,
        "late_game": st.session_state.late_game,
        "simplicity": st.session_state.simplicity,
        "status_cards": st.session_state.status_cards,
        "multiplayer_consistency": st.session_state.multiplayer_consistency
    }
    settings_json = json.dumps(settings)
    st.download_button("Download Settings", settings_json, "settings.json")
st.markdown("After adjusting the heroes and weighting, you can save your settings to a file. "
            "This file can be uploaded later to restore your settings and view your personalized tier list."
            "Upload your saved file at the top of the page to restore your settings. In order to change the sliders again, you must close the settings file by clicking the 'x'.")
# ----------------------------------------
# Continue with tier list calculations and display
# ----------------------------------------

# Use the current hero stats from session state.
heroes = st.session_state.heroes

# Define the path to the hero images (update the path accordingly)
hero_images_path = "C:/Users/user/Desktop/MC_Code/MC_github/Marvel-Champions-Hero-Tier-List/images/heroes"

# Load hero images
hero_images = {}
for hero in default_heroes.keys():
    image_path = os.path.join(hero_images_path, f"{hero.replace(' ', '_').replace('.', '').replace('(', '').replace(')', '').lower()}.png")
    if os.path.exists(image_path):
        hero_images[hero] = Image.open(image_path)
    else:
        hero_images[hero] = None

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

# ----------------------------------------
# Add background image with a semi-transparent black overlay using custom CSS
# ----------------------------------------
background_image_url = "https://raw.githubusercontent.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/refs/heads/main/images/background/marvel_champions_background_image.jpg"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url({background_image_url});
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        position: relative;
        padding: 40px;
        color: white;
    }}
    .stApp::before {{
        content: "";
        position: absolute;
        inset: 40px;
        background: rgba(0, 0, 0, 0.8);
        z-index: 1;
    }}
    .stApp > div {{
        position: relative;
        z-index: 2;
    }}
    .stApp, .stApp * {{
        color: white !important;
    }}
    .stApp .stSelectbox div[role="listbox"] * {{
        color: black !important;
    }}
    </style>
    """, 
    unsafe_allow_html=True
)

# ----------------------------------------
# Display Tier List with Images
# ----------------------------------------
st.header(f"Hero Tier List - {plot_title}")

tier_colors = {"S": "red", "A": "orange", "B": "green", "C": "blue", "D": "purple"}

for tier in ["S", "A", "B", "C", "D"]:
    st.markdown(f"<h2>{tier}</h2>", unsafe_allow_html=True)
    num_cols = 5  # Number of columns per row
    rows = [tiers[tier][i:i + num_cols] for i in range(0, len(tiers[tier]), num_cols)]
    for row in rows:
        cols = st.columns(num_cols)
        for idx, (hero, score) in enumerate(row):
            with cols[idx]:
                if hero in hero_image_urls:
                    st.image(hero_image_urls[hero], width=150)
    #st.markdown("<hr>", unsafe_allow_html=True)

# ----------------------------------------
# Plotting
# ----------------------------------------
st.header("Hero Scores")

sorted_hero_names = list(sorted_scores.keys())
sorted_hero_scores = list(sorted_scores.values())
bar_colors = [tier_colors[hero_to_tier[hero]] for hero in sorted_hero_names]

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
plt.tight_layout()
ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)
st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    "The stats for the heroes were determined by the merits of their identity specific cards. Due to the nature of their kits, Maria Hill and Cyclops had to be considered slightly differently. Depending on your build, these heroes can become significantly more powerful."
)

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Most card images are from the Cerebro Discord bot developed by UnicornSnuggler. Thank you!")

