# pages/workout.py
import streamlit as st
from datetime import datetime
import random

st.set_page_config(page_title="Start Workout", page_icon="🏃")

st.title("🏃 Start Workout")

# Quick workout templates
templates = {
    "Quick Cardio": {
        "duration": 15,
        "exercises": [
            {"name": "Jumping Jacks", "duration": 60, "rest": 30},
            {"name": "High Knees", "duration": 45, "rest": 30},
            {"name": "Mountain Climbers", "duration": 45, "rest": 30},
            {"name": "Burpees", "duration": 60, "rest": 30}
        ]
    },
    "Full Body": {
        "duration": 30,
        "exercises": [
            {"name": "Squats", "duration": 45, "rest": 30},
            {"name": "Push-ups", "duration": 45, "rest": 30},
            {"name": "Plank", "duration": 60, "rest": 30},
            {"name": "Lunges", "duration": 45, "rest": 30}
        ]
    },
    "Stretch & Mobility": {
        "duration": 20,
        "exercises": [
            {"name": "Neck Stretches", "duration": 60, "rest": 15},
            {"name": "Shoulder Rolls", "duration": 45, "rest": 15},
            {"name": "Hamstring Stretch", "duration": 60, "rest": 15},
            {"name": "Quad Stretch", "duration": 45, "rest": 15}
        ]
    }
}

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Quick Start")
    
    selected_template = st.selectbox(
        "Choose a workout template",
        list(templates.keys())
    )
    
    if selected_template:
        template = templates[selected_template]
        st.write(f"**Duration:** {template['duration']} minutes")
        st.write("**Exercises:**")
        for exercise in template["exercises"]:
            st.write(f"- {exercise['name']}: {exercise['duration']}s work, {exercise['rest']}s rest")
    
    if st.button("Start This Workout", type="primary", use_container_width=True):
        # Calculate calories (rough estimate)
        calories = template["duration"] * 8
        
        workout_data = {
            "date": str(datetime.now().date()),
            "type": selected_template.split()[0],
            "name": selected_template,
            "duration": template["duration"],
            "calories": calories,
            "exercises": template["exercises"]
        }
        
        if "workout_history" not in st.session_state:
            st.session_state.workout_history = []
        
        st.session_state.workout_history.append(workout_data)
        st.success(f"Started {selected_template}! Good luck! 🎯")
        
        # Show workout timer
        st.session_state.workout_active = True
        st.session_state.workout_start = datetime.now()

with col2:
    st.subheader("Custom Workout")
    
    workout_name = st.text_input("Workout Name")
    duration = st.number_input("Duration (min)", min_value=5, max_value=180, value=30)
    
    if st.button("Create Custom", use_container_width=True):
        calories = duration * 7  # Rough estimate
        
        workout_data = {
            "date": str(datetime.now().date()),
            "type": "Custom",
            "name": workout_name or "Custom Workout",
            "duration": duration,
            "calories": calories
        }
        
        if "workout_history" not in st.session_state:
            st.session_state.workout_history = []
        
        st.session_state.workout_history.append(workout_data)
        st.success("Custom workout logged! 💪")

# Back button
if st.button("← Back to Dashboard"):
    st.switch_page("app.py")