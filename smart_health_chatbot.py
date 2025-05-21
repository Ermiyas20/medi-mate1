import streamlit as st
from fpdf import FPDF
from datetime import date
import re

# --- Must come FIRST before any Streamlit UI commands ---
st.set_page_config(page_title="MediMate", layout="wide")

# --- Inject JS to capture user agent ---
def get_user_agent():
    user_agent = """
    <script>
    const userAgent = navigator.userAgent;
    const streamlitDoc = window.parent.document;
    const iframe = streamlitDoc.querySelector('iframe');
    const streamlitWindow = iframe.contentWindow;
    streamlitWindow.postMessage({type: 'streamlit:setComponentValue', value: userAgent}, '*');
    </script>
    """
    st.components.v1.html(user_agent, height=0)

# --- User Agent Setup ---
if 'user_agent' not in st.session_state:
    st.session_state['user_agent'] = ""
    get_user_agent()

def is_mobile():
    ua = st.session_state.get('user_agent', "")
    return bool(re.search("iphone|android|blackberry|mobile", ua.lower()))

# --- Device Flag ---
MOBILE = is_mobile()

# --- Navigation ---
if not MOBILE:
    st.sidebar.title("MediMate")
    st.sidebar.info("Your Smart Health Companion")
    page = st.sidebar.selectbox("Go to", ["🏠 Home", "🩺 Symptom Checker", "📊 BMI Calculator", "📝 Health Report"])
else:
    st.title("📱 MediMate Mobile")
    page = st.selectbox("Go to", ["🏠 Home", "🩺 Symptom Checker", "📊 BMI Calculator", "📝 Health Report"])

# --- Home Page ---
if page == "🏠 Home":
    st.header("👋 Welcome to MediMate")
    st.write("Your smart assistant for basic health needs.")
    st.image("assets/logo.png", width=300 if MOBILE else 500)

# --- Symptom Checker ---
elif page == "🩺 Symptom Checker":
    st.header("Check Your Symptoms")
    symptoms = st.text_input("Describe your symptoms (e.g. cough, fever):")

    if st.button("Check"):
        symptoms = symptoms.lower()
        if "fever" in symptoms and "cough" in symptoms:
            st.warning("You may have the flu or COVID-19. Seek medical help.")
        elif "headache" in symptoms:
            st.info("Possible causes: stress, migraine, dehydration.")
        elif "stomach" in symptoms:
            st.info("Might be food-related. Stay hydrated.")
        else:
            st.success("Mild symptoms detected. Rest and monitor.")

# --- BMI Calculator ---
elif page == "📊 BMI Calculator":
    st.header("Calculate Your BMI")
    weight = st.number_input("Weight (kg)", 1.0)
    height = st.number_input("Height (cm)", 1.0)

    if st.button("Calculate"):
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        st.success(f"Your BMI is {bmi:.2f}")
        if bmi < 18.5:
            st.info("Underweight")
        elif 18.5 <= bmi < 25:
            st.success("Normal weight")
        elif 25 <= bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Obese")

# --- Health Report PDF ---
elif page == "📝 Health Report":
    st.header("📝 Generate Health Report")
    name = st.text_input("Your Name")
    age = st.number_input("Age", 0, 120)
    notes = st.text_area("Health Notes / Symptoms")
    if st.button("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, "MediMate - Health Report", ln=True, align="C")
        pdf.cell(200, 10, f"Name: {name}", ln=True)
        pdf.cell(200, 10, f"Age: {age}", ln=True)
        pdf.cell(200, 10, f"Date: {date.today()}", ln=True)
        pdf.ln(10)
        pdf.multi_cell(0, 10, f"Notes: {notes}")
        pdf.output("mediMate_report.pdf")
        st.success("PDF generated! Check your local directory.")
