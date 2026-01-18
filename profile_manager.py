import streamlit as st
import pandas as pd
from datetime import datetime
import random  # Add this line

class ProfileManager:
    def __init__(self):
        self.initialize_profile_data()
    
    def initialize_profile_data(self):
        """Initialize default profile data"""
        defaults = {
            'personal': {
                'name': '',
                'age': 25,
                'gender': 'Male',
                'height': 170,
                'weight': 70,
                'birth_date': '1995-01-01'
            },
            'fitness': {
                'fitness_level': 'Beginner',
                'experience_years': 0,
                'workout_days_per_week': 3,
                'workout_duration': 45,
                'preferred_time': 'Morning'
            },
            'goals': {
                'primary_goal': 'weight_loss',
                'secondary_goals': ['muscle_gain', 'endurance'],
                'target_weight': 65,
                'timeline': '3_months',
                'motivation_level': 'High'
            },
            'health': {
                'medical_conditions': [],
                'allergies': [],
                'medications': [],
                'injuries': [],
                'sleep_hours': 7,
                'stress_level': 'Medium'
            },
            'nutrition': {
                'diet_type': 'Balanced',
                'food_preferences': [],
                'food_allergies': [],
                'meals_per_day': 3,
                'water_target': 8,
                'alcohol_intake': 'None',
                'smoking': 'No'
            },
            'lifestyle': {
                'occupation': 'Sedentary',
                'activity_level': 'Moderate',
                'sleep_schedule': 'Regular',
                'stress_management': 'Exercise',
                'hobbies': []
            }
        }
        
        if 'profile_data' not in st.session_state:
            st.session_state.profile_data = defaults
    
    def render(self):
        """Render profile management interface"""
        st.markdown('<h1 class="main-header">👤 PERSONAL PROFILE SETUP</h1>', unsafe_allow_html=True)
        
        tabs = st.tabs(["Personal Info", "Fitness Goals", "Health Details", "Nutrition", "Lifestyle"])
        
        with tabs[0]:
            self.render_personal_info()
        
        with tabs[1]:
            self.render_fitness_goals()
        
        with tabs[2]:
            self.render_health_details()
        
        with tabs[3]:
            self.render_nutrition_info()
        
        with tabs[4]:
            self.render_lifestyle_info()
        
        # Save button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💾 SAVE PROFILE", use_container_width=True, type="primary"):
                self.save_profile()
                st.success("✅ Profile saved successfully!")
                st.balloons()
    
    def render_personal_info(self):
        """Render personal information form"""
        st.markdown('<div class="section-header">📝 PERSONAL INFORMATION</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.profile_data['personal']['name'] = st.text_input(
                "Full Name",
                value=st.session_state.profile_data['personal']['name'],
                placeholder="Enter your full name"
            )
            
            st.session_state.profile_data['personal']['age'] = st.number_input(
                "Age",
                min_value=10,
                max_value=100,
                value=st.session_state.profile_data['personal']['age']
            )
            
            st.session_state.profile_data['personal']['gender'] = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=["Male", "Female", "Other"].index(
                    st.session_state.profile_data['personal']['gender']
                ) if st.session_state.profile_data['personal']['gender'] in ["Male", "Female", "Other"] else 0
            )
        
        with col2:
            st.session_state.profile_data['personal']['height'] = st.number_input(
                "Height (cm)",
                min_value=100,
                max_value=250,
                value=st.session_state.profile_data['personal']['height']
            )
            
            st.session_state.profile_data['personal']['weight'] = st.number_input(
                "Weight (kg)",
                min_value=30.0,
                max_value=200.0,
                value=float(st.session_state.profile_data['personal']['weight']),
                step=0.5
            )
            
            birth_date = st.date_input(
                "Date of Birth",
                value=datetime.strptime(st.session_state.profile_data['personal']['birth_date'], '%Y-%m-%d'),
                max_value=datetime.now()
            )
            st.session_state.profile_data['personal']['birth_date'] = birth_date.strftime('%Y-%m-%d')
    
    def render_fitness_goals(self):
        """Render fitness goals form"""
        st.markdown('<div class="section-header">🎯 FITNESS GOALS & LEVEL</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.profile_data['fitness']['fitness_level'] = st.selectbox(
                "Current Fitness Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=["Beginner", "Intermediate", "Advanced"].index(
                    st.session_state.profile_data['fitness']['fitness_level']
                )
            )
            
            st.session_state.profile_data['fitness']['experience_years'] = st.slider(
                "Years of Exercise Experience",
                0, 20, st.session_state.profile_data['fitness']['experience_years']
            )
            
            st.session_state.profile_data['fitness']['workout_days_per_week'] = st.slider(
                "Preferred Workout Days/Week",
                1, 7, st.session_state.profile_data['fitness']['workout_days_per_week']
            )
        
        with col2:
            st.session_state.profile_data['goals']['primary_goal'] = st.selectbox(
                "Primary Goal",
                ["weight_loss", "muscle_gain", "endurance", "flexibility", "general_fitness", "sports_specific"],
                format_func=lambda x: x.replace("_", " ").title(),
                index=["weight_loss", "muscle_gain", "endurance", "flexibility", "general_fitness", "sports_specific"].index(
                    st.session_state.profile_data['goals']['primary_goal']
                ) if st.session_state.profile_data['goals']['primary_goal'] in ["weight_loss", "muscle_gain", "endurance", "flexibility", "general_fitness", "sports_specific"] else 0
            )
            
            st.session_state.profile_data['goals']['secondary_goals'] = st.multiselect(
                "Secondary Goals",
                ["weight_loss", "muscle_gain", "endurance", "flexibility", "strength", "recovery", "mental_health"],
                format_func=lambda x: x.replace("_", " ").title(),
                default=st.session_state.profile_data['goals']['secondary_goals']
            )
            
            st.session_state.profile_data['goals']['target_weight'] = st.number_input(
                "Target Weight (kg)",
                min_value=30.0,
                max_value=200.0,
                value=float(st.session_state.profile_data['goals']['target_weight']),
                step=0.5
            )
            
            st.session_state.profile_data['goals']['timeline'] = st.select_slider(
                "Goal Timeline",
                ["1_month", "3_months", "6_months", "1_year"],
                value=st.session_state.profile_data['goals']['timeline'],
                format_func=lambda x: x.replace("_", " ").title()
            )
    
    def render_health_details(self):
        """Render health details form"""
        st.markdown('<div class="section-header">❤️ HEALTH INFORMATION</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.profile_data['health']['medical_conditions'] = st.multiselect(
                "Medical Conditions",
                ["Diabetes", "Hypertension", "Heart Disease", "Asthma", "Arthritis", "None"],
                default=st.session_state.profile_data['health']['medical_conditions']
            )
            
            st.session_state.profile_data['health']['allergies'] = st.multiselect(
                "Allergies",
                ["Peanuts", "Dairy", "Gluten", "Shellfish", "Eggs", "None"],
                default=st.session_state.profile_data['health']['allergies']
            )
            
            st.session_state.profile_data['health']['injuries'] = st.text_area(
                "Previous Injuries",
                value=", ".join(st.session_state.profile_data['health']['injuries']) 
                if st.session_state.profile_data['health']['injuries'] else "",
                placeholder="List any previous injuries (comma separated)"
            )
        
        with col2:
            st.session_state.profile_data['health']['sleep_hours'] = st.slider(
                "Average Sleep Hours/Night",
                3.0, 12.0, float(st.session_state.profile_data['health']['sleep_hours']), 0.5
            )
            
            st.session_state.profile_data['health']['stress_level'] = st.select_slider(
                "Average Stress Level",
                ["Low", "Medium", "High"],
                value=st.session_state.profile_data['health']['stress_level']
            )
            
            medications = st.text_area(
                "Current Medications",
                value=", ".join(st.session_state.profile_data['health']['medications'])
                if st.session_state.profile_data['health']['medications'] else "",
                placeholder="List any medications (comma separated)"
            )
            if medications:
                st.session_state.profile_data['health']['medications'] = [m.strip() for m in medications.split(",")]
    
    def render_nutrition_info(self):
        """Render nutrition information form"""
        st.markdown('<div class="section-header">🍎 NUTRITION PREFERENCES</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.profile_data['nutrition']['diet_type'] = st.selectbox(
                "Diet Type",
                ["Balanced", "Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean", "Low Carb", "High Protein"],
                index=["Balanced", "Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean", "Low Carb", "High Protein"].index(
                    st.session_state.profile_data['nutrition']['diet_type']
                ) if st.session_state.profile_data['nutrition']['diet_type'] in ["Balanced", "Vegetarian", "Vegan", "Keto", "Paleo", "Mediterranean", "Low Carb", "High Protein"] else 0
            )
            
            st.session_state.profile_data['nutrition']['food_preferences'] = st.multiselect(
                "Food Preferences",
                ["Spicy", "Sweet", "Salty", "Bitter", "Sour", "Umami"],
                default=st.session_state.profile_data['nutrition']['food_preferences']
            )
            
            st.session_state.profile_data['nutrition']['food_allergies'] = st.multiselect(
                "Food Allergies",
                ["Nuts", "Dairy", "Gluten", "Shellfish", "Eggs", "Soy", "None"],
                default=st.session_state.profile_data['nutrition']['food_allergies']
            )
        
        with col2:
            st.session_state.profile_data['nutrition']['meals_per_day'] = st.slider(
                "Meals per Day",
                1, 6, st.session_state.profile_data['nutrition']['meals_per_day']
            )
            
            st.session_state.profile_data['nutrition']['water_target'] = st.slider(
                "Daily Water Target (glasses)",
                4, 16, st.session_state.profile_data['nutrition']['water_target']
            )
            
            st.session_state.profile_data['nutrition']['alcohol_intake'] = st.selectbox(
                "Alcohol Intake",
                ["None", "Occasional", "Weekly", "Daily"],
                index=["None", "Occasional", "Weekly", "Daily"].index(
                    st.session_state.profile_data['nutrition']['alcohol_intake']
                )
            )
            
            st.session_state.profile_data['nutrition']['smoking'] = st.selectbox(
                "Smoking",
                ["No", "Occasional", "Regular"],
                index=["No", "Occasional", "Regular"].index(
                    st.session_state.profile_data['nutrition']['smoking']
                )
            )
    
    def render_lifestyle_info(self):
        """Render lifestyle information form"""
        st.markdown('<div class="section-header">🏡 LIFESTYLE INFORMATION</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.profile_data['lifestyle']['occupation'] = st.selectbox(
                "Occupation Type",
                ["Sedentary", "Light Active", "Moderate Active", "Very Active"],
                index=["Sedentary", "Light Active", "Moderate Active", "Very Active"].index(
                    st.session_state.profile_data['lifestyle']['occupation']
                ) if st.session_state.profile_data['lifestyle']['occupation'] in ["Sedentary", "Light Active", "Moderate Active", "Very Active"] else 0
            )
            
            st.session_state.profile_data['lifestyle']['activity_level'] = st.select_slider(
                "Overall Activity Level",
                ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                value=st.session_state.profile_data['lifestyle']['activity_level']
            )
        
        with col2:
            st.session_state.profile_data['lifestyle']['sleep_schedule'] = st.selectbox(
                "Sleep Schedule",
                ["Regular", "Irregular", "Night Shift", "Early Bird", "Night Owl"],
                index=["Regular", "Irregular", "Night Shift", "Early Bird", "Night Owl"].index(
                    st.session_state.profile_data['lifestyle']['sleep_schedule']
                ) if st.session_state.profile_data['lifestyle']['sleep_schedule'] in ["Regular", "Irregular", "Night Shift", "Early Bird", "Night Owl"] else 0
            )
            
            st.session_state.profile_data['lifestyle']['stress_management'] = st.multiselect(
                "Stress Management Techniques",
                ["Exercise", "Meditation", "Reading", "Socializing", "Hobbies", "Therapy", "Other"],
                default=st.session_state.profile_data['lifestyle']['stress_management']
            )
            
            hobbies = st.text_area(
                "Hobbies & Interests",
                value=", ".join(st.session_state.profile_data['lifestyle']['hobbies'])
                if st.session_state.profile_data['lifestyle']['hobbies'] else "",
                placeholder="List your hobbies (comma separated)"
            )
            if hobbies:
                st.session_state.profile_data['lifestyle']['hobbies'] = [h.strip() for h in hobbies.split(",")]
    
    def save_profile(self):
        """Save profile data to session state"""
        # Calculate BMI and store
        height_m = st.session_state.profile_data['personal']['height'] / 100
        weight = st.session_state.profile_data['personal']['weight']
        bmi = weight / (height_m ** 2) if height_m > 0 else 0
        
        st.session_state.profile_data['metrics'] = {
            'bmi': round(bmi, 1),
            'bmi_category': self.get_bmi_category(bmi),
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Initialize other session states if not exists
        if 'workout_history' not in st.session_state:
            st.session_state.workout_history = []
        
        if 'nutrition_logs' not in st.session_state:
            st.session_state.nutrition_logs = []
        
        if 'water_intake' not in st.session_state:
            st.session_state.water_intake = 0
        
        if 'sleep_hours' not in st.session_state:
            st.session_state.sleep_hours = st.session_state.profile_data['health']['sleep_hours']
        
        st.success("Profile saved successfully!")
    
    def get_bmi_category(self, bmi):
        """Get BMI category"""
        if bmi < 18.5:
            return "Underweight"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        else:
            return "Obese"