import  streamlit as st

st.title("welcome to the health dashboard")
import streamlit as st
import hashlib

# Dummy credentials
USER_DB = {
    "prince": hashlib.sha256("secure123".encode()).hexdigest(),
    "admin": hashlib.sha256("adminpass".encode()).hexdigest()
}

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

# Login Page
def login_page():
    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        if username in USER_DB and USER_DB[username] == hashed_pw:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.show_balloons = True  # Trigger balloons

        else:
            st.error("❌ Invalid username or password")

# Dashboard Page
def dashboard_page():
    if st.session_state.show_balloons:
        st.balloons()
        st.session_state.show_balloons = False  # Prevent repeat animation

    st.title("📊 Dashboard Homepage")
    st.write(f"Welcome, **{st.session_state.username}**! You're now inside the protected health assistant dashboard.")
    st.metric("Heart Rate", "72 bpm")
    st.metric("Blood Pressure", "120/80 mmHg")
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.experimental_rerun()

# Routing Logic
if st.session_state.logged_in:
    dashboard_page()
else:
    login_page()


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
mood_music = {
    "😊 Happy": {
        "playlist": "https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
        "suggestion": "Uplifting pop and feel-good beats to keep your energy high!"
    },
    "😢 Sad": {
        "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0",
        "suggestion": "Gentle acoustic and comforting melodies to soothe your heart."
    },
    "😠 Angry": {
        "playlist": "https://open.spotify.com/playlist/37i9dQZF1DWYxwmBaMqxsl",
        "suggestion": "Powerful rock and cathartic tracks to release tension."
    },
    "😨 Anxious": {
        "playlist": "https://open.spotify.com/playlist/37i9dQZF1DWU0ScTcjJBdj",
        "suggestion": "Calming ambient sounds and soft piano to ease your mind."
    },
    "😴 Tired": {
        "playlist": "https://open.spotify.com/playlist/37i9dQZF1DWZd79rJ6a7lp",
        "suggestion": "Sleep-inducing tones and slow rhythms for deep rest."
    },
    "😐 Neutral": {
        "playlist": "https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwq3LiO",
        "suggestion": "Balanced background music for focus and clarity."
    }
}
mood = st.selectbox("How are you feeling today?", list(mood_music.keys()))
selected = mood_music[mood]

st.subheader("🎵 Music Recommendation")
st.write(selected["suggestion"])
st.markdown(f"[Open Playlist]({selected['playlist']})")

# Optional: Embed Spotify player
st.markdown(f"""
<iframe src="https://open.spotify.com/embed/playlist/{selected['playlist'].split('/')[-1]}" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
""", unsafe_allow_html=True)
mood_meditation = {
    "😊 Happy": "https://www.youtube.com/watch?v=ZToicYcHIOU",
    "😢 Sad": "https://www.youtube.com/watch?v=4pLUleLdwY4",
    "😠 Angry": "https://www.youtube.com/watch?v=I0a3Wc3wC4c",
    "😨 Anxious": "https://www.youtube.com/watch?v=MIr3RsUWrdo",
    "😴 Tired": "https://www.youtube.com/watch?v=1vx8iUvfyCY",
    "😐 Neutral": "https://www.youtube.com/watch?v=inpok4MKVLM"
}

st.subheader("🧘 Guided Meditation")
st.markdown(f"[Start Meditation]({mood_meditation[mood]})")
import streamlit as st
import pandas as pd
import plotly.express as px

# Load mood log
df = pd.read_csv("mood_log.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Map moods to scores
mood_scores = {
    "😊 Happy": 5,
    "😐 Neutral": 3,
    "😢 Sad": 1,
    "😠 Angry": 2,
    "😨 Anxious": 2,
    "😴 Tired": 2
}
df["Mood Score"] = df["Mood"].map(mood_scores)

# Classy Plotly chart
st.subheader("📈 Your Mood Journey")
fig = px.line(
    df,
    x="Date",
    y="Mood Score",
    markers=True,
    text=df["Mood"],
    title="Mood Trend Over Time",
    color_discrete_sequence=["#00BFFF"],
)

fig.update_traces(
    line=dict(width=3),
    marker=dict(size=10, color="#FF69B4"),
    textposition="top center",
    hovertemplate="<b>Date:</b> %{x}<br><b>Mood:</b> %{text}<br><b>Score:</b> %{y}"
)

fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Mood Score (1–5)",
    plot_bgcolor="#F0F8FF",
    paper_bgcolor="#F8F8FF",
    font=dict(family="Arial", size=14),
    title_font=dict(size=20),
    margin=dict(t=60, b=40, l=20, r=20)
)

st.plotly_chart(fig, use_container_width=True)





import streamlit as st
import os
from datetime import datetime

# Directory to store reports
REPORT_DIR = "medical_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

# UI
st.title("🗂️ Medical Report Vault")
st.write("Upload, view, download, or delete your medical reports securely.")

# Upload section
uploaded_file = st.file_uploader("📤 Upload your medical report", type=["pdf", "jpg", "png", "jpeg"])
if uploaded_file:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    filepath = os.path.join(REPORT_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Report '{uploaded_file.name}' uploaded successfully!")

# List stored reports
st.subheader("📁 Your Stored Reports")
files = os.listdir(REPORT_DIR)
if files:
    for file in sorted(files, reverse=True):
        file_path = os.path.join(REPORT_DIR, file)
        st.markdown(f"📄 **{file}**")
        col1, col2 = st.columns([1, 1])
        with col1:
            with open(file_path, "rb") as f:
                st.download_button(label="⬇️ Download", data=f, file_name=file)
        with col2:
            if st.button(f"🗑️ Delete '{file}'", key=file):
                os.remove(file_path)
                st.warning(f"🗑️ '{file}' has been deleted.")

else:
    st.info("No reports uploaded yet.")
import streamlit as st
import pandas as pd

# Sample data (can be replaced with live data or database)
data = {
    "Disease": [
        "Acute Diarrheal Disease (ADD)",
        "Typhoid",
        "Cholera",
        "Hepatitis A",
        "Hepatitis E",
        "Shigellosis",
        "Japanese Encephalitis",
        "Scrub Typhus"
    ],
    "Cases": [1240, 870, 430, 520, 310, 290, 150, 180]
}

df = pd.DataFrame(data)

# UI
st.title("💬 Waterborne Disease Chat")
st.write("📍 Region: Rural Northeast India")
st.write("🧪 Showing latest disease burden and case counts")

# Display disease data
for i, row in df.iterrows():
    st.markdown(f"""
    **🦠 Disease:** {row['Disease']}  
    **📊 Cases Reported:** {row['Cases']}  
    ---
    """)

# Summary
total_cases = df["Cases"].sum()
st.success(f"✅ Total Waterborne Disease Cases Reported: {total_cases}")

# Optional: Add filters or chatbot-style input
st.subheader("🔍 Ask about a specific disease")
query = st.text_input("Type disease name (e.g., Cholera)")
if query:
    match = df[df["Disease"].str.contains(query, case=False)]
    if not match.empty:
        for _, row in match.iterrows():
            st.info(f"{row['Disease']} has {row['Cases']} reported cases.")
    else:
        st.warning("Disease not found in current dataset.")
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# File to store appointments
APPT_FILE = "appointments.csv"
if not os.path.exists(APPT_FILE):
    pd.DataFrame(columns=["Name", "Date", "Time", "Message"]).to_csv(APPT_FILE, index=False)

# Title
st.title("📅 Appointment Reminder System")

# Form to schedule appointment
with st.form("schedule_form"):
    name = st.text_input("Patient Name")
    date = st.date_input("Appointment Date", min_value=datetime.today())
    time = st.time_input("Appointment Time")
    message = st.text_area("Reminder Message", value="This is a reminder for your upcoming appointment.")
    submit = st.form_submit_button("📌 Schedule Appointment")

# Save appointment
if submit:
    new_appt = pd.DataFrame([[name, date.strftime("%Y-%m-%d"), time.strftime("%H:%M"), message]],
                            columns=["Name", "Date", "Time", "Message"])
    df = pd.read_csv(APPT_FILE)
    df = pd.concat([df, new_appt], ignore_index=True)
    df.to_csv(APPT_FILE, index=False)
    st.success(f"✅ Appointment for {name} scheduled on {date} at {time.strftime('%H:%M')}")

# Load and show upcoming appointments
st.subheader("📋 Upcoming Appointments")
df = pd.read_csv(APPT_FILE)
if not df.empty:
    df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="mixed" )
    upcoming = df[df["DateTime"] >= datetime.now()].sort_values("DateTime")
    st.dataframe(upcoming[["Name", "Date", "Time", "Message"]])
else:
    st.info("No appointments scheduled yet.")




