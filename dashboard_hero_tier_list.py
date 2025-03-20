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

# Custom CSS to add a black background
st.markdown(
    """
    <style>
    .black-background {
        background-color: black;
        color: white;
        padding: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Marvel Champions Hero Tier List")
st.markdown(
    "Adjust the weighting based on how much you value each aspect of hero strength. "
    "You can choose from preset weighting functions (which automatically load into the sliders) "
    "or adjust the sliders manually."
)

# ----------------------------------------
# Layout: Two columns side by side
# ----------------------------------------

# Apply black background to the entire layout
col1, col2 = st.columns(2)

# Column 1: Weighting settings (presets and sliders)
with col1:
    st.markdown('<div class="black-background">', unsafe_allow_html=True)  # Apply black background to this section
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
        st.session_state["plot_title"] = preset_choice
    else:
        st.session_state["plot_title"] = "Custom"
    
    st.markdown('</div>', unsafe_allow_html=True)  # End of the black background div

# Column 2: Graphs and other data

with col2:
    st.markdown('<div class="black-background">', unsafe_allow_html=True)  # Apply black background to this section
    st.header("Hero Performance Analysis")
    # Your graphing code here
    st.markdown('</div>', unsafe_allow_html=True)  # End of the black background div
