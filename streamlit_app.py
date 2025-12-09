import streamlit as st
from PIL import Image
import requests

# =========================
# Basic Config
# =========================
st.set_page_config(
    page_title="NEXTGEN PC Store",
    page_icon="🛒",
    layout="centered"
)

# =========================
# Custom CSS (ألوان من البالِت حقتك)
# =========================
st.markdown("""
<style>

/* ===== BACKGROUND ===== */
html, body, [data-testid="stApp"], .stApp {
    background-color: #f0faff !important;
}

/* ===== GLOBAL TEXT RESET ===== */
* {
    color: #ffffff !important;
}

/* ===== TITLES ===== */
.nextgen-title {
    font-size: 32px;
    font-weight: 700;
    color: #210c5f !important;
    letter-spacing: 2px;
}

.nextgen-subtitle {
    font-size: 16px;
    color: #605490 !important;
    letter-spacing: 2px;
}
            
/* ===== PRODUCT NAME & DESC ===== */
h1, h2, h3, h4, h5, h6 {
    color: #210c5f !important;
}

p, span, label, div {
    color: #605490 !important;
}

/* ===== PRICE ===== */
.price-tag {
    font-size: 22px;
    font-weight: 700;
    color: #210c5f !important;
}

/* ===== TOTAL ===== */
.total-text {
    font-size: 18px;
    font-weight: 600;
    color: #210c5f !important;
}

.fraud-hint {
    font-size: 12px;
    color: #a9a8c8 !important;
}

/* ===== INPUTS ===== */
input, textarea {
    background-color: #f0faff !important;
    color: #210c5f !important;
    border: 1px solid #a4bade !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background-color: #210c5f !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 600;
    color: #ffffff !important;   
}

.stButton > button * {
    color: #ffffff !important;
}

.stButton > button:hover {
    background-color: #37b6ff !important;
    color: #210c5f !important;
}


/* ===== RESULT MESSAGES ===== */
.success-msg {
    color: #37b6ff !important;
    font-weight: 700;
}

.error-msg {
    color: #210c5f !important;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# =========================
# Constants
# =========================
UNIT_PRICE = 8000          # سعر الجهاز
FRAUD_THRESHOLD = 100000   # لو المجموع > هذا يعتبر high risk في الديمو
PRODUCT_NAME = "OcUK Gaming Fluorite"
PRODUCT_DESC = "Intel Core I5 14600KF, RTX 5070 Pre-Built Gaming PC"

# =========================
# Session State
# =========================
if "step" not in st.session_state:
    st.session_state.step = "product"   # product -> checkout -> result
if "quantity" not in st.session_state:
    st.session_state.quantity = 1
if "total_amount" not in st.session_state:
    st.session_state.total_amount = UNIT_PRICE

# =========================
# Helper: (حاليًا منطق بسيط بدل استدعاء FastAPI)
# لاحقًا استبدليه بطلب حقيقي للـ API
# =========================
def call_fraud_api(total_amount: float, quantity: int):
    url = "http://127.0.0.1:8000/simulate_checkout"
    payload = {"quantity": quantity}
    resp = requests.post(url, json=payload)
    data = resp.json()
    return data["is_fraud_predicted"], data["fraud_probability"]

# =========================
# Header (Logo + Title)
# =========================
header_logo_col, header_text_col = st.columns([1, 4])

with header_logo_col:
    try:
        logo_img = Image.open("assets/logo.png")
        st.image(logo_img, use_container_width=True)
    except Exception:
        st.write("NEXTGEN PC")

with header_text_col:
    st.markdown(
        """
        <div style="display:flex; flex-direction:column; justify-content:center; height:100%;">
            <div class="nextgen-title">NEXTGEN PC</div>
            <div class="nextgen-subtitle">YOUR ULTIMATE PC STORE</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")  # مسافة بسيطة تحت الهيدر


# =========================
# STEP 1: Product Page
# =========================
if st.session_state.step == "product":

    col_img, col_info = st.columns([1, 1])

    with col_img:
        try:
            pc_img = Image.open("assets/pc.png")
            st.image(pc_img, use_container_width=True)
        except Exception:
            st.write("[Product image here]")

    with col_info:
        st.subheader(PRODUCT_NAME)
        st.caption(PRODUCT_DESC)

        st.markdown('<span class="label-muted">Unit Price</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="price-tag">{UNIT_PRICE:,.0f} SAR</div>', unsafe_allow_html=True)

        quantity = st.number_input("Quantity", min_value=1, max_value=50, value=st.session_state.quantity, step=1)
        total_amount = quantity * UNIT_PRICE

        st.session_state.quantity = quantity
        st.session_state.total_amount = total_amount

        st.markdown('<div class="total-box">', unsafe_allow_html=True)
        st.markdown(
            f'<div class="total-text">Total: {total_amount:,.0f} SAR</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            f'<div class="fraud-hint">* For demo: amounts above {FRAUD_THRESHOLD:,.0f} SAR will be treated as high-risk.</div>',
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")
        if st.button("Checkout 🧾"):
            st.session_state.step = "checkout"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEP 2: Checkout Page
# =========================
elif st.session_state.step == "checkout":
    st.subheader("Payment Details")

    st.text_input("Cardholder Name", value="")
    st.text_input("Card Number", value="", max_chars=19)
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Expiry Date (MM/YY)", value="")
    with col2:
        st.text_input("CVV", value="", max_chars=4)

    st.markdown('<hr/>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="total-text">Total to Pay: {st.session_state.total_amount:,.0f} SAR</div>',
        unsafe_allow_html=True
    )

    col_back, col_pay = st.columns([1, 2])
    with col_back:
        if st.button("⬅ Back"):
            st.session_state.step = "product"
            st.rerun()

    with col_pay:
        if st.button("Pay Now 💳"):
            # هنا نستدعي منطق الاحتيال (حاليًا mock)
            is_fraud, fraud_prob = call_fraud_api(st.session_state.total_amount)
            st.session_state.is_fraud = is_fraud
            st.session_state.fraud_prob = fraud_prob
            st.session_state.step = "result"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# STEP 3: Result Page
# =========================
elif st.session_state.step == "result":
    st.subheader("Transaction Result")

    is_fraud = st.session_state.get("is_fraud", False)
    fraud_prob = st.session_state.get("fraud_prob", 0.0)

    if is_fraud:
        st.markdown(
            f'<div class="error-msg">❌ Transaction Declined – Suspected Fraud '
            f'({fraud_prob*100:.1f}% risk)</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="success-msg">✅ Payment Approved – Transaction Completed '
            f'({fraud_prob*100:.1f}% fraud risk)</div>',
            unsafe_allow_html=True
        )

    st.write("")
    if st.button("New Purchase 🛒"):
        st.session_state.step = "product"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
