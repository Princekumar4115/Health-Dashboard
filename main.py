import  streamlit as st

st.title("welcome to the health dashboard")


# Dummy user credentials
users = {
    "admin": "admin123",
    "prince": "securepass",
    "guest": "guest123"
}

# Page setup
st.set_page_config(page_title="Login Page", layout="centered")
st.title("🔐 User Login")

# Login form
with st.form("login_form"):
    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")
    login_btn = st.form_submit_button("Login")

# Login logic
if login_btn:
    if not username or not password:
        st.warning("Please fill in both username and password.")
    elif username in users and users[username] == password:
        st.success(f"Welcome, {username}!")
        st.balloons()
        # You can redirect to another page or show dashboard here
    else:
        st.error("Invalid username or password.")



# Dashboard UI
st.title("📊 Health Assistant Dashboard")
st.write("Welcome to your health assistant dashboard, Prince!")

# Example health metrics
st.metric("Heart Rate", "72 bpm")
st.metric("Blood Pressure", "120/80 mmHg")

# 🚶 Step Count Section
st.subheader("🚶 Daily Step Count")
step_goal = 10000
steps_today = 6842  # You can make this dynamic later

progress = int((steps_today / step_goal) * 100)
st.progress(progress)
st.write(f"You've walked **{steps_today} steps** today out of your goal of **{step_goal} steps**.")

# Log out button
if st.button("Log Out"):
    st.session_state.logged_in = False
    st.experimental_rerun()
import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# Google Maps API Key
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"

# User's location (can be dynamic via geolocation or input)
user_lat = 23.2599
user_lng = 77.4126

# Function to find nearby hospitals
def find_nearest_hospital(lat, lng):
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,
        "type": "hospital",
        "key": API_KEY
    }
    response = requests.get(url, params=params).json()
    if response["results"]:
        return response["results"][0]  # Nearest hospital
    return None

# Function to simulate notification
def send_notification(hospital_name, hospital_location):
    st.success(f"🚨 Notification sent to {hospital_name} at {hospital_location}!")

# Streamlit UI
st.title("🏥 Emergency Hospital Notifier")

hospital = find_nearest_hospital(user_lat, user_lng)

if hospital:
    name = hospital["name"]
    location = hospital["vicinity"]
    lat = hospital["geometry"]["location"]["lat"]
    lng = hospital["geometry"]["location"]["lng"]

    st.write(f"Nearest Hospital: **{name}**")
    st.write(f"Location: {location}")

    # Map display
    m = folium.Map(location=[user_lat, user_lng], zoom_start=13)
    folium.Marker([user_lat, user_lng], tooltip="Your Location", icon=folium.Icon(color="blue")).add_to(m)
    folium.Marker([lat, lng], tooltip=name, icon=folium.Icon(color="red")).add_to(m)
    st_folium(m, width=700)

    # Notify button
    if st.button("Send Emergency Notification"):
        send_notification(name, location)
else:
    st.error("No hospitals found nearby.")
import streamlit as st

# Symptom database
health_data = {
    "diarrhea": {
        "avoid": ["Dairy", "Fried foods", "Caffeine", "Spicy foods"],
        "prevention": ["Drink clean water", "Wash hands", "Avoid street food"],
        "precautions": ["Stay hydrated", "Use oral rehydration salts"],
        "diseases": ["Gastroenteritis", "Food poisoning", "IBS"]
    },
    "vomiting": {
        "avoid": ["Solid food", "Alcohol", "Citrus fruits", "Dairy"],
        "prevention": ["Avoid overeating", "Limit alcohol", "Eat fresh food"],
        "precautions": ["Sip water slowly", "Rest", "Avoid strong smells"],
        "diseases": ["Stomach flu", "Migraine", "Pregnancy-related nausea"]
    },
    "nausea": {
        "avoid": ["Greasy food", "Strong odors", "Caffeine"],
        "prevention": ["Eat small meals", "Avoid motion sickness triggers"],
        "precautions": ["Ginger tea", "Cool compress", "Rest"],
        "diseases": ["Indigestion", "Anxiety", "Vertigo"]
    },
    "dehydration": {
        "avoid": ["Alcohol", "Caffeinated drinks", "Salty snacks"],
        "prevention": ["Drink 2.5–3L water daily", "Avoid excessive heat"],
        "precautions": ["Use ORS", "Monitor urine color"],
        "diseases": ["Heat stroke", "Kidney issues"]
    },
    "jaundice": {
        "avoid": ["Alcohol", "Fatty foods", "Red meat"],
        "prevention": ["Vaccinate for hepatitis", "Avoid contaminated water"],
        "precautions": ["Eat boiled vegetables", "Rest", "Monitor bilirubin"],
        "diseases": ["Hepatitis A/B/C", "Liver cirrhosis"]
    },
    "headache": {
        "avoid": ["Caffeine", "Processed meat", "MSG"],
        "prevention": ["Sleep well", "Stay hydrated", "Limit screen time"],
        "precautions": ["Cold compress", "Quiet room", "Pain relievers"],
        "diseases": ["Migraine", "Tension headache", "Sinusitis"]
    },
    "abdominal pain": {
        "avoid": ["Spicy food", "Carbonated drinks", "Dairy"],
        "prevention": ["Eat slowly", "Avoid overeating"],
        "precautions": ["Warm compress", "Hydration", "Light meals"],
        "diseases": ["Ulcers", "Appendicitis", "Gallstones"]
    },
    "fatigue": {
        "avoid": ["Sugar", "Alcohol", "Heavy meals"],
        "prevention": ["Regular sleep", "Balanced diet", "Exercise"],
        "precautions": ["Short naps", "Hydration", "Iron-rich foods"],
        "diseases": ["Anemia", "Thyroid issues", "Chronic fatigue syndrome"]
    }
}

# Streamlit UI
st.title("🩺 Health Chatbot Assistant")
user_input = st.chat_input("Describe your symptom (e.g., diarrhea, nausea)...")

if user_input:
    symptom = user_input.lower().strip()
    st.chat_message("You").write(user_input)

    if symptom in health_data:
        info = health_data[symptom]
        response = f"""
        ### 🚫 Foods to Avoid
        {', '.join(info['avoid'])}

        ### ✅ Prevention Tips
        {', '.join(info['prevention'])}

        ### ⚠️ Precautions
        {', '.join(info['precautions'])}

        ### 🧠 Possible Diseases
        {', '.join(info['diseases'])}
        """
    else:
        response = "🤖 Sorry, I don't have data for that symptom yet. Try another one like 'vomiting' or 'fatigue'."

    st.chat_message("Bot").markdown(response)
import speech_recognition as sr

def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Speak your symptom...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        return "Sorry, I couldn't understand."
from googletrans import Translator

def translate_to_english(text):
    translator = Translator()
    translated = translator.translate(text, dest='en')
    return translated.text
emergency_keywords = ["chest pain", "shortness of breath", "severe bleeding", "loss of consciousness"]
import smtplib

def send_hospital_alert(symptom, location="Bhopal"):
    message = f"🚨 Emergency Alert: {symptom} reported near {location}. Immediate attention required."
    # Simulate email alert
    print("Sending alert:", message)
    # You can use SMTP or webhook here
import streamlit as st

st.title("🩺 Multilingual Voice-Enabled Health Chatbot")

if st.button("🎙️ Speak"):
    voice_input = listen_to_voice()
    st.write("You said:", voice_input)
    translated = translate_to_english(voice_input)
    st.write("Translated:", translated)

    if any(keyword in translated.lower() for keyword in emergency_keywords):
        send_hospital_alert(translated)
        st.error("🚨 Emergency detected! Hospital has been notified.")
    else:
        st.success("✅ No emergency detected.")
# BMI CALCULATOR
import streamlit as st

st.title("⚖️ BMI Calculator")

# Input fields
height_cm = st.number_input("Enter your height (cm)", min_value=50.0, max_value=250.0, step=0.1)
weight_kg = st.number_input("Enter your weight (kg)", min_value=10.0, max_value=300.0, step=0.1)

# Calculate BMI
if height_cm and weight_kg:
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 2)

    # Interpretation
    if bmi < 18.5:
        category = "Underweight"
        color = "blue"
    elif 18.5 <= bmi < 24.9:
        category = "Normal weight"
        color = "green"
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        color = "orange"
    else:
        category = "Obese"
        color = "red"

    st.metric(label="Your BMI", value=bmi)
    st.markdown(f"### 🧠 Category: <span style='color:{color}'>{category}</span>", unsafe_allow_html=True)
health_articles = [
    {
        "title": "Transforming Healthcare with Chatbots",
        "summary": "This review explores how AI-powered chatbots are revolutionizing healthcare—from mental health support to appointment management and COVID-19 triage.",
        "link": "https://journals.sagepub.com/doi/pdf/10.1177/20552076251319174"
    },
    {
        "title": "Reporting Guidelines for Chatbot Health Advice",
        "summary": "The CHART framework helps standardize how chatbot health advice studies are reported, improving transparency and reliability.",
        "link": "https://jamanetwork.com/journals/jamanetworkopen/fullarticle/2837224"
    },
    {
        "title": "Inclusive Healthcare Chatbots: A Systematic Review",
        "summary": "This article highlights the role of chatbots in inclusive healthcare, covering diagnostic support, self-monitoring, and ethical concerns.",
        "link": "https://link.springer.com/article/10.1007/s10209-024-01118-x"
    }
]
import streamlit as st

st.title("📰 Health Articles")

for article in health_articles:
    st.subheader(article["title"])
    st.write(article["summary"])
    st.markdown(f"[Read Full Article]({article['link']})")
    st.divider()
    # QUIZ SECTION
import streamlit as st

# Quiz data
quiz = [
    {
        "question": "Which vitamin is essential for blood clotting?",
        "options": ["Vitamin K", "Vitamin D", "Vitamin C", "Vitamin A"],
        "answer": 0,
        "explanation": "Vitamin K plays a crucial role in blood clotting by helping the body produce proteins needed for coagulation."
    },
    {
        "question": "Which of the following is a common symptom of dehydration?",
        "options": ["Cold hands", "Dry mouth", "Increased appetite",
                    "Blurred vision"],
        "answer": 1,
        "explanation": "Dry mouth is a common symptom of dehydration, along with fatigue, dizziness, and dark-colored urine."
    },
    {
        "question": "Which organ is primarily affected by jaundice?",
        "options": ["Kidneys", "Lungs", "Liver", "Heart"],
        "answer": 2,
        "explanation": "Jaundice is caused by elevated bilirubin levels due to liver dysfunction."
    },
    {
        "question": "Which of the following foods should be avoided during nausea?",
        "options": ["Boiled potatoes", "Ginger tea", "Greasy foods",
                    "Plain crackers"],
        "answer": 2,
        "explanation": "Greasy foods can worsen nausea by irritating the stomach lining."
    },
    {
        "question": "Which mineral is important for preventing fatigue and anemia?",
        "options": ["Zinc", "Iron", "Calcium", "Magnesium"],
        "answer": 1,
        "explanation": "Iron is essential for producing hemoglobin, which carries oxygen in the blood."
    },
    {
        "question": "Which of the following is a recommended prevention for diarrhea?",
        "options": ["Skipping meals", "Washing hands regularly",
                    "Eating raw seafood", "Drinking untreated water"],
        "answer": 1,
        "explanation": "Washing hands regularly helps prevent the spread of bacteria and viruses that cause diarrhea."
    },
    {
        "question": "Which of the following symptoms may indicate a migraine?",
        "options": ["Chest pain", "Blurred vision and headache",
                    "Swollen feet", "Cough and fever"],
        "answer": 1,
        "explanation": "Migraines often involve intense headaches, blurred vision, nausea, and sensitivity to light or sound."
    },
    {
        "question": "Which food is best avoided during vomiting episodes?",
        "options": ["Toast", "Spicy curry", "Boiled rice", "Bananas"],
        "answer": 1,
        "explanation": "Spicy foods like curry can irritate the stomach and worsen vomiting."
    },
    {
        "question": "Which of the following is a common cause of abdominal pain?",
        "options": ["Tooth decay", "Skin rash", "Appendicitis",
                    "Ear infection"],
        "answer": 2,
        "explanation": "Appendicitis is a common and serious cause of abdominal pain."
    },
    {
        "question": "Which precaution is recommended during dehydration?",
        "options": ["Avoid fluids", "Eat spicy food",
                    "Use oral rehydration salts", "Drink sugary sodas"],
        "answer": 2,
        "explanation": "Oral rehydration salts help restore lost electrolytes and fluids during dehydration."
    }
]

# Streamlit UI
st.title("🧠 Health Quiz Challenge")
st.write("Test your health knowledge and learn something new!")

score = 0

for i, q in enumerate(quiz):
    st.subheader(f"Q{i + 1}: {q['question']}")
    user_answer = st.radio("Choose your answer:", q["options"], key=f"q{i}")

    if st.button(f"Submit Answer {i + 1}", key=f"submit{i}"):
        correct = q["options"][q["answer"]]
        if user_answer == correct:
            st.success("✅ Correct!")
            score += 1
        else:
            st.error(f"❌ Incorrect. Correct answer: {correct}")
        st.info(f"🧠 Explanation: {q['explanation']}")

st.markdown("---")
st.metric("Your Score", f"{score} / {len(quiz)}")
# MOOD TRACKER
import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

# File to store mood logs
MOOD_LOG = "mood_log.csv"

# Load or create mood log
try:
    df = pd.read_csv(MOOD_LOG)
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Mood", "Note"])

# UI
st.title("🌤 Mood Tracker")
today = datetime.date.today()
st.write(f"Log your mood for **{today}**")

# Mood options
mood = st.selectbox("How are you feeling today?", ["😊 Happy", "😢 Sad", "😠 Angry", "😨 Anxious", "😴 Tired", "😐 Neutral"])
note = st.text_area("Want to add a note or reflection?", placeholder="Write about your day...")

if st.button("Save Mood"):
    new_entry = pd.DataFrame([[today, mood, note]], columns=["Date", "Mood", "Note"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(MOOD_LOG, index=False)
    st.success("✅ Mood saved!")

# Mood trends
st.subheader("📊 Mood Trends")
if not df.empty:
    mood_counts = df["Mood"].value_counts()
    st.bar_chart(mood_counts)

    # Show recent entries
    st.subheader("📝 Recent Entries")
    st.dataframe(df.tail(5))
else:
    st.info("No mood data yet. Start tracking today!")

# Inspirational quote
quotes = {
    "😊 Happy": "Keep shining. Your joy is contagious!",
    "😢 Sad": "It's okay to feel down. Tomorrow is a new day.",
    "😠 Angry": "Take a breath. You’re stronger than your anger.",
    "😨 Anxious": "You’ve survived 100% of your worst days.",
    "😴 Tired": "Rest is productive too. Recharge.",
    "😐 Neutral": "Even calm days matter. Stay grounded."
}
if mood in quotes:
    st.markdown(f"### 🌈 Quote of the Day\n> {quotes[mood]}")
# CUSTOM BACKGROUND
import streamlit as st

# Inject custom CSS for background
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] > div:first-child {
    background-image: url("")
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


