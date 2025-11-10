import streamlit as st
from fuzzy_engine import OutfitFuzzySystem

if "fuzzy_system" not in st.session_state:
    st.session_state.fuzzy_system = OutfitFuzzySystem()
system = st.session_state.fuzzy_system

st.set_page_config(page_title="FuzzFit 👕", page_icon="👕", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    section[data-testid="stSidebar"] .stButton>button {
        background-color: #238636;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 10px 14px;
        font-weight: 600;
        border: 1px solid #2ea043;
        transition: all 0.2s ease;
        width: 100%;
    }
    section[data-testid="stSidebar"] .stButton>button:hover {
        background-color: #2ea043;
        border-color: #3fb950;
    }
    section[data-testid="stSidebar"] label {
        color: #f0f6fc;
        font-weight: 600;
    }
    .main-title {
        font-size: 52px !important;
        color: #f0f6fc;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
    }
    .sub-title {
        font-size: 18px !important;
        color: #8b949e;
        text-align: center;
        margin-bottom: 24px;
    }
    .link-style {
        display: block;
        padding: 10px 14px;
        border-radius: 8px;
        background: #21262d;
        color: #c9d1d9;
        border: 1px solid #30363d;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.2s ease;
        text-align: center;
    }
    .link-style:hover {
        background: #30363d;
        border-color: #8b949e;
    }
    h3, h4 {
        color: #f0f6fc;
    }
    .stMetricLabel {
        color: #8b949e !important;
    }
    .stMetricValue {
        color: #f0f6fc !important;
    }
    .stInfo {
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #c9d1d9;
        border-radius: 8px;
    }
    hr {
        border: 1px solid #30363d !important;
    }
    .footer {
        text-align:center; 
        margin-top:26px; 
        color: #8b949e;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

github_url = "https://github.com/aditiiprasad/FuzzFit"

st.markdown('<p class="main-title">FuzzFit 👕</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">AI Outfit Recommender — Get intelligent outfit & color suggestions based on temperature, location, and your style</p>',
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1.5, 2, 1.5])
with col2:
    st.markdown(
        f'<a class="link-style" href="{github_url}" target="_blank">🌐 View on GitHub</a>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

st.sidebar.title("🎯 Your Preferences")

temperature = st.sidebar.slider("🌡️ Temperature (°C)", 0, 50, 25)

occasion_options = {
    "Casual Outing": 0, "Office / Work": 3, "Business Meeting": 5,
    "Party": 7, "Festival": 10, "Wedding": 9,
    "Date / Evening Out": 8, "Formal Event": 6,
    "Sports / Outdoor": 2, "Travel": 4
}
occasion_name = st.sidebar.selectbox("🎭 Occasion", list(occasion_options.keys()))
occasion_val = occasion_options[occasion_name]

style_options = {
    "Minimal": 0, "Elegant": 2, "Trendy": 5, "Vintage": 6,
    "Streetwear": 7, "Bohemian": 8, "Sporty": 4,
    "Bold": 10, "Chic": 3, "Classic": 1
}
style_name = st.sidebar.selectbox("🎨 Personal Style", list(style_options.keys()))
style_val = style_options[style_name]

st.sidebar.divider()
recommend = st.sidebar.button("✨ Recommend Outfit")

st.subheader("Your Recommendation")

if recommend:
    rec = system.get_recommendation(temperature, occasion_val, style_val)
    st.markdown(f"### **{rec['outfit_type']}**")
    c1, c2, c3 = st.columns(3)
    c1.metric("Temperature", f"{rec['temperature']}°C")
    c2.metric("Occasion", occasion_name)
    c3.metric("Style", style_name)
    st.divider()
    st.markdown("#### 🎨 Suggested Color Palette")
    color_primaries = rec["color_palette"]["primary"]
    color_names = rec["color_palette"]["names"]
    cols = st.columns(len(color_primaries)) 
    for i, color in enumerate(color_primaries):
        with cols[i]:
            st.markdown(
                f"<div style='background:{color}; height:72px; border-radius:8px; border:1px solid #30363d'></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p style='text-align:center; font-weight:600; color:#c9d1d9'>{color_names[i]}</p>", 
                unsafe_allow_html=True
            )
    st.info(f"**Category:** {rec['color_palette']['category']}")
    st.divider()
    st.markdown("#### 👔 Outfit Ideas")
    for o in rec["outfit_details"]:
        st.markdown(f"- {o}")
    st.balloons()
else:
    st.info("Adjust your preferences from the sidebar and click 'Recommend Outfit' to see suggestions.")




# --- Fuzzy Logic Explanation Section ---
st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #f58529, #dd2a7b, #8134af, #515bd4);
        padding: 40px 24px;
        border-radius: 16px;
        color: white;
        margin-top: 40px;
        text-align: center;
        box-shadow: 0 0 25px rgba(0,0,0,0.3);
    ">
        <h2 style="color:white; font-size:30px;">💡 How Fuzzy Logic Powers FuzzFit</h2>
        <p style="font-size:16px; line-height:1.7; text-align:justify;">
            Fuzzy Logic is an intelligent system that mimics how humans make decisions 
            based on <b>degrees of truth</b> rather than rigid yes/no logic. 
            Instead of saying “it’s cold” or “it’s hot,” fuzzy logic understands that temperature can be 
            <i>somewhat cold</i> or <i>moderately warm</i>, and uses smooth transitions between these states.
        </p>
        <p style="font-size:16px; line-height:1.7; text-align:justify;">
            In <b>FuzzFit 👕</b>, fuzzy logic takes three key inputs:
            <b>temperature</b>, <b>occasion type</b>, and <b>personal style</b>.
            Using predefined fuzzy sets and rules, it calculates the most suitable 
            <b>outfit type</b> (like Light Casual or Formal Wear) and the matching 
            <b>color intensity</b> (Neutral, Cool, or Vibrant).
        </p>
        <p style="font-size:16px; line-height:1.7; text-align:justify;">
            Behind the scenes, each input is passed through fuzzy membership functions, 
            fuzzy rules are applied (IF–THEN logic), and the results are defuzzified into crisp output values. 
            These values determine your final outfit and color recommendations — 
            just like how humans make style choices based on mood, weather, and events 🌤️🎉.
        </p>
        <p style="font-size:16px; font-weight:600; margin-top:16px;">
            → Powered by <b>Fuzzy Inference System (skfuzzy)</b> & <b>Streamlit</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
