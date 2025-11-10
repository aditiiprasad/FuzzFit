import streamlit as st
from fuzzy_engine import OutfitFuzzySystem

# Initialize fuzzy system
system = OutfitFuzzySystem()

st.set_page_config(page_title="FuzzFit 👕", page_icon="👕", layout="wide")

st.title("👕 FuzzFit: AI Outfit Recommender using Fuzzy Logic")
st.markdown("### Get intelligent outfit & color suggestions based on temperature, occasion, and your style!")

# Inputs
temperature = st.slider("🌡️ Temperature (°C)", 0, 50, 25)
occasion_val = st.slider("🎭 Occasion", 0, 10, 5, help="0=Casual, 5=Formal, 10=Festive")
style_val = st.slider("🎨 Personal Style", 0, 10, 5, help="0=Minimal, 5=Trendy, 10=Bold")

# Button
if st.button("✨ Recommend Outfit"):
    rec = system.get_recommendation(temperature, occasion_val, style_val)

    st.subheader(f"👕 Recommended: **{rec['outfit_type']}**")
    st.write(f"**Temperature:** {rec['temperature']}°C")
    st.write(f"**Occasion:** {rec['occasion']}  |  **Style:** {rec['style']}")

    st.markdown("### 🎨 Suggested Color Palette:")
    cols = st.columns(len(rec['color_palette']['primary']))
    for i, color in enumerate(rec['color_palette']['primary']):
        with cols[i]:
            st.color_picker(rec['color_palette']['names'][i], color, disabled=True)
    st.info(f"Color Category: {rec['color_palette']['category']}")

    st.markdown("### 👔 Outfit Ideas:")
    for o in rec['outfit_details']:
        st.markdown(f"- {o}")

    st.success("✅ Recommendation generated successfully!")
