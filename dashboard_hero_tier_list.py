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


st.title("The Living Tier List")
st.subheader("For Marvel Champions Heroes by Daring Lime")

st.markdown(
    "Adjust the weighting based on how much you value each aspect of hero strength. "
    "You can choose from preset weighting functions, "
    "adjust the sliders manually, "
    "or both! You have full control over the tier list. "
    "If a hero has a positive stat, it is a strength, and if it has a negative stat, it is a weakness. "
    "The weighting factors represent how much you personally value each of those stats. "
    "The tier list is automatically calculated based off of the weighting and hero stats to create a personalized hero tier list. "
    "There are a plethora of premade weighting factors to choose from, as well as a custom option. Any of these weighting functions can be modified and the tier list will automatically update."
)
st.markdown(
    "For a video tutorial of how to use this, check out my YouYube channel: [Daring Lime](https://www.youtube.com/channel/UCpV2UWmBTAeIKUso1LkeU2A). "
    "There you'll see a full breakdown of each hero and how to use this tool to create your own tier list."
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
    st.header("Weighting Factors")
    
    # Define preset weighting functions
    preset_options = {                          #          e, t, cv,s, d, th,re,mi,c, su,br,lg,si,sc,mu
        "General Power ~2 Player":              np.array([ 4, 2, 2, 2, 1, 2, 3, 1, 2, 2, 2, 1, 0, 0, 1]),
        "Multiplayer 3 Player":                 np.array([ 4, 1, 2, 2, 1, 5, 2, 3, 1, 7, 2, 5, 0, 0, 6]),
        "Multiplayer 4 Player":                 np.array([ 4, 1, 2, 2, 1, 5, 2, 3, 1, 7, 2, 5, 0, 0, 10]),
        "Solo (No Rush)":                       np.array([ 8, 3, 2, 4, 2, 2, 4, 1, 2, 2, 2, 1, 0, 4,-7]),
        "Solo Rush":                            np.array([ 0, 5, 0, 2, 5, 0, 0, 0, 0, 0, 0,-3, 0, 0, 0]),
        "Solo Final Boss Steady/Stalwart":      np.array([10, 3, 3, 8, 6, 2, 2, 4, 1, 2, 2, 2, 1,-4,-7]),
        "Beginner Friendly Heroes":             np.array([ 2, 1, 0, 1, 0, 0, 5, 0, 0, 0, 0,-1,10, 1, 0])
    }
    
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
    economy =                   st.slider("Economy",                            min_value=-10, max_value=10, value=st.session_state.get("economy", 4), key="economy")
    tempo =                     st.slider("Tempo",                              min_value=-10, max_value=10, value=st.session_state.get("tempo", 2), key="tempo")
    card_value =                st.slider("Card Value",                         min_value=-10, max_value=10, value=st.session_state.get("card_value", 2), key="card_value")
    survivability =             st.slider("Survivability",                      min_value=-10, max_value=10, value=st.session_state.get("survivability", 2), key="survivability")
    villain_damage =            st.slider("Villain Damage",                     min_value=-10, max_value=10, value=st.session_state.get("villain_damage", 1), key="villain_damage")
    threat_removal =            st.slider("Threat Removal",                     min_value=-10, max_value=10, value=st.session_state.get("threat_removal", 2), key="threat_removal")
    reliability =               st.slider("Reliability",                        min_value=-10, max_value=10, value=st.session_state.get("reliability", 3), key="reliability")
    minion_control =            st.slider("Minion Control",                     min_value=-10, max_value=10, value=st.session_state.get("minion_control", 1), key="minion_control")
    control =                   st.slider("Control Boon",                       min_value=-10, max_value=10, value=st.session_state.get("control", 2), key="control")
    support =                   st.slider("Support Boon",                       min_value=-10, max_value=10, value=st.session_state.get("support", 2), key="support")
    unique_builds =             st.slider("Unique Broken Builds Boon",          min_value=-10, max_value=10, value=st.session_state.get("unique_builds", 1), key="unique_builds")
    late_game =                 st.slider("Late Game Power Boon",               min_value=-10, max_value=10, value=st.session_state.get("late_game", 1), key="late_game")
    simplicity =                st.slider("Simplicity",                         min_value=-10, max_value=10, value=st.session_state.get("simplicity", 0), key="simplicity")
    status_cards =              st.slider("Stun/Confuse Boon",                  min_value=-10, max_value=10, value=st.session_state.get("status_cards", 0), key="status_cards")
    multiplayer_consistency =   st.slider("Multiplayer Consistency Boon",       min_value=-10, max_value=10, value=st.session_state.get("multiplayer_consistency", 0), key="multiplayer_consistency")
    
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
    default_heroes = {          #          e, t, cv,s, d, th,re,mi,c, s, br,lg,si,sc,mu  
        "Captain Marvel":       np.array([ 4, 3,-1, 3, 4, 2, 4, 1, 1, 2, 0, 0, 5, 1, 1]),
        "Iron Man":             np.array([ 4,-5, 4, 2, 5, 2, 0, 3, 0, 0, 1, 4,-5, 0, 5]),
        "Spider-Man Peter":     np.array([ 4, 0, 3, 5, 3,-2, 2, 0, 4, 1, 2, 0, 0, 0, 0]),
        "Black Panther":        np.array([ 3,-1, 4, 3, 3, 1, 1, 5, 0, 0, 0, 3,-1, 0, 1]),
        "She-Hulk":             np.array([ 1, 3,-3, 3, 4,-2, 0, 4, 1, 0, 1, 0,-3, 1, 1]),
        "Captain America":      np.array([ 4, 4, 3, 3, 3, 4, 5, 5, 1, 1, 0, 0, 5, 2, 0]),
        "Ms. Marvel":           np.array([ 3,-2, 1, 3, 0, 3, 3, 1, 0, 0, 3, 3, 0, 0, 0]),
        "Thor":                 np.array([ 2,-4,-4, 3, 3,-1,-2, 5,-1, 0, 1, 0, 3, 0, 2]),
        "Black Widow":          np.array([ 2, 0, 3,-2,-4, 3, 2, 3, 4, 0, 0, 0,-5, 4, 1]),
        "Doctor Strange":       np.array([ 4, 3, 5, 4, 2, 5, 5, 0, 5, 5, 5, 5, 3, 5, 4]),
        "Hulk":                 np.array([-3, 5,-2, 4, 4,-5,-5, 3, 0, 0, 1, 0, 2, 0, 0]),
                                #          e, t, cv,s, d, th,re,mi,c, s, br,lg,si,sc,mu  
        "Hawkeye":              np.array([ 1,-1, 4,-3, 2, 1,-2, 5, 3, 0, 0, 0,-3, 5, 0]),
        "Spider-Woman":         np.array([ 3, 3, 4, 3, 2, 4, 3, 2, 3, 1, 2, 0,-3, 5, 0]),
        "Ant-Man":              np.array([ 2, 0, 3, 3, 4, 1, 2, 4, 2, 0, 0, 2,-3, 1, 0]),
        "Wasp":                 np.array([ 1, 3, 0, 1, 4, 2, 3, 4, 0, 1, 1, 0,-5, 0, 0]),
        "Quicksilver":          np.array([ 1,-3, 3,-1, 3, 4, 3, 3, 0, 1, 0, 3, 0, 0, 0]),
        "Scarlet Witch":        np.array([ 2, 3, 5, 3, 3, 2, 3, 1, 3, 4, 1, 0,-3, 2, 0]),
                                #          e, t, cv,s, d, th,re,mi,c, s, br,lg,si,sc,mu          
        "Star-Lord":            np.array([ 4, 5, 3, 1, 5, 3, 2, 3,-3, 0, 1, 0,-5, 0, 0]),
        "Groot":                np.array([ 0,-3, 2, 4, 3, 2,-2, 2, 0, 3, 0, 1, 2, 0, 2]),
        "Rocket":               np.array([ 3,-1, 0, 0,-2, 2,-2, 4, 0, 0, 1, 1,-3, 0, 1]),
        "Gamora":               np.array([ 1, 4, 3, 1, 3, 4, 4, 3, 0, 0, 1, 0, 3, 0, 0]),
        "Drax":                 np.array([ 2,-3, 4, 2, 4,-1,-5, 3, 0, 1, 1, 0,-2, 0, 0]),
        "Venom (Flash)":        np.array([ 3, 2, 4, 3, 3, 4, 5, 5, 3, 0, 0, 1,-3, 5, 0]),
        "Spectrum":             np.array([ 3, 3, 2, 2, 2, 3,-2, 3, 0, 0, 2, 0,-5, 0, 0]),
        "Adam Warlock":         np.array([ 3,-3, 2, 3, 2, 4,-1, 1, 3, 2, 3, 2,-5, 0, 1]),
        "Nebula":               np.array([ 2, 1, 2, 1,-3, 2, 3, 1, 1, 0, 0, 0,-5, 0, 1]),
        "War Machine":          np.array([ 1,-2, 1, 2, 4, 0,-2, 5, 0, 0, 0, 1,-3, 0, 2]),
        "Valkyrie":             np.array([ 1, 3,-2, 2, 2,-2,-1, 4, 0, 0, 0, 0,-3, 0, 1]),
        "Vision":               np.array([ 2, 3, 3, 3, 4, 3, 4, 2, 2, 0, 1, 0, 0, 1, 0]),
                                #          e, t, cv,s, d, th,re,mi,c, s, br,lg,si,sc,mu          
        "Ghost Spider":         np.array([ 3, 3, 3, 3, 3, 2, 2, 2, 4, 1, 1, 0,-3, 0, 0]),
        "Spider-Man (Miles)":   np.array([ 2, 4, 5, 3, 5, 4, 5, 1, 4, 0, 1, 0, 3, 5, 0]),
        "Nova":                 np.array([ 4, 4, 4, 1, 2, 3, 4, 3, 0, 1, 2, 0, 2, 0, 2]),
        "Ironheart":            np.array([ 2,-3, 4, 3, 5, 5, 0, 3, 0, 0, 2, 5,-3, 0, 4]),
        "SP//dr":               np.array([ 2,-1, 5, 3, 3, 5, 0, 1, 1, 0, 2, 2,-5, 0, 1]),
        "Spider-Ham":           np.array([ 5, 3, 4, 5, 2, 4, 5, 2, 4, 0, 2, 1,-1, 5, 0]),
                                #          e, t, cv,s, d, th,re,mi,c, s, br,lg,si,sc,mu        
        "Colossus":             np.array([ 1,-1, 4, 5, 3,-5,-2, 2, 4, 0, 0, 0,-3, 5, 1]),
        "Shadowcat":            np.array([ 3, 4, 2, 3, 1, 3, 5, 3, 3, 0, 0, 0,-5, 3, 0]),
        "Cyclops":              np.array([ 1,-2, 5, 3, 4, 4, 3, 3, 0, 2, 2, 1,-3, 0, 0]),
        "Phoenix":              np.array([ 2, 3, 3, 3, 4, 4, 3, 4, 3, 1, 2, 0, 0, 4, 0]),
        "Wolverine":            np.array([ 3, 5, 3, 4, 5, 3, 4, 5, 0, 0, 1, 0, 1, 0, 0]),
        "Storm":                np.array([ 1, 3, 3, 1, 4, 4, 3, 3, 1, 3, 1, 0,-3, 0, 2]),
        "Gambit":               np.array([ 1,-1, 2, 2, 3, 3, 2, 4, 2, 1, 0, 0,-1, 4, 0]),
        "Rogue":                np.array([ 0, 3, 3, 3, 3, 3, 1, 2, 2, 0, 1, 0, 0, 1, 2]),
                                #          e, t, cv,s, d, th,re,mi,c, s, br,lg,si,sc,mu        
        "Cable":                np.array([ 2, 3, 4, 3, 3, 5, 5, 2, 3, 3, 2, 3,-5, 0,-4]),
        "Domino":               np.array([ 3,-2, 4, 1, 4, 3, 2, 4, 1, 0, 0, 3,-5, 0, 1]),
        "Psylocke":             np.array([ 4, 4, 4, 1, 1, 5, 4, 3, 5, 0, 2, 0,-3, 5, 0]),
        "Angel":                np.array([ 2, 5, 2, 2, 3, 5, 5, 2, 1, 0, 2, 0,-1, 0, 0]),
        "X-23":                 np.array([ 1, 5, 4, 3, 5, 5, 5, 4, 0, 0, 1, 2,-2, 0, 0]),
        "Deadpool":             np.array([ 1, 5, 5, 5, 5, 5,-3, 2, 1, 3, 1, 0,-1, 1, 0]),
                                #          e, t, cv,s, d, th,re,mi,c, s, br,lg,si,sc,mu        
        "Bishop":               np.array([ 5, 2, 4, 4, 5, 1, 3, 2, 0, 0, 1, 1,-3, 0, 0]),
        "Magik":                np.array([ 4, 1, 4, 3, 2, 4, 3, 3, 2, 0, 1, 1,-5, 5, 0]),
        "Iceman":               np.array([ 3, 2, 3, 3, 2, 2, 3, 4, 3, 2, 0, 0, 0, 0, 1]),
        "Jubilee":              np.array([ 3,-1, 4, 0, 2, 4, 3, 3, 4, 1, 0, 1,-1, 5, 1]),
        "Nightcrawler":         np.array([ 1, 2, 3, 3, 0, 3, 4, 4, 1, 3, 0, 0,-1, 1, 0]),
        "Magneto":              np.array([ 3, 3, 3, 4, 3, 4, 5, 4, 2, 0, 0, 1, 3, 0, 1]),
                                #          e, t, cv,s, d, th,re,mi,c, s, br,lg,si,sc,mu        
        "Maria Hill":           np.array([ 2, 1, 5, 1, 2, 5, 5, 1, 1, 2, 2, 5,-3, 0, 2]),
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

# Define the path to the hero images
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

# Define a dictionary to map hero names to their image URLs
hero_image_urls = {
    "Captain Marvel": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/2_Captain%20Marvel.jpg?raw=true",
    "Iron Man": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/3_Iron_Man.jpg?raw=true",
    "Spider-Man Peter": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/5_Spider-Man_(Peter%20Parker).jpg?raw=true",
    "Black Panther": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/1_Black%20Panther.jpg?raw=true",
    "She-Hulk": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/4_She_Hulk.jpg?raw=true",
    "Captain America": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/6_Captain_America.jpg?raw=true",
    "Ms. Marvel": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/7_Ms_Marvel.jpg?raw=true",
    "Thor": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/8_Thor.jpg?raw=true",
    "Black Widow": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/9_Black_Widow.jpg?raw=true",
    "Doctor Strange": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/10_Doctor_Strange.jpg?raw=true",
    "Hulk": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/11_Hulk.jpg?raw=true",
    "Hawkeye": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/12_Hawkeye.jpg?raw=true",
    "Spider-Woman": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/13_Spider_Woman.jpg?raw=true",
    "Ant-Man": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/14_Ant_Man.jpg?raw=true",
    "Wasp": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/15_Wasp.jpg?raw=true",
    "Quicksilver": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/16_Quicksilver.jpg?raw=true",
    "Scarlet Witch": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/17_Scarlet_Witch.jpg?raw=true",
    "Groot": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/18_Groot.jpg?raw=true",
    "Rocket": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/19_Rocket.jpg?raw=true",
    "Star-Lord": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/20_Star_Lord.jpg?raw=true",
    "Gamora": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/21_Gamora.jpg?raw=true",
    "Drax": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/22_Drax.jpg?raw=true",
    "Venom (Flash)": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/23_Venom.jpg?raw=true",
    "Spectrum": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/25_Spectrum.jpg?raw=true",
    "Adam Warlock": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/24_Adam_Warlock.jpg?raw=true",
    "Nebula": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/26_Nebula.jpg?raw=true",
    "War Machine": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/27_War_Machine.jpg?raw=true",
    "Valkyrie": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/28_Valkyrie.jpg?raw=true",
    "Vision": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/29_Vision.jpg?raw=true",
    "Ghost Spider": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/30_Ghost_Spider.jpg?raw=true",
    "Spider-Man (Miles)": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/31_Spider_Man_Miles.jpg?raw=true",
    "Nova": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/32_Nova.jpg?raw=true",
    "Ironheart": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/33_Ironheart.jpg?raw=true",
    "SP//dr": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/35_SPdr.jpg?raw=true",
    "Spider-Ham": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/34_Spider_Ham.jpg?raw=true",
    "Colossus": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/36_Colossus.jpg?raw=true",
    "Cyclops": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/38_Cyclops.jpg?raw=true",
    "Shadowcat": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/37_Shadowcat.jpg?raw=true",
    "Phoenix": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/39_Phoenix.jpg?raw=true",
    "Wolverine": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/40_Wolverine.jpg?raw=true",
    "Storm": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/41_Storm.jpg?raw=true",
    "Gambit": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/42_Gambit.jpg?raw=true",
    "Rogue": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/43_Rogue.jpg?raw=true",
    "Cable": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/44_Cable.jpg?raw=true",
    "Domino": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/45_Domino.jpg?raw=true",
    "Psylocke": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/46_Psylocke.jpg?raw=true",
    "Angel": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/47_Angel.jpg?raw=true",
    "X-23": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/48_X_23.jpg?raw=true",
    "Deadpool": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/49_Deadpool.jpg?raw=true",
    "Bishop": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/50_Bishop.jpg?raw=true",
    "Magik": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/51_Magik.jpg?raw=true",
    "Iceman": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/52_Iceman.jpg?raw=true",
    "Jubilee": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/53_Jubilee.jpg?raw=true",
    "Nightcrawler": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/54_Nightcrawler.jpg?raw=true",
    "Magneto": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/55_Magneto.jpg?raw=true",
    "Maria Hill": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/56_Maria_Hill.jpg?raw=true",
    "Nick Fury": "https://github.com/alechoward-lab/Marvel-Champions-Hero-Tier-List/blob/main/images/heroes/57_Nick_Fury.jpg?raw=true"
}

# Display Tier List with Images
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
    st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line after each tier

# ----------------------------------------
# Plotting
# ----------------------------------------
st.header(f"Hero Scores")

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

ax.grid(axis='y', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.markdown("<hr>", unsafe_allow_html=True)  # Add a horizontal line after each tier

st.markdown("Most card images are from the Cerebro Discord bot developed by UnicornSnuggler. Thank you!")
# To Do List:

# Create a markdown section at the end that goes over the assumptions of this tier list and mention that people can adjust them.
# find a way to allow users to save their settings
# find a way to allow users to load their settings
# Check that the hero values are correct and nothing was lost in translation
# fine tune all the presets

# mention heroes that don't work well with this system (Maria Hill, Cylcops, Cable, etc.)

# Link to my site: https://marvel-champions-hero-tier-list-lrfbh27q9vswdmvapphhlzd.streamlit.app/ 