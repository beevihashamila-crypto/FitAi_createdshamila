import streamlit as st
import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import random

# Add modules to path
sys.path.append(os.path.dirname(__file__))

# Page config
st.set_page_config(
    page_title="FitAi",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple CSS

st.markdown("""
<style>

/* ====== GLOBAL BACKGROUND ====== */
.stApp {
    background: linear-gradient(135deg, #050b0a, #071f14, #042b1a);
    color: #eafff5;
}

/* ====== MAIN HEADER (HOME TITLE) ====== */
.main-header {
    font-size: 3.2rem;
    background: linear-gradient(90deg, #00ff87, #00d4ff, #9b5cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-weight: 900;
    letter-spacing: 2px;
    margin-bottom: 2.5rem;
    text-shadow: 0 0 25px rgba(0,255,135,0.35);
}

/* ====== SECTION HEADERS ====== */
.section-header {
    font-size: 1.7rem;
    color: #00ff87;
    margin: 2rem 0 1.2rem 0;
    font-weight: 700;
    border-left: 5px solid #00ff87;
    padding-left: 12px;
}

/* ====== METRIC CARDS ====== */
[data-testid="metric-container"] {
    background: rgba(0, 40, 25, 0.85);
    border-radius: 20px;
    padding: 1.4rem;
    border: 1px solid rgba(0, 255, 135, 0.35);
    box-shadow: 0 0 25px rgba(0,255,135,0.15);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

[data-testid="metric-container"]:hover {
    transform: translateY(-6px);
    box-shadow: 0 0 40px rgba(0,255,135,0.35);
}

/* ====== RECENT ACTIVITY CARDS ====== */
.metric-card {
    background: linear-gradient(135deg, rgba(0,255,135,0.15), rgba(0,120,255,0.15));
    border-radius: 20px;
    padding: 1.6rem;
    border: 1px solid rgba(0, 255, 135, 0.4);
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}

/* ====== BUTTONS ====== */
.stButton > button {
    background: linear-gradient(90deg, #00ff87, #00c6ff);
    color: #002018;
    font-weight: 800;
    border-radius: 14px;
    border: none;
    padding: 0.7rem 1rem;
    box-shadow: 0 0 20px rgba(0,255,135,0.4);
}

.stButton > button:hover {
    background: linear-gradient(90deg, #00c6ff, #9b5cff);
    color: white;
    transform: scale(1.03);
}

/* ====== SIDEBAR USER NAME (BIG & VISIBLE) ====== */
section[data-testid="stSidebar"] strong {
    font-size: 1.4rem !important;
    color: #00ff87 !important;
    text-shadow: 0 0 15px rgba(0,255,135,0.8);
}

/* ====== WELCOME SUCCESS BOX ====== */
.stAlert.success {
    background: linear-gradient(135deg, rgba(0,255,135,0.25), rgba(0,120,255,0.25));
    border-radius: 16px;
    border: 1px solid rgba(0,255,135,0.4);
    box-shadow: 0 0 30px rgba(0,255,135,0.3);
    font-size: 1.1rem;
    font-weight: 600;
}

/* ====== REMOVE STREAMLIT WHITE BLOCK FEEL ====== */
.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>

/* ===== BIG USER NAME ON HOME PAGE ===== */
.home-username {
    font-size: 3.2rem;
    font-weight: 900;
    text-align: center;
    background: linear-gradient(90deg, #00ff87, #00c6ff, #9b5cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: 1rem;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 30px rgba(0,255,135,0.6);
}

/* ===== SUBTEXT UNDER NAME ===== */
.home-subtext {
    text-align: center;
    font-size: 1.2rem;
    color: #caffea;
    margin-bottom: 2rem;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ===== FULL SCREEN HERO ===== */
.hero-section {
    height: 90vh;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    background: radial-gradient(circle at top, #00ff87 0%, #042b1a 45%, #020807 100%);
    margin: -3rem -3rem 3rem -3rem;
    border-bottom-left-radius: 40px;
    border-bottom-right-radius: 40px;
}

/* ===== FIT AI TITLE ===== */
.hero-title {
    font-size: 5rem;
    font-weight: 900;
    letter-spacing: 6px;
    background: linear-gradient(90deg, #ffffff, #00ff87, #00c6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(0,255,135,0.8);
}

/* ===== HERO SUBTITLE ===== */
.hero-subtitle {
    margin-top: 1rem;
    font-size: 1.4rem;
    color: #eafff5;
    opacity: 0.9;
}

/* ===== SCROLL HINT ===== */
.scroll-down {
    position: absolute;
    bottom: 30px;
    font-size: 1rem;
    color: #eafff5;
    opacity: 0.8;
}

</style>
""", unsafe_allow_html=True)



# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'profile_data': {
            'personal': {
                'name': '', 
                'age': 25, 
                'gender': 'Male', 
                'height': 170, 
                'weight': 70,
                'email': '',
                'phone': '',
                'location': ''
            },
            'goals': {
                'primary_goal': 'weight_loss', 
                'target_weight': 65,
                'target_date': '',
                'fitness_level': 'beginner',
                'weekly_workouts': 3
            },
            'nutrition': {
                'water_target': 8,
                'calorie_target': 2000,
                'dietary_preferences': [],
                'allergies': ''
            },
            'lifestyle': {
                'activity_level': 'Moderate',
                'sleep_target': 8,
                'occupation': '',
                'hobbies': ''
            },
            'medical': {
                'conditions': '',
                'medications': '',
                'injuries': ''
            }
        },
        'workout_history': [],
        'nutrition_logs': [],
        'water_intake': 0,
        'sleep_hours': 7,
        'current_mood': 'neutral',
        'streak_days': 0,
        'total_points': 0,
        'level': 1,
        'badges': [],
        'water_history': [],
        'sleep_history': [],
        'mood_history': [],
        'stress_history': [],
        'heart_rate_data': [],
        'blood_pressure_data': [],
        'active_challenges': [],
        'redeemed_rewards': [],
        'custom_workouts': [],
        'favorite_foods': [],
        'meal_plans': [],
        'current_page': '🏠 Home'
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Initialize session state
initialize_session_state()

# Sidebar navigation
st.sidebar.title("🏋️‍♂️ FitAi")
st.sidebar.markdown("---")

# User info in sidebar
if 'profile_data' in st.session_state:
    profile = st.session_state.profile_data
    name = profile['personal'].get('name', 'Guest User')
    if name:
        st.sidebar.markdown(f"**👤 {name}**")

# Navigation menu
st.sidebar.markdown("### 🧭 Navigation")

# Define navigation options
nav_options = [
    {"icon": "🏠", "label": "Home", "key": "home"},
    {"icon": "👤", "label": "Profile", "key": "profile"},
    {"icon": "🏋️‍♂️", "label": "Workout", "key": "workout"},
    {"icon": "🍎", "label": "Nutrition", "key": "nutrition"},
    {"icon": "❤️", "label": "Health", "key": "health"},
    {"icon": "📈", "label": "Progress", "key": "progress"},
    {"icon": "🎮", "label": "Gamification", "key": "gamification"},
    {"icon": "🤖", "label": "AI Coach", "key": "ai_coach"}
]

# Create navigation buttons
for option in nav_options:
    if st.sidebar.button(f"{option['icon']} {option['label']}", 
                        key=f"nav_{option['key']}",
                        use_container_width=True):
        st.session_state.current_page = f"{option['icon']} {option['label']}"
        st.rerun()

st.sidebar.markdown("---")

# Quick stats in sidebar
st.sidebar.markdown("### 📊 Quick Stats")

# Streak display
streak = st.session_state.get('streak_days', 0)
st.sidebar.metric("🔥 Streak", f"{streak} days")

# Today's water
water = st.session_state.get('water_intake', 0)
water_target = st.session_state.profile_data.get('nutrition', {}).get('water_target', 8)
st.sidebar.metric("💧 Water", f"{water}/{water_target} glasses")

# Today's workouts
if 'workout_history' in st.session_state:
    today = datetime.now().strftime("%Y-%m-%d")
    today_workouts = [w for w in st.session_state.workout_history if w.get('date') == today]
    workout_count = len(today_workouts)
else:
    workout_count = 0

st.sidebar.metric("🏋️‍♂️ Workouts", workout_count)

# Quick actions in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### ⚡ Quick Actions")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("💧 +1", help="Log 1 Glass of Water", use_container_width=True):
        st.session_state.water_intake += 1
        st.session_state.water_history.append({
            'date': datetime.now().strftime("%Y-%m-%d"),
            'time': datetime.now().strftime("%H:%M"),
            'amount': 1
        })
        st.success("Logged 1 glass of water!")
        st.rerun()

with col2:
    if st.button("🍎 Meal", help="Quick Meal Log", use_container_width=True):
        meal_options = {
            "Apple": {"calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3},
            "Protein Shake": {"calories": 150, "protein": 30, "carbs": 5, "fat": 2},
            "Greek Yogurt": {"calories": 100, "protein": 18, "carbs": 6, "fat": 0.5},
            "Mixed Nuts": {"calories": 170, "protein": 6, "carbs": 6, "fat": 15}
        }
        
        food_item = random.choice(list(meal_options.keys()))
        nutrition = meal_options[food_item]
        
        st.session_state.nutrition_logs.append({
            'date': datetime.now().strftime("%Y-%m-%d"),
            'meal': 'Snack',
            'food': food_item,
            'calories': nutrition['calories'],
            'protein': nutrition['protein'],
            'carbs': nutrition['carbs'],
            'fat': nutrition['fat'],
            'time': datetime.now().strftime("%H:%M")
        })
        
        st.success(f"Logged {food_item} as a snack!")
        st.rerun()

# Main content area based on current page
current_page = st.session_state.current_page

if current_page == "🏠 Home":
    st.markdown("""
<div class="hero-section">
    <div class="hero-title">FIT AI</div>
    <div class="hero-subtitle">Your Personal AI Fitness Coach</div>
    <div class="scroll-down">⬇ Scroll to continue</div>
</div>
""", unsafe_allow_html=True)

    # Dashboard/Home Page
    st.markdown('<h1 class="main-header">🏋️‍♂️ AI FITNESS COACH</h1>', unsafe_allow_html=True)
    
    # Welcome message
    name = st.session_state.profile_data['personal'].get('name', 'Fitness Enthusiast')
    goal = st.session_state.profile_data['goals'].get('primary_goal', 'fitness')
    goal_text = goal.replace('_', ' ').title()
    
    st.markdown(f"<div class='home-username'>{name}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='home-subtext'>🎯 Current Goal: <b>{goal_text}</b></div>", unsafe_allow_html=True)

    
    # Quick stats row
    st.markdown('<div class="section-header">📊 Today\'s Overview</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # BMI
        height = st.session_state.profile_data['personal']['height']
        weight = st.session_state.profile_data['personal']['weight']
        if height > 0:
            height_m = height / 100
            bmi = weight / (height_m ** 2)
        else:
            bmi = 0
        
        st.metric("⚖️ BMI", f"{bmi:.1f}")
    
    with col2:
        # Calories burned today
        today = datetime.now().strftime("%Y-%m-%d")
        today_calories = sum(w.get('calories', 0) for w in st.session_state.workout_history if w.get('date') == today)
        st.metric("🔥 Calories Burned", today_calories)
    
    with col3:
        # Protein today
        today_protein = sum(log.get('protein', 0) for log in st.session_state.nutrition_logs if log.get('date') == today)
        st.metric("🥚 Protein", f"{today_protein:.0f}g")
    
    with col4:
        # Sleep
        sleep = st.session_state.get('sleep_hours', 0)
        st.metric("💤 Sleep", f"{sleep:.1f}h")
    
    # Recent Activity
    st.markdown('<div class="section-header">📈 Recent Activity</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏋️‍♂️ Recent Workouts")
        if st.session_state.workout_history:
            recent_workouts = st.session_state.workout_history[-3:][::-1]
            for workout in recent_workouts:
                st.write(f"**{workout.get('name', 'Workout')}**")
                st.caption(f"{workout.get('date', '')} • {workout.get('duration', 0)}min • 🔥 {workout.get('calories', 0)}")
        else:
            st.info("No workouts yet. Start your first workout!")
    
    with col2:
        st.subheader("🍎 Recent Meals")
        if st.session_state.nutrition_logs:
            recent_meals = st.session_state.nutrition_logs[-3:][::-1]
            for meal in recent_meals:
                st.write(f"**{meal.get('meal', 'Meal')}**: {meal.get('food', 'Food')}")
                st.caption(f"{meal.get('time', '')} • 🔥 {meal.get('calories', 0)}")
        else:
            st.info("No meals logged yet. Log your first meal!")
    
    # Quick Start Section
    st.markdown('<div class="section-header">🚀 Quick Start</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🏃 Start Workout", use_container_width=True, type="primary"):
            st.session_state.current_page = "🏋️‍♂️ Workout"
            st.rerun()
    
    with col2:
        if st.button("🍎 Log Meal", use_container_width=True, type="primary"):
            st.session_state.current_page = "🍎 Nutrition"
            st.rerun()
    
    with col3:
        if st.button("❤️ Log Health", use_container_width=True):
            st.session_state.current_page = "❤️ Health"
            st.rerun()
    
    with col4:
        if st.button("📊 View Progress", use_container_width=True):
            st.session_state.current_page = "📈 Progress"
            st.rerun()

elif current_page == "👤 Profile":
    # Profile Page
    st.markdown('<h1 class="main-header">👤 PROFILE</h1>', unsafe_allow_html=True)
    
    # Create tabs for different profile sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Personal Info", 
        "🎯 Goals", 
        "🥗 Nutrition", 
        "🏃 Lifestyle", 
        "🏥 Medical"
    ])
    
    with tab1:
        st.subheader("Personal Information")
        
        with st.form("personal_info_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", value=st.session_state.profile_data['personal'].get('name', ''))
                age = st.number_input("Age", min_value=13, max_value=100, value=st.session_state.profile_data['personal'].get('age', 25))
                gender = st.selectbox("Gender", ["Male", "Female", "Other", "Prefer not to say"], 
                                    index=["Male", "Female", "Other", "Prefer not to say"].index(
                                        st.session_state.profile_data['personal'].get('gender', 'Male')))
            
            with col2:
                height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, 
                                       value=float(st.session_state.profile_data['personal'].get('height', 170.0)))
                weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, 
                                       value=float(st.session_state.profile_data['personal'].get('weight', 70.0)))
                email = st.text_input("Email", value=st.session_state.profile_data['personal'].get('email', ''))
            
            if st.form_submit_button("💾 Save Personal Information", type="primary", use_container_width=True):
                st.session_state.profile_data['personal'].update({
                    'name': name, 'age': age, 'gender': gender,
                    'height': height, 'weight': weight, 'email': email
                })
                st.success("Personal information saved successfully!")
                st.rerun()
    
    with tab2:
        st.subheader("Fitness Goals")
        
        with st.form("goals_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                primary_goal = st.selectbox("Primary Goal", ["weight_loss", "muscle_gain", "maintenance", "endurance", "strength"])
                target_weight = st.number_input("Target Weight (kg)", min_value=30.0, max_value=200.0, 
                                              value=float(st.session_state.profile_data['goals'].get('target_weight', 65.0)))
            
            with col2:
                fitness_level = st.selectbox("Fitness Level", ["beginner", "intermediate", "advanced", "athlete"])
                weekly_workouts = st.slider("Weekly Workout Target", 1, 7, st.session_state.profile_data['goals'].get('weekly_workouts', 3))
            
            if st.form_submit_button("🎯 Save Goals", type="primary", use_container_width=True):
                st.session_state.profile_data['goals'].update({
                    'primary_goal': primary_goal,
                    'target_weight': target_weight,
                    'fitness_level': fitness_level,
                    'weekly_workouts': weekly_workouts
                })
                st.success("Goals saved successfully!")
                st.rerun()
    
    with tab3:
        st.subheader("Nutrition Preferences")
        
        with st.form("nutrition_form"):
            water_target = st.slider("Daily Water Target (glasses)", 4, 15, st.session_state.profile_data['nutrition'].get('water_target', 8))
            calorie_target = st.number_input("Daily Calorie Target", 1000, 5000, st.session_state.profile_data['nutrition'].get('calorie_target', 2000))
            
            if st.form_submit_button("🥗 Save Nutrition Preferences", type="primary", use_container_width=True):
                st.session_state.profile_data['nutrition'].update({
                    'water_target': water_target,
                    'calorie_target': calorie_target
                })
                st.success("Nutrition preferences saved successfully!")
                st.rerun()
    
    with tab4:
        st.subheader("Lifestyle Information")
        
        with st.form("lifestyle_form"):
            activity_level = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])
            sleep_target = st.slider("Sleep Target (hours)", 4.0, 12.0, float(st.session_state.profile_data['lifestyle'].get('sleep_target', 8.0)), 0.5)
            
            if st.form_submit_button("🏃 Save Lifestyle Info", type="primary", use_container_width=True):
                st.session_state.profile_data['lifestyle'].update({
                    'activity_level': activity_level,
                    'sleep_target': sleep_target
                })
                st.success("Lifestyle information saved successfully!")
                st.rerun()
    
    with tab5:
        st.subheader("Medical Information")
        st.info("⚠️ This information is stored locally and is for fitness guidance only.")
        
        with st.form("medical_form"):
            conditions = st.text_area("Medical Conditions", value=st.session_state.profile_data['medical'].get('conditions', ''))
            medications = st.text_area("Current Medications", value=st.session_state.profile_data['medical'].get('medications', ''))
            
            if st.form_submit_button("🏥 Save Medical Information", type="primary", use_container_width=True):
                st.session_state.profile_data['medical'].update({
                    'conditions': conditions,
                    'medications': medications
                })
                st.success("Medical information saved successfully!")
                st.rerun()
    
    # Profile summary
    st.markdown("---")
    st.subheader("📋 Profile Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Personal Stats**")
        st.write(f"Age: {st.session_state.profile_data['personal'].get('age', 'N/A')}")
        st.write(f"Height: {st.session_state.profile_data['personal'].get('height', 'N/A')} cm")
        st.write(f"Weight: {st.session_state.profile_data['personal'].get('weight', 'N/A')} kg")
        
        # Calculate BMI
        height = st.session_state.profile_data['personal'].get('height', 170)
        weight = st.session_state.profile_data['personal'].get('weight', 70)
        if height > 0:
            bmi = weight / ((height/100) ** 2)
            st.write(f"BMI: {bmi:.1f}")
    
    with col2:
        st.write("**Fitness Goals**")
        st.write(f"Primary Goal: {st.session_state.profile_data['goals'].get('primary_goal', 'N/A').replace('_', ' ').title()}")
        st.write(f"Target Weight: {st.session_state.profile_data['goals'].get('target_weight', 'N/A')} kg")
        st.write(f"Fitness Level: {st.session_state.profile_data['goals'].get('fitness_level', 'N/A').title()}")
        st.write(f"Weekly Workouts: {st.session_state.profile_data['goals'].get('weekly_workouts', 'N/A')}")

elif current_page == "🏋️‍♂️ Workout":
    st.markdown('<h1 class="main-header">🏋️‍♂️ WORKOUT PLANNER</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📅 Weekly Plan", "💪 Start Workout", "📊 Workout History"])
    
    with tab1:
        st.subheader("Your Weekly Workout Plan")
        
        # Sample workout plan
        workout_days = {
            "Monday": "Chest & Triceps",
            "Tuesday": "Back & Biceps",
            "Wednesday": "Legs & Shoulders",
            "Thursday": "Rest Day",
            "Friday": "Full Body",
            "Saturday": "Cardio",
            "Sunday": "Active Recovery"
        }
        
        today = datetime.now().strftime('%A')
        
        for day, workout in workout_days.items():
            if day == today:
                st.success(f"**{day} (TODAY):** {workout}")
            else:
                st.write(f"**{day}:** {workout}")
    
    with tab2:
        st.subheader("Start a Workout")
        
        with st.form("start_workout_form"):
            workout_type = st.selectbox("Workout Type", ["Strength Training", "Cardio", "HIIT", "Yoga", "Custom"])
            duration = st.slider("Duration (minutes)", 10, 120, 45)
            intensity = st.slider("Intensity (1-10)", 1, 10, 7)
            notes = st.text_area("Notes")
            
            if st.form_submit_button("🏁 Start Workout", type="primary", use_container_width=True):
                # Calculate calories (simplified formula)
                weight = st.session_state.profile_data['personal'].get('weight', 70)
                calories = int((weight * duration * intensity) / 100)
                
                workout_record = {
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'time': datetime.now().strftime("%H:%M"),
                    'name': f"{workout_type} Workout",
                    'duration': duration,
                    'calories': calories,
                    'type': workout_type,
                    'intensity': intensity,
                    'notes': notes
                }
                
                st.session_state.workout_history.append(workout_record)
                st.session_state.streak_days += 1
                st.session_state.total_points += calories // 10
                
                st.success(f"Workout completed! Burned approximately {calories} calories.")
                st.rerun()
    
    with tab3:
        st.subheader("Workout History")
        
        if st.session_state.workout_history:
            for workout in st.session_state.workout_history[-10:][::-1]:
                with st.expander(f"{workout['date']} - {workout['name']}"):
                    st.write(f"**Duration:** {workout['duration']} min")
                    st.write(f"**Calories:** {workout['calories']}")
                    st.write(f"**Intensity:** {workout.get('intensity', 'N/A')}/10")

                    if workout.get('notes'):
                        st.write(f"**Notes:** {workout['notes']}")
        else:
            st.info("No workout history yet.")

elif current_page == "🍎 Nutrition":
    st.markdown('<h1 class="main-header">🍎 NUTRITION</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📝 Food Log", "🥗 Meal Plan", "📊 Nutrition Stats"])
    
    with tab1:
        st.subheader("Log Your Food")
        
        with st.form("food_log_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                meal_type = st.selectbox("Meal Type", ["Breakfast", "Lunch", "Dinner", "Snack", "Other"])
                food_name = st.text_input("Food/Meal Name", placeholder="e.g., Grilled Chicken Salad")
                calories = st.number_input("Calories", 0, 2000, 300)
            
            with col2:
                protein = st.number_input("Protein (g)", 0.0, 100.0, 20.0, 0.5)
                carbs = st.number_input("Carbohydrates (g)", 0.0, 200.0, 30.0, 0.5)
                fat = st.number_input("Fat (g)", 0.0, 100.0, 10.0, 0.5)
            
            if st.form_submit_button("📝 Log This Meal", type="primary", use_container_width=True):
                if food_name:
                    meal_log = {
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'time': datetime.now().strftime("%H:%M"),
                        'meal': meal_type,
                        'food': food_name,
                        'calories': calories,
                        'protein': protein,
                        'carbs': carbs,
                        'fat': fat
                    }
                    
                    st.session_state.nutrition_logs.append(meal_log)
                    st.success(f"Logged {food_name} for {meal_type}!")
                    st.rerun()
                else:
                    st.error("Please enter a food name.")
    
    with tab2:
        st.subheader("Today's Meal Plan")
        
        meal_plan = {
            "Breakfast": "Oatmeal with berries and nuts (300 cal)",
            "Lunch": "Grilled chicken salad with quinoa (450 cal)",
            "Dinner": "Salmon with roasted vegetables (500 cal)",
            "Snacks": "Greek yogurt and apple (200 cal)"
        }
        
        for meal, description in meal_plan.items():
            with st.expander(f"{meal}"):
                st.write(description)
                if st.button(f"Mark as eaten", key=f"eat_{meal}"):
                    st.success(f"Marked {meal} as eaten!")
    
    with tab3:
        st.subheader("Nutrition Statistics")
        
        if st.session_state.nutrition_logs:
            today = datetime.now().strftime("%Y-%m-%d")
            today_meals = [m for m in st.session_state.nutrition_logs if m.get('date') == today]
            
            if today_meals:
                total_calories = sum(m.get('calories', 0) for m in today_meals)
                total_protein = sum(m.get('protein', 0) for m in today_meals)
                total_carbs = sum(m.get('carbs', 0) for m in today_meals)
                total_fat = sum(m.get('fat', 0) for m in today_meals)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Calories", f"{total_calories}")
                
                with col2:
                    st.metric("Protein", f"{total_protein:.1f}g")
                
                with col3:
                    st.metric("Carbs", f"{total_carbs:.1f}g")
                
                with col4:
                    st.metric("Fat", f"{total_fat:.1f}g")
                
                # Show today's meals
                st.write("**Today's Meals:**")
                for meal in today_meals:
                    st.write(f"- {meal['time']}: {meal['meal']} - {meal['food']} ({meal['calories']} cal)")
            else:
                st.info("No meals logged today yet.")
        else:
            st.info("No nutrition data available.")

elif current_page == "❤️ Health":
    st.markdown('<h1 class="main-header">❤️ HEALTH TRACKER</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["😴 Sleep", "💧 Hydration", "❤️ Vital Signs"])
    
    with tab1:
        st.subheader("Sleep Monitor")
        
        with st.form("sleep_form"):
            hours = st.slider("Sleep Duration (hours)", 3.0, 12.0, float(st.session_state.get('sleep_hours', 7.0)), 0.5)
            quality = st.slider("Sleep Quality (1-10)", 1, 10, 7)
            
            if st.form_submit_button("💾 Log Sleep", type="primary", use_container_width=True):
                st.session_state.sleep_hours = hours
                st.session_state.sleep_history.append({
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'hours': hours,
                    'quality': quality
                })
                st.success(f"Logged {hours} hours of sleep!")
                st.rerun()
    
    with tab2:
        st.subheader("Hydration Tracker")
        
        water = st.session_state.get('water_intake', 0)
        water_target = st.session_state.profile_data.get('nutrition', {}).get('water_target', 8)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Water Intake", f"{water} glasses")
            st.metric("Target", f"{water_target} glasses")
        
        with col2:
            water_percent = min((water / water_target) * 100, 100) if water_target > 0 else 0
            st.progress(water_percent / 100)
            st.write(f"{water_percent:.1f}% of target")
        
        st.write("**Quick Log:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💧 +1 Glass", use_container_width=True):
                st.session_state.water_intake += 1
                st.success("Added 1 glass of water!")
                st.rerun()
        
        with col2:
            if st.button("💧💧 +2 Glasses", use_container_width=True):
                st.session_state.water_intake += 2
                st.success("Added 2 glasses of water!")
                st.rerun()
        
        with col3:
            if st.button("💧 Reset", use_container_width=True):
                st.session_state.water_intake = 0
                st.success("Reset water intake!")
                st.rerun()
    
    with tab3:
        st.subheader("Vital Signs")
        
        with st.form("vitals_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                heart_rate = st.number_input("Heart Rate (bpm)", 40, 200, 75)
                systolic = st.number_input("Blood Pressure - Systolic", 80, 200, 120)
            
            with col2:
                diastolic = st.number_input("Blood Pressure - Diastolic", 50, 150, 80)
                stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
            
            if st.form_submit_button("❤️ Log Vital Signs", type="primary", use_container_width=True):
                st.session_state.heart_rate_data.append({
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'time': datetime.now().strftime("%H:%M"),
                    'bpm': heart_rate
                })
                
                st.session_state.blood_pressure_data.append({
                    'date': datetime.now().strftime("%Y-%m-%d"),
                    'time': datetime.now().strftime("%H:%M"),
                    'systolic': systolic,
                    'diastolic': diastolic
                })
                
                st.success("Vital signs logged successfully!")
                st.rerun()

elif current_page == "📈 Progress":
    st.markdown('<h1 class="main-header">📈 PROGRESS ANALYTICS</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Trends", "🏆 Achievements"])
    
    with tab1:
        st.subheader("Progress Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            current_weight = st.session_state.profile_data['personal'].get('weight', 70)
            target_weight = st.session_state.profile_data['goals'].get('target_weight', 65)
            weight_diff = current_weight - target_weight
            st.metric("Weight Progress", f"{current_weight} kg", f"{-weight_diff:.1f} kg to go")
        
        with col2:
            streak = st.session_state.get('streak_days', 0)
            st.metric("🔥 Streak", f"{streak} days")
        
        with col3:
            weekly_target = st.session_state.profile_data['goals'].get('weekly_workouts', 3)
            week_workouts = len([w for w in st.session_state.workout_history 
                               if w.get('date') and 
                               datetime.strptime(w['date'], "%Y-%m-%d") >= datetime.now() - timedelta(days=7)])
            st.metric("Weekly Workouts", f"{week_workouts}/{weekly_target}")
        
        with col4:
            week_meals = len([m for m in st.session_state.nutrition_logs 
                            if m.get('date') and 
                            datetime.strptime(m['date'], "%Y-%m-%d") >= datetime.now() - timedelta(days=7)])
            st.metric("Meals Logged", f"{week_meals}")
        
        # Health Recommendations
        st.subheader("Health Recommendations")
        
        recommendations = []
        
        if st.session_state.get('sleep_hours', 7) < 7:
            recommendations.append("😴 **Sleep:** Aim for 7-9 hours of sleep per night")
        
        if st.session_state.get('water_intake', 0) < st.session_state.profile_data['nutrition'].get('water_target', 8) * 0.8:
            recommendations.append("💧 **Hydration:** Drink more water throughout the day")
        
        if recommendations:
            for rec in recommendations:
                st.info(rec)
        else:
            st.success("Great job! You're on track with your health goals.")
    
    with tab2:
        st.subheader("Progress Trends")
        
        # Create sample data
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        current_weight = st.session_state.profile_data['personal'].get('weight', 70)
        target_weight = st.session_state.profile_data['goals'].get('target_weight', 65)
        
        # Generate weight trend
        weight_trend = [current_weight + i * 0.1 * (-1 if current_weight > target_weight else 1) 
                       for i in range(30)]
        
        weight_df = pd.DataFrame({
            'Date': dates,
            'Weight': weight_trend
        })
        
        st.line_chart(weight_df.set_index('Date')['Weight'])
        st.caption("Weight Trend (Last 30 Days)")
    
    with tab3:
        st.subheader("Achievements & Milestones")
        
        achievements = []
        streak = st.session_state.get('streak_days', 0)
        
        if streak >= 7:
            achievements.append("🔥 **7-Day Streak:** Consistent for a full week!")
        
        if streak >= 30:
            achievements.append("🔥 **30-Day Streak:** Fitness master!")
        
        if st.session_state.workout_history:
            total_workouts = len(st.session_state.workout_history)
            if total_workouts >= 10:
                achievements.append("💪 **10 Workouts:** Getting stronger!")
            
            if total_workouts >= 50:
                achievements.append("💪 **50 Workouts:** Fitness champion!")
        
        if achievements:
            for achievement in achievements:
                st.success(achievement)
        else:
            st.info("Keep going! Achievements will unlock as you progress.")

elif current_page == "🎮 Gamification":
    st.markdown('<h1 class="main-header">🎮 GAMIFICATION</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🏆 Level", st.session_state.get('level', 1))
    
    with col2:
        st.metric("⭐ Points", st.session_state.get('total_points', 0))
    
    with col3:
        st.metric("🔥 Streak", st.session_state.get('streak_days', 0))
    
    # Badges display
    st.subheader("🏅 Your Badges")
    badges = st.session_state.get('badges', [])
    if badges:
        for badge in badges:
            st.write(f"✅ {badge}")
    else:
        st.info("Complete challenges to earn badges!")
    
    # Challenges
    st.subheader("📋 Current Challenges")
    
    challenges = [
        {"name": "Complete 5 workouts", "progress": min(len(st.session_state.workout_history) / 5, 1)},
        {"name": "Log 10 meals", "progress": min(len(st.session_state.nutrition_logs) / 10, 1)},
        {"name": "7-day streak", "progress": min(st.session_state.get('streak_days', 0) / 7, 1)}
    ]
    
    for challenge in challenges:
        st.write(f"**{challenge['name']}**")
        st.progress(challenge['progress'])

elif current_page == "🤖 AI Coach":
    st.markdown('<h1 class="main-header">🤖 AI FITNESS COACH</h1>', unsafe_allow_html=True)
    
    # Initialize chat messages
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": "Hi! I'm your AI Fitness Coach. How can I help you today?"}
        ]
    
    # Display chat messages
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about fitness, nutrition, or health..."):
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        
        # Simple AI responses
        if "workout" in prompt.lower():
            response = "I recommend starting with 3-4 workouts per week. Focus on compound exercises like squats, push-ups, and rows."
        elif "diet" in prompt.lower() or "nutrition" in prompt.lower():
            response = "A balanced diet with protein, healthy carbs, and fats is key. Aim for 1.6-2.2g of protein per kg of body weight."
        elif "weight loss" in prompt.lower():
            response = "For weight loss, focus on a calorie deficit of 300-500 calories per day and combine cardio with strength training."
        else:
            response = "I can help with workout plans, nutrition advice, and health tracking. What specific area would you like to discuss?"
        
        st.session_state.chat_messages.append({"role": "assistant", "content": response})
        st.rerun()
    
    # Quick questions
    st.subheader("💬 Quick Questions")
    
    col1, col2 = st.columns(2)
    
    quick_questions = [
        ("What's a good beginner workout?", "💪"),
        ("How much protein do I need?", "🥚"),
        ("Best exercises for weight loss?", "🔥"),
        ("How to stay motivated?", "🚀")
    ]
    
    for i, (question, icon) in enumerate(quick_questions):
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(f"{icon} {question}", key=f"q_{i}", use_container_width=True):
                st.session_state.chat_messages.append({"role": "user", "content": question})
                
                # Responses for quick questions
                responses = {
                    "What's a good beginner workout?": "Start with full-body workouts 3 times per week. Focus on bodyweight exercises like squats, push-ups, planks, and lunges.",
                    "How much protein do I need?": "Aim for 1.6-2.2g of protein per kg of body weight daily if you're active. For a 70kg person, that's 112-154g per day.",
                    "Best exercises for weight loss?": "Combine cardio (running, cycling) with strength training. HIIT workouts are especially effective for burning calories.",
                    "How to stay motivated?": "Set specific goals, track your progress, find a workout buddy, and celebrate small victories along the way!"
                }
                
                response = responses.get(question, "I can help with that! Could you provide more details?")
                st.session_state.chat_messages.append({"role": "assistant", "content": response})
                st.rerun()

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #666666;'>© 2026 FitAi - Virtual Coach v1.0 created by Shamila</div>", unsafe_allow_html=True)