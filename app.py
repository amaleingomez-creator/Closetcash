import streamlit as st
import requests
import json

st.set_page_config(page_title="ClosetCa$h", page_icon="👗", layout="centered")

CSS = """
<style>
.stApp { background-color: #F3E7D2; }
section[data-testid="stMain"] { background-color: #F3E7D2; }
#MainMenu, footer, header { visibility: hidden; }
html, body, [class*="css"] { font-family: 'Calibri', 'Gill Sans', sans-serif; color: #3B2418; }
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    background-color: #EDE0C6 !important; border: 2px solid #C1623E !important;
    border-radius: 12px !important; color: #3B2418 !important; }
.stButton > button {
    background-color: #C1623E !important; color: #FBF3E6 !important;
    border: none !important; border-radius: 30px !important;
    padding: 14px 30px !important; font-size: 17px !important;
    font-weight: 700 !important; letter-spacing: 1.5px !important;
    width: 100% !important; margin-top: 10px !important; }
.stButton > button:hover { background-color: #9C4A2C !important; }
div[data-testid="stMetric"] {
    background-color: #EDE0C6; border-radius: 12px;
    padding: 12px; border-left: 4px solid #C1623E; }
hr { border-color: #C1623E33; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

STORES = [
    {"name": "Vintage Hub", "distance": "1.2 km",
     "address": "45 Fuencarral Street, Madrid",
     "hours": "10:00 - 20:00", "phone": "+34 910 123 456",
     "brands": ["Zara", "Mango", "Guess", "H&M"], "pct": 1.0},
    {"name": "ReFashion Store", "distance": "2.0 km",
     "address": "12 Serrano Street, Madrid",
     "hours": "11:00 - 19:30", "phone": "+34 910 234 567",
     "brands": ["H&M", "Zara", "Pull&Bear", "Bershka"], "pct": 0.85},
    {"name": "Circular Closet", "distance": "3.4 km",
     "address": "88 Gran Via, Madrid",
     "hours": "10:00 - 21:00", "phone": "+34 910 345 678",
     "brands": ["Guess", "Mango", "Massimo Dutti", "COS"], "pct": 0.92},
]

def header(title, subtitle, dark=True):
    bg = "#3B2418" if dark else "#EDE0C6"
    fg = "#FBF3E6" if dark else "#3B2418"
    sub_color = "#D7A33E" if dark else "#6E5641"
    st.markdown(
        '<div style="background:' + bg + ';border-radius:16px;padding:24px;margin-bottom:20px;text-align:center;">'
        + '<h2 style="color:' + fg + ';font-family:Georgia,serif;margin:0;">' + title + '</h2>'
        + '<p style="color:' + sub_color + ';margin:6px 0 0 0;font-size:14px;font-style:italic;">' + subtitle + '</p>'
        + '</div>',
        unsafe_allow_html=True
    )

def gold_box(label, value, note=""):
    st.markdown(
        '<div style="background:#D7A33E;border-radius:16px;padding:24px;text-align:center;margin:12px 0;">'
        + '<p style="color:#3B2418;margin:0;font-size:12px;font-weight:700;letter-spacing:2px;">' + label + '</p>'
        + '<h1 style="color:#3B2418;margin:10px 0;font-family:Georgia,serif;font-size:46px;">' + value + '</h1>'
        + '<p style="color:#3B2418;margin:0;font-size:14px;">' + note + '</p>'
        + '</div>',
        unsafe_allow_html=True
    )

def dark_card(label, text):
    st.markdown(
        '<div style="background:#3B2418;border-radius:12px;padding:16px 20px;margin:12px 0;">'
        + '<p style="color:#D7A33E;margin:0;font-size:12px;font-weight:700;letter-spacing:1px;">' + label + '</p>'
        + '<p style="color:#FBF3E6;margin:6px 0 0 0;font-size:14px;">' + text + '</p>'
        + '</div>',
        unsafe_allow_html=True
    )

def store_row(name, distance, payout, best=False):
    bg = "#3B2418" if best else "#EDE0C6"
    fg = "#FBF3E6" if best else "#3B2418"
    price_color = "#D7A33E" if best else "#C1623E"
    dist_color = "#D7A33E" if best else "#6E5641"
    badge = " 🏆 Best offer" if best else ""
    st.markdown(
        '<div style="background:' + bg + ';border-radius:14px;padding:16px 20px;margin-bottom:8px;">'
        + '<div style="display:flex;justify-content:space-between;align-items:center;">'
        + '<div>'
        + '<p style="color:' + fg + ';margin:0;font-weight:700;font-size:15px;">📍 ' + name + badge + '</p>'
        + '<p style="color:' + dist_color + ';margin:2px 0 0 0;font-size:12px;">' + distance + '</p>'
        + '</div>'
        + '<p style="color:' + price_color + ';margin:0;font-size:24px;font-weight:700;">€' + str(payout) + '</p>'
        + '</div></div>',
        unsafe_allow_html=True
    )

# ── Logo ──────────────────────────────────────────
st.markdown(
    '<div style="background:#3B2418;border-radius:20px;padding:28px;text-align:center;margin-bottom:24px;">'
    + '<h1 style="color:#FBF3E6;font-family:Georgia,serif;font-size:42px;margin:0;">'
    + 'ClosetCa<span style="color:#D7A33E;">$</span>h</h1>'
    + '<p style="color:#EDE0C6;margin:8px 0 0 0;font-size:15px;font-style:italic;">'
    + 'Snap it. Price it. ClosetCa$h.</p>'
    + '</div>',
    unsafe_allow_html=True
)

# ── SCREEN: Store Details ─────────────────────────
if "store_selected" in st.session_state:
    t = STORES[st.session_state.store_selected]
    price = st.session_state.get("price_max", 0)
    payout = int(price * t["pct"])

    header("🏪 " + t["name"], "Best option for your item")

    col1, col2 = st.columns(2)
    col1.metric("📍 Address", t["address"])
    col2.metric("🕐 Hours", t["hours"])

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**✅ Accepted brands:**")
    cols = st.columns(len(t["brands"]))
    for i, b in enumerate(t["brands"]):
        cols[i].markdown(
            '<div style="background:#EDE0C6;border-radius:10px;padding:8px;'
            + 'text-align:center;border-left:3px solid #C1623E;">'
            + '<span style="color:#3B2418;font-weight:600;">✓ ' + b + '</span></div>',
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    gold_box("ESTIMATED PAYOUT", "€" + str(payout), "Average: 75% of estimated resale value")

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    if col1.button("🗺️ Get Directions"):
        url = t["address"].replace(" ", "+")
        st.markdown("[👉 Open in Google Maps](https://maps.google.com/?q=" + url + ")")
    if col2.button("📞 Call Store"):
        st.info("📞 " + t["phone"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to results"):
        del st.session_state.store_selected
        st.rerun()

# ── SCREEN: Form + Results ────────────────────────
else:
    st.markdown(
        '<p style="color:#3B2418;font-size:16px;text-align:center;margin-bottom:20px;">'
        + 'Before buying more clothes — discover the value hidden in the ones you already own.</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div style="background:#EDE0C6;border-radius:16px;padding:20px 24px;margin-bottom:16px;">'
        + '<h3 style="color:#3B2418;font-family:Georgia,serif;margin:0 0 4px 0;">What are you looking to sell?</h3>'
        + '</div>',
        unsafe_allow_html=True
    )

    category = st.selectbox("Category",
        ["Top / T-shirt", "Jacket", "Skirt / Dress", "Trousers", "Shoes"],
        label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    brand = st.text_input("Brand", placeholder="e.g. Zara, H&M, Guess, Mango...")

    st.markdown("<br>", unsafe_allow_html=True)
    condition = st.radio("Condition",
        ["New", "Used - good condition", "Used - worn"],
        horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("💰 ESTIMATE RESALE VALUE"):
        if brand:
            with st.spinner("Analysing your item with AI..."):
                prompt = (
    "You are an expert in second-hand fashion with deep knowledge of resale platforms "
    "like Vinted, Wallapop, Depop and eBay in Europe in 2025. "
    "Estimate a REALISTIC resale price in euros for this item based on current market prices. "
    "Premium brands (Tommy Hilfiger, Guess, Levis, Mango, Zara, Carolina Herrera) typically sell for 15-80 euros depending on condition. "
    "Luxury brands (COS, Massimo Dutti, Arket) sell for 30-120 euros. "
    "Fast fashion (H&M, Primark, Bershka) sells for 3-15 euros. "
    "Category: " + category + ", Brand: " + brand + ", Condition: " + condition + ". "
    "Reply ONLY with this exact JSON format, no extra text: "
    '{"price_min": 10, "price_max": 30, "confidence": 85, "reason": "brief explanation in English"}'
)
                try:
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={"model": "llama3.2", "prompt": prompt, "stream": False},
                        timeout=30
                    )
                    result = response.json()["response"]
                    start = result.find("{")
                    end = result.rfind("}") + 1
                    data = json.loads(result[start:end])
                    st.session_state.result = data
                except Exception as e:
                    st.error("Could not connect to Ollama: " + str(e))
        else:
            st.warning("Please enter the brand of your item.")

    if "result" in st.session_state:
        data = st.session_state.result
        st.session_state.price_max = data["price_max"]

        st.markdown("<br>", unsafe_allow_html=True)
        gold_box(
            "ESTIMATED RESALE VALUE",
            "€" + str(data["price_min"]) + " — €" + str(data["price_max"]),
            "Confidence: " + str(data["confidence"]) + "%"
        )

        dark_card("💡 AI INSIGHT", data["reason"])

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<h3 style="color:#3B2418;font-family:Georgia,serif;">🏪 Nearby buyers</h3>',
            unsafe_allow_html=True
        )

        for i, t in enumerate(STORES):
            payout = int(data["price_max"] * t["pct"])
            store_row(t["name"], t["distance"], payout, best=(i == 0))
            if st.button("See details →", key="s" + str(i)):
                st.session_state.store_selected = i
                st.rerun()