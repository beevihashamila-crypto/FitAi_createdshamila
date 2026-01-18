import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

class WorkoutPlanner:
    def __init__(self):
        self.workout_templates = self.load_workout_templates()
        self.exercise_library = self.load_exercise_library()
    
    def load_workout_templates(self):
        """Load workout templates for different goals and levels"""
        return {
            'weight_loss': {
                'beginner': {
                    'name': 'Fat Burn Starter',
                    'duration': 30,
                    'exercises': [
                        {'name': 'Jumping Jacks', 'sets': 3, 'reps': 30, 'rest': 30},
                        {'name': 'Bodyweight Squats', 'sets': 3, 'reps': 15, 'rest': 45},
                        {'name': 'Push-ups (Knee)', 'sets': 3, 'reps': 10, 'rest': 45},
                        {'name': 'Plank', 'sets': 3, 'duration': 30, 'rest': 30}
                    ],
                    'calories': 250
                },
                'intermediate': {
                    'name': 'HIIT Blaster',
                    'duration': 40,
                    'exercises': [
                        {'name': 'Burpees', 'sets': 4, 'reps': 12, 'rest': 45},
                        {'name': 'Mountain Climbers', 'sets': 4, 'reps': 30, 'rest': 30},
                        {'name': 'Jump Squats', 'sets': 4, 'reps': 15, 'rest': 45},
                        {'name': 'Plank Jacks', 'sets': 4, 'reps': 20, 'rest': 30}
                    ],
                    'calories': 400
                }
            },
            'muscle_gain': {
                'beginner': {
                    'name': 'Strength Foundation',
                    'duration': 45,
                    'exercises': [
                        {'name': 'Push-ups', 'sets': 3, 'reps': 12, 'rest': 60},
                        {'name': 'Bodyweight Rows', 'sets': 3, 'reps': 10, 'rest': 60},
                        {'name': 'Goblet Squats', 'sets': 3, 'reps': 12, 'rest': 60},
                        {'name': 'Plank', 'sets': 3, 'duration': 45, 'rest': 45}
                    ],
                    'calories': 300
                },
                'intermediate': {
                    'name': 'Muscle Builder',
                    'duration': 60,
                    'exercises': [
                        {'name': 'Bench Press', 'sets': 4, 'reps': 8, 'rest': 90},
                        {'name': 'Bent Over Rows', 'sets': 4, 'reps': 10, 'rest': 90},
                        {'name': 'Barbell Squats', 'sets': 4, 'reps': 8, 'rest': 90},
                        {'name': 'Shoulder Press', 'sets': 3, 'reps': 10, 'rest': 60}
                    ],
                    'calories': 450
                }
            }
        }
    
    def load_exercise_library(self):
        """Load exercise library with details"""
        return {
            'cardio': [
                {'name': 'Running', 'calories_per_min': 10, 'muscles': ['Legs', 'Core']},
                {'name': 'Cycling', 'calories_per_min': 8, 'muscles': ['Legs', 'Glutes']},
                {'name': 'Jump Rope', 'calories_per_min': 12, 'muscles': ['Full Body']}
            ],
            'strength': [
                {'name': 'Squats', 'calories_per_min': 5, 'muscles': ['Legs', 'Glutes']},
                {'name': 'Push-ups', 'calories_per_min': 4, 'muscles': ['Chest', 'Arms']},
                {'name': 'Pull-ups', 'calories_per_min': 6, 'muscles': ['Back', 'Arms']}
            ]
        }
    
    def render(self):
        """Render workout planner interface"""
        st.markdown('<h1 class="main-header">🏋️‍♂️ AI WORKOUT PLANNER</h1>', unsafe_allow_html=True)
        
        tabs = st.tabs(["Personalized Plan", "Create Workout", "Exercise Library", "Log Workout", "History"])
        
        with tabs[0]:
            self.render_personalized_plan()
        
        with tabs[1]:
            self.render_workout_creator()
        
        with tabs[2]:
            self.render_exercise_library()
        
        with tabs[3]:
            self.render_workout_logger()
        
        with tabs[4]:
            self.render_workout_history()
    
    def render_personalized_plan(self):
        """Render personalized workout plan"""
        st.markdown('<div class="section-header">🎯 YOUR WEEKLY WORKOUT PLAN</div>', unsafe_allow_html=True)
        
        if 'profile_data' not in st.session_state:
            st.warning("Please complete your profile first!")
            return
        
        profile = st.session_state.profile_data
        goals = profile.get('goals', {})
        fitness = profile.get('fitness', {})
        
        primary_goal = goals.get('primary_goal', 'weight_loss')
        fitness_level = fitness.get('fitness_level', 'beginner').lower()
        
        # Generate weekly plan
        weekly_plan = self.generate_weekly_plan(primary_goal, fitness_level)
        
        # Display weekly calendar
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        cols = st.columns(7)
        for i, col in enumerate(cols):
            with col:
                day_plan = weekly_plan[i]
                
                if day_plan['type'] == 'rest':
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px; 
                                text-align: center; border: 1px solid rgba(255, 255, 255, 0.1);">
                        <div style="color: #666666; font-size: 0.9rem;">{days[i]}</div>
                        <div style="color: #00FF87; font-size: 2rem;">😴</div>
                        <div style="color: #999999; font-size: 0.8rem;">Rest Day</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background: rgba(0, 255, 135, 0.1); padding: 1rem; border-radius: 10px; 
                                text-align: center; border: 1px solid #00FF87;">
                        <div style="color: #CCCCCC; font-size: 0.9rem;">{days[i]}</div>
                        <div style="color: #00FF87; font-size: 1.5rem;">💪</div>
                        <div style="color: white; font-size: 0.9rem;">{day_plan['workout']}</div>
                        <div style="color: #999999; font-size: 0.8rem;">{day_plan['duration']} min</div>
                        <div style="color: #00FF87; font-size: 0.8rem;">🔥 {day_plan['calories']} cal</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Today's workout details
        st.markdown('<div class="section-header">💪 TODAY\'S WORKOUT DETAILS</div>', unsafe_allow_html=True)
        
        today_index = datetime.now().weekday()
        today_plan = weekly_plan[today_index]
        
        if today_plan['type'] != 'rest':
            # Display workout details
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background: rgba(0, 255, 135, 0.05); padding: 1.5rem; border-radius: 15px;">
                    <h3 style="color: #00FF87;">{today_plan['workout']}</h3>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin: 1rem 0;">
                        <div style="text-align: center;">
                            <div style="color: white;">⏱️</div>
                            <div style="color: #CCCCCC;">{today_plan['duration']} min</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: white;">🔥</div>
                            <div style="color: #CCCCCC;">{today_plan['calories']} cal</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: white;">🎯</div>
                            <div style="color: #CCCCCC;">{today_plan['focus']}</div>
                        </div>
                    </div>
                    <p style="color: #CCCCCC;">{today_plan['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("🏁 START WORKOUT", use_container_width=True, type="primary"):
                    self.start_workout(today_plan)
                
                if st.button("📝 LOG COMPLETED", use_container_width=True):
                    self.log_workout_completion(today_plan)
                    st.success("✅ Workout logged! Keep up the great work!")
            
            # Exercises
            st.markdown("**📋 EXERCISES**")
            
            for i, exercise in enumerate(today_plan['exercises']):
                with st.expander(f"{i+1}. {exercise['name']}", expanded=True):
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.markdown(f"""
                        <div style="color: white;">
                            <strong>Muscles:</strong> {', '.join(exercise.get('muscles', ['Full Body']))}
                        </div>
                        <div style="color: #CCCCCC;">
                            <strong>Instructions:</strong> {exercise.get('instructions', 'Perform with proper form')}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        if 'sets' in exercise:
                            st.markdown(f"""
                            <div style="background: rgba(0, 255, 135, 0.1); padding: 0.5rem; border-radius: 8px; text-align: center;">
                                <div style="color: #00FF87;">Sets</div>
                                <div style="color: white; font-size: 1.2rem;">{exercise['sets']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    with col3:
                        if 'reps' in exercise:
                            st.markdown(f"""
                            <div style="background: rgba(0, 255, 135, 0.1); padding: 0.5rem; border-radius: 8px; text-align: center;">
                                <div style="color: #00FF87;">Reps</div>
                                <div style="color: white; font-size: 1.2rem;">{exercise['reps']}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        elif 'duration' in exercise:
                            st.markdown(f"""
                            <div style="background: rgba(0, 255, 135, 0.1); padding: 0.5rem; border-radius: 8px; text-align: center;">
                                <div style="color: #00FF87;">Seconds</div>
                                <div style="color: white; font-size: 1.2rem;">{exercise['duration']}</div>
                            </div>
                            """, unsafe_allow_html=True)
        
        else:
            st.info("🏖️ Today is a rest day! Focus on recovery and nutrition.")
    
    def generate_weekly_plan(self, goal, level):
        """Generate personalized weekly workout plan"""
        # Sample weekly plan
        plans = {
            'weight_loss': [
                {'type': 'workout', 'workout': 'HIIT Cardio', 'duration': 30, 'calories': 350, 
                 'focus': 'Fat Burning', 'description': 'High intensity interval training for maximum calorie burn',
                 'exercises': [
                     {'name': 'Burpees', 'sets': 4, 'reps': 12, 'muscles': ['Full Body'], 
                      'instructions': 'Start standing, drop to push-up position, jump back up'},
                     {'name': 'Mountain Climbers', 'sets': 4, 'reps': 30, 'muscles': ['Core', 'Shoulders'],
                      'instructions': 'Alternate bringing knees to chest rapidly'},
                     {'name': 'Jump Squats', 'sets': 4, 'reps': 15, 'muscles': ['Legs', 'Glutes'],
                      'instructions': 'Squat down then explode upward into a jump'}
                 ]},
                {'type': 'workout', 'workout': 'Strength Circuit', 'duration': 40, 'calories': 300,
                 'focus': 'Full Body', 'description': 'Circuit training combining strength exercises',
                 'exercises': [
                     {'name': 'Push-ups', 'sets': 3, 'reps': 15, 'muscles': ['Chest', 'Arms']},
                     {'name': 'Bodyweight Squats', 'sets': 3, 'reps': 20, 'muscles': ['Legs', 'Glutes']},
                     {'name': 'Plank', 'sets': 3, 'duration': 45, 'muscles': ['Core']}
                 ]},
                {'type': 'rest', 'workout': 'Rest', 'duration': 0, 'calories': 0, 'focus': 'Recovery'},
                {'type': 'workout', 'workout': 'Cardio Blast', 'duration': 35, 'calories': 400,
                 'focus': 'Endurance', 'description': 'Steady state cardio workout'},
                {'type': 'workout', 'workout': 'Core Focus', 'duration': 25, 'calories': 200,
                 'focus': 'Abs & Core', 'description': 'Targeted core strengthening'},
                {'type': 'rest', 'workout': 'Rest', 'duration': 0, 'calories': 0, 'focus': 'Recovery'},
                {'type': 'active', 'workout': 'Active Recovery', 'duration': 20, 'calories': 150,
                 'focus': 'Mobility', 'description': 'Light activity and stretching'}
            ]
        }
        
        return plans.get(goal, plans['weight_loss'])
    
    def start_workout(self, workout_plan):
        """Start workout timer and tracking"""
        st.session_state.workout_active = True
        st.session_state.workout_start_time = datetime.now()
        st.session_state.current_workout = workout_plan
        
        st.success(f"🚀 Starting {workout_plan['workout']}! Good luck!")
    
    def log_workout_completion(self, workout_plan):
        """Log completed workout"""
        if 'workout_history' not in st.session_state:
            st.session_state.workout_history = []
        
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().strftime('%H:%M'),
            'workout': workout_plan['workout'],
            'duration': workout_plan['duration'],
            'calories': workout_plan['calories'],
            'type': workout_plan['focus'],
            'completed': True
        }
        
        st.session_state.workout_history.append(log_entry)
        
        # Update streak and energy
        st.session_state.last_workout_date = datetime.now().strftime('%Y-%m-%d')
        st.session_state.streak_days += 1
        st.session_state.energy_level = min(100, st.session_state.energy_level + 20)
    
    def render_workout_creator(self):
        """Render custom workout creator"""
        st.markdown('<div class="section-header">🏗️ CREATE CUSTOM WORKOUT</div>', unsafe_allow_html=True)
        
        with st.form("custom_workout_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                workout_name = st.text_input("Workout Name", placeholder="e.g., Morning Strength")
                workout_type = st.selectbox("Workout Type", ["Strength", "Cardio", "HIIT", "Yoga", "Recovery"])
                duration = st.slider("Duration (minutes)", 10, 120, 45)
            
            with col2:
                intensity = st.select_slider("Intensity", ["Light", "Moderate", "Hard", "Very Hard"])
                estimated_calories = duration * {
                    "Light": 4, "Moderate": 6, "Hard": 8, "Very Hard": 10
                }[intensity]
                
                st.metric("Estimated Calories", f"{estimated_calories}")
            
            # Exercise selector
            st.markdown("**➕ ADD EXERCISES**")
            
            exercises = []
            for i in range(4):  # Allow up to 4 exercises
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    exercise_name = st.text_input(f"Exercise {i+1}", 
                                                 placeholder="e.g., Push-ups, Squats",
                                                 key=f"ex_name_{i}")
                
                with col2:
                    sets = st.number_input(f"Sets", min_value=1, max_value=10, value=3, 
                                          key=f"ex_sets_{i}")
                
                with col3:
                    reps = st.number_input(f"Reps", min_value=1, max_value=100, value=12,
                                          key=f"ex_reps_{i}")
                
                if exercise_name:
                    exercises.append({
                        'name': exercise_name,
                        'sets': sets,
                        'reps': reps
                    })
            
            notes = st.text_area("Workout Notes", placeholder="Any specific instructions or goals...")
            
            submitted = st.form_submit_button("💾 SAVE WORKOUT")
            
            if submitted:
                custom_workout = {
                    'name': workout_name,
                    'type': workout_type,
                    'duration': duration,
                    'calories': estimated_calories,
                    'intensity': intensity,
                    'exercises': exercises,
                    'notes': notes,
                    'custom': True
                }
                
                # Save to session state
                if 'custom_workouts' not in st.session_state:
                    st.session_state.custom_workouts = []
                
                st.session_state.custom_workouts.append(custom_workout)
                st.success("✅ Custom workout saved!")
    
    def render_exercise_library(self):
        """Render exercise library browser"""
        st.markdown('<div class="section-header">📚 EXERCISE LIBRARY</div>', unsafe_allow_html=True)
        
        category = st.selectbox("Select Category", ["All", "Cardio", "Strength", "Flexibility", "Core"])
        
        # Display exercises
        for cat, exercises in self.exercise_library.items():
            if category == "All" or category.lower() == cat:
                st.markdown(f"**{cat.upper()} EXERCISES**")
                
                for exercise in exercises:
                    with st.expander(exercise['name']):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"""
                            <div style="color: white;">
                                <strong>Muscles Worked:</strong> {', '.join(exercise['muscles'])}
                            </div>
                            <div style="color: #CCCCCC;">
                                <strong>Calories:</strong> {exercise['calories_per_min']} per minute
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col2:
                            if st.button("Add to Workout", key=f"add_{exercise['name']}"):
                                st.info(f"Added {exercise['name']} to your workout")
    
    def render_workout_logger(self):
        """Render manual workout logger"""
        st.markdown('<div class="section-header">📝 LOG WORKOUT</div>', unsafe_allow_html=True)
        
        with st.form("manual_workout_log"):
            col1, col2 = st.columns(2)
            
            with col1:
                workout_name = st.text_input("Workout Name")
                workout_date = st.date_input("Date", datetime.now())
                duration = st.number_input("Duration (min)", min_value=1, max_value=300, value=45)
            
            with col2:
                calories = st.number_input("Calories Burned", min_value=0, max_value=2000, value=300)
                intensity = st.select_slider("Intensity", ["Light", "Moderate", "Hard", "Very Hard"])
                rating = st.slider("How did it feel?", 1, 10, 7)
            
            notes = st.text_area("Notes", placeholder="How did it go? Any achievements?")
            
            submitted = st.form_submit_button("💾 LOG WORKOUT")
            
            if submitted:
                self.log_manual_workout({
                    'name': workout_name,
                    'date': workout_date.strftime('%Y-%m-%d'),
                    'duration': duration,
                    'calories': calories,
                    'intensity': intensity,
                    'rating': rating,
                    'notes': notes
                })
                st.success("✅ Workout logged successfully!")
    
    def log_manual_workout(self, workout_data):
        """Log manual workout"""
        if 'workout_history' not in st.session_state:
            st.session_state.workout_history = []
        
        log_entry = {
            'date': workout_data['date'],
            'timestamp': datetime.now().strftime('%H:%M'),
            'workout': workout_data['name'],
            'duration': workout_data['duration'],
            'calories': workout_data['calories'],
            'intensity': workout_data['intensity'],
            'rating': workout_data['rating'],
            'notes': workout_data['notes'],
            'completed': True
        }
        
        st.session_state.workout_history.append(log_entry)
        
        # Update streak
        if workout_data['date'] == datetime.now().strftime('%Y-%m-%d'):
            st.session_state.last_workout_date = workout_data['date']
            st.session_state.streak_days += 1
            st.session_state.energy_level = min(100, st.session_state.energy_level + 15)
    
    def render_workout_history(self):
        """Render workout history"""
        st.markdown('<div class="section-header">📊 WORKOUT HISTORY</div>', unsafe_allow_html=True)
        
        if 'workout_history' not in st.session_state or not st.session_state.workout_history:
            st.info("No workouts logged yet. Start your first workout!")
            return
        
        # Filter by time period
        period = st.selectbox("View Period", ["Last 7 days", "Last 30 days", "All time"])
        
        # Calculate stats
        workouts = st.session_state.workout_history
        
        total_workouts = len(workouts)
        total_calories = sum(w.get('calories', 0) for w in workouts)
        total_duration = sum(w.get('duration', 0) for w in workouts)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Workouts", total_workouts)
        with col2:
            st.metric("Calories Burned", f"{total_calories:,}")
        with col3:
            st.metric("Total Duration", f"{total_duration:,} min")
        
        # Display recent workouts
        st.markdown("**📋 RECENT WORKOUTS**")
        
        for workout in workouts[-5:][::-1]:  # Last 5 workouts, newest first
            with st.container():
                st.markdown(f"""
                <div style="background: rgba(0, 255, 135, 0.05); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #00FF87; font-weight: 600;">{workout['workout']}</div>
                            <div style="color: #CCCCCC; font-size: 0.9rem;">
                                {workout['date']} | ⏱️ {workout['duration']}min | 🔥 {workout['calories']}cal
                            </div>
                        </div>
                        <div style="color: #00FF87;">✅</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)