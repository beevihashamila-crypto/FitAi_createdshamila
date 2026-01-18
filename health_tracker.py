import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import random

class HealthTracker:
    def __init__(self):
        self.initialize_health_data()
    
    def initialize_health_data(self):
        """Initialize health tracking data"""
        defaults = {
            'water_history': [],
            'sleep_history': [],
            'mood_history': [],
            'stress_history': [],
            'heart_rate_data': [],
            'blood_pressure_data': []
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def render(self):
        """Render health tracker interface"""
        st.markdown('<h1 class="main-header">❤️ HEALTH TRACKER</h1>', unsafe_allow_html=True)
        
        tabs = st.tabs(["Water Tracker", "Sleep Monitor", "Mood Check", "Stress Management", "Vitals"])
        
        with tabs[0]:
            self.render_water_tracker()
        
        with tabs[1]:
            self.render_sleep_monitor()
        
        with tabs[2]:
            self.render_mood_checker()
        
        with tabs[3]:
            self.render_stress_management()
        
        with tabs[4]:
            self.render_vitals_tracker()
    
    def render_water_tracker(self):
        """Render water intake tracker"""
        st.markdown('<div class="section-header">💧 WATER INTAKE TRACKER</div>', unsafe_allow_html=True)
        
        # Current water intake
        current = st.session_state.water_intake
        target = st.session_state.profile_data['nutrition']['water_target'] if 'profile_data' in st.session_state else 8
        
        # Progress visualization
        percent = min((current / target) * 100, 100)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Water glass visualization
            st.markdown(f"""
            <div style="text-align: center; margin: 2rem 0;">
                <div style="position: relative; width: 200px; height: 300px; margin: 0 auto;">
                    <!-- Water bottle outline -->
                    <div style="position: absolute; width: 100px; height: 300px; left: 50px; 
                                border: 3px solid #00FF87; border-radius: 50px 50px 10px 10px; 
                                background: rgba(255, 255, 255, 0.1); overflow: hidden;">
                        <!-- Water level -->
                        <div style="position: absolute; bottom: 0; width: 100%; 
                                    height: {percent}%; background: linear-gradient(to top, #00D4FF, #00FF87); 
                                    transition: height 1s ease-in-out;"></div>
                    </div>
                    <!-- Measurement markers -->
                    <div style="position: absolute; right: 60px; top: 20px; color: #00FF87;">{target}</div>
                    <div style="position: absolute; right: 60px; top: 50%; color: #00FF87;">{target//2}</div>
                    <div style="position: absolute; right: 60px; bottom: 20px; color: #00FF87;">0</div>
                </div>
                <div style="color: #00FF87; font-size: 1.5rem; margin-top: 1rem;">
                    {current} / {target} glasses
                </div>
                <div style="color: #CCCCCC;">
                    {percent:.0f}% of daily goal
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="stats-card">
                <h4 style="color: #00FF87;">💦 QUICK LOG</h4>
                <div style="text-align: center; margin: 1rem 0;">
                    <div style="font-size: 3rem; color: #00D4FF;">💧</div>
                </div>
                <p style="color: #CCCCCC; text-align: center;">
                    Log your water intake quickly
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Quick log buttons
            glass_sizes = [1, 2, 0.5]
            
            for size in glass_sizes:
                label = f"+{size} glass{'es' if size > 1 else ''}"
                if st.button(label, use_container_width=True, key=f"water_{size}"):
                    st.session_state.water_intake = min(target, current + size)
                    
                    # Add to history
                    water_log = {
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'time': datetime.now().strftime('%H:%M'),
                        'amount': size,
                        'total': st.session_state.water_intake
                    }
                    
                    st.session_state.water_history.append(water_log)
                    st.rerun()
            
            if st.button("Reset Today", use_container_width=True, type="secondary"):
                st.session_state.water_intake = 0
                st.rerun()
        
        # History
        st.markdown("**📊 WEEKLY HISTORY**")
        
        if st.session_state.water_history:
            # Create weekly summary
            weekly_data = []
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                day_logs = [log for log in st.session_state.water_history 
                           if log.get('date') == date]
                total = sum(log.get('amount', 0) for log in day_logs)
                weekly_data.append({
                    'date': date,
                    'amount': total,
                    'day': (datetime.now() - timedelta(days=i)).strftime('%a')
                })
            
            weekly_data.reverse()  # Oldest to newest
            
            # Display as chart
            fig = go.Figure(data=[
                go.Bar(
                    x=[d['day'] for d in weekly_data],
                    y=[d['amount'] for d in weekly_data],
                    marker_color=['#00FF87' if d['amount'] >= target else '#666666' 
                                 for d in weekly_data],
                    text=[f"{d['amount']}/{target}" for d in weekly_data],
                    textposition='auto'
                )
            ])
            
            fig.update_layout(
                title="Water Intake (Last 7 Days)",
                xaxis_title="Day",
                yaxis_title="Glasses",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def render_sleep_monitor(self):
        """Render sleep tracking interface"""
        st.markdown('<div class="section-header">💤 SLEEP MONITOR</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Sleep log form
            with st.form("sleep_log_form"):
                st.markdown("**🛏️ LOG LAST NIGHT'S SLEEP**")
                
                hours = st.slider("Sleep Duration (hours)", 3.0, 12.0, 
                                 st.session_state.sleep_hours or 7.0, 0.5)
                
                quality = st.slider("Sleep Quality", 1, 10, 7)
                
                wake_ups = st.number_input("Times Woke Up", 0, 10, 0)
                
                notes = st.text_area("Notes", placeholder="How did you sleep?")
                
                submitted = st.form_submit_button("💾 LOG SLEEP")
                
                if submitted:
                    self.log_sleep({
                        'hours': hours,
                        'quality': quality,
                        'wake_ups': wake_ups,
                        'notes': notes
                    })
                    st.success("✅ Sleep logged successfully!")
        
        with col2:
            # Sleep recommendations
            current_sleep = st.session_state.sleep_hours or 7
            target_sleep = 8
            
            st.markdown(f"""
            <div class="stats-card">
                <h4 style="color: #00FF87;">🌙 SLEEP RECOMMENDATIONS</h4>
                <div style="margin: 1rem 0;">
                    <div style="display: flex; justify-content: space-between; color: #CCCCCC;">
                        <span>Current</span>
                        <span>{current_sleep}h</span>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); height: 10px; border-radius: 5px;">
                        <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                                   width: {min((current_sleep / target_sleep) * 100, 100)}%; 
                                   height: 100%; border-radius: 5px;"></div>
                    </div>
                    <div style="color: #999999; font-size: 0.9rem; text-align: center; margin-top: 5px;">
                        Target: {target_sleep}h
                    </div>
                </div>
                
                <div style="color: #CCCCCC; margin-top: 1rem;">
                    <strong>💡 Tips for better sleep:</strong>
                    <ul style="color: #999999; font-size: 0.9rem;">
                        <li>Stick to a consistent sleep schedule</li>
                        <li>Avoid screens 1 hour before bed</li>
                        <li>Keep bedroom cool and dark</li>
                        <li>Limit caffeine after 2 PM</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sleep history
        st.markdown("**📈 SLEEP HISTORY**")
        
        if st.session_state.sleep_history:
            # Create sleep chart
            sleep_data = st.session_state.sleep_history[-7:]  # Last 7 days
            
            dates = [s['date'] for s in sleep_data]
            hours = [s['hours'] for s in sleep_data]
            quality = [s['quality'] for s in sleep_data]
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=dates,
                y=hours,
                name='Hours',
                marker_color='#00FF87',
                text=hours,
                textposition='auto'
            ))
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=quality,
                name='Quality',
                yaxis='y2',
                line=dict(color='#00D4FF', width=3),
                mode='lines+markers'
            ))
            
            fig.update_layout(
                title="Sleep Pattern (Last 7 Days)",
                xaxis_title="Date",
                yaxis_title="Hours",
                yaxis2=dict(
                    title="Quality (1-10)",
                    overlaying='y',
                    side='right',
                    range=[0, 10]
                ),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def log_sleep(self, sleep_data):
        """Log sleep data"""
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().strftime('%H:%M'),
            **sleep_data
        }
        
        st.session_state.sleep_history.append(log_entry)
        st.session_state.sleep_hours = sleep_data['hours']
    
    def render_mood_checker(self):
        """Render mood tracking interface"""
        st.markdown('<div class="section-header">😊 MOOD CHECKER</div>', unsafe_allow_html=True)
        
        # Current mood
        current_mood = st.session_state.current_mood
        
        mood_emojis = {
            'happy': '😊',
            'neutral': '😐',
            'sad': '😔',
            'angry': '😤',
            'energized': '🔥',
            'tired': '😴'
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem;">
                <div style="font-size: 5rem;">
                    {mood_emojis.get(current_mood, '😊')}
                </div>
                <div style="color: #00FF87; font-size: 1.5rem; margin-top: 1rem;">
                    {current_mood.upper()}
                </div>
                <div style="color: #CCCCCC;">
                    Current Mood
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Mood log
            with st.form("mood_log_form"):
                new_mood = st.selectbox(
                    "Update Mood",
                    list(mood_emojis.keys()),
                    format_func=lambda x: f"{mood_emojis[x]} {x.title()}",
                    index=list(mood_emojis.keys()).index(current_mood) 
                    if current_mood in mood_emojis else 0
                )
                
                mood_reason = st.text_area("Why do you feel this way?", 
                                          placeholder="Optional: Describe what's affecting your mood...")
                
                submitted = st.form_submit_button("💾 LOG MOOD")
                
                if submitted:
                    self.log_mood(new_mood, mood_reason)
                    st.success("✅ Mood logged!")
        
        with col2:
            # Mood recommendations based on current mood
            recommendations = self.get_mood_recommendations(current_mood)
            
            st.markdown(f"""
            <div class="stats-card">
                <h4 style="color: #00FF87;">💡 MOOD RECOMMENDATIONS</h4>
                <div style="color: #CCCCCC; margin-top: 1rem;">
                    {recommendations['main']}
                </div>
                <ul style="color: #999999; margin-top: 1rem;">
                    {''.join([f'<li>{rec}</li>' for rec in recommendations['tips']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Show joke button for sad mood
            if current_mood == 'sad':
                if st.button("😄 Need a laugh?", use_container_width=True):
                    joke = self.get_mood_joke()
                    st.info(f"**Joke of the day:** {joke}")
        
        # Mood history
        st.markdown("**📊 MOOD HISTORY**")
        
        if st.session_state.mood_history:
            mood_data = st.session_state.mood_history[-7:]  # Last 7 days
            
            # Create mood chart
            mood_values = {
                'happy': 5,
                'energized': 4,
                'neutral': 3,
                'tired': 2,
                'sad': 1,
                'angry': 0
            }
            
            dates = [m['date'] for m in mood_data]
            moods = [mood_values.get(m['mood'], 3) for m in mood_data]
            mood_labels = [m['mood'].title() for m in mood_data]
            
            fig = go.Figure(data=[
                go.Scatter(
                    x=dates,
                    y=moods,
                    mode='lines+markers',
                    line=dict(color='#00FF87', width=3),
                    marker=dict(size=10, color='#00D4FF'),
                    text=mood_labels,
                    hoverinfo='text+y'
                )
            ])
            
            fig.update_layout(
                title="Mood Trend (Last 7 Days)",
                xaxis_title="Date",
                yaxis_title="Mood Level",
                yaxis=dict(tickvals=[0, 1, 2, 3, 4, 5],
                          ticktext=['Angry', 'Sad', 'Tired', 'Neutral', 'Energized', 'Happy'],
                          range=[0, 5],
                          gridcolor='rgba(255,255,255,0.1)'),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def get_mood_recommendations(self, mood):
        """Get recommendations based on mood"""
        recommendations = {
            'happy': {
                'main': 'Great! Keep up the positive energy!',
                'tips': [
                    'Share your positivity with others',
                    'Try a challenging workout',
                    'Set new fitness goals'
                ]
            },
            'sad': {
                'main': 'It\'s okay to feel sad sometimes. Let\'s boost your mood!',
                'tips': [
                    'Go for a light walk outside',
                    'Listen to uplifting music',
                    'Call a friend or family member',
                    'Try some gentle stretching'
                ]
            },
            'tired': {
                'main': 'Listen to your body and give it the rest it needs.',
                'tips': [
                    'Take a 20-minute power nap',
                    'Stay hydrated throughout the day',
                    'Try light yoga or stretching',
                    'Go to bed 30 minutes earlier tonight'
                ]
            },
            'energized': {
                'main': 'Perfect time for an intense workout!',
                'tips': [
                    'Try a new high-intensity workout',
                    'Challenge yourself with heavier weights',
                    'Go for a run or bike ride',
                    'Learn a new exercise technique'
                ]
            }
        }
        
        return recommendations.get(mood, {
            'main': 'Stay balanced and consistent!',
            'tips': ['Drink plenty of water', 'Get enough sleep', 'Eat balanced meals']
        })
    
    def get_mood_joke(self):
        """Get a joke to improve mood"""
        jokes = [
            "Why don't skeletons fight each other? They don't have the guts!",
            "I told my personal trainer I want to get abs. He told me to stop buying biscuits.",
            "Why did the tomato turn red? Because it saw the salad dressing!",
            "What's a runner's favorite subject in school? Jog-raphy!",
            "I'm on a seafood diet. I see food and I eat it!"
        ]
        
        return random.choice(jokes)
    
    def log_mood(self, mood, reason=None):
        """Log mood data"""
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().strftime('%H:%M'),
            'mood': mood,
            'reason': reason
        }
        
        st.session_state.mood_history.append(log_entry)
        st.session_state.current_mood = mood
    
    def render_stress_management(self):
        """Render stress management interface"""
        st.markdown('<div class="section-header">🧘 STRESS MANAGEMENT</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Stress level assessment
            st.markdown("**📊 ASSESS YOUR STRESS LEVEL**")
            
            stress_level = st.slider("Current Stress Level (1-10)", 1, 10, 5)
            
            stress_symptoms = st.multiselect(
                "Current Symptoms",
                ["Headache", "Fatigue", "Irritability", "Muscle tension", 
                 "Sleep problems", "Anxiety", "Poor concentration"],
                help="Select symptoms you're experiencing"
            )
            
            stress_causes = st.text_area(
                "What's causing stress?",
                placeholder="Work, relationships, health, etc..."
            )
            
            if st.button("💾 LOG STRESS LEVEL", use_container_width=True):
                self.log_stress({
                    'level': stress_level,
                    'symptoms': stress_symptoms,
                    'causes': stress_causes
                })
                st.success("✅ Stress level logged!")
        
        with col2:
            # Stress relief techniques
            st.markdown("**💆 STRESS RELIEF TECHNIQUES**")
            
            techniques = [
                {
                    'name': 'Deep Breathing',
                    'duration': '5 min',
                    'instructions': 'Inhale for 4 counts, hold for 7, exhale for 8',
                    'benefits': 'Calms nervous system'
                },
                {
                    'name': 'Progressive Muscle Relaxation',
                    'duration': '10 min',
                    'instructions': 'Tense and relax each muscle group',
                    'benefits': 'Reduces physical tension'
                },
                {
                    'name': 'Mindful Walking',
                    'duration': '15 min',
                    'instructions': 'Walk slowly while focusing on senses',
                    'benefits': 'Clears mind, reduces anxiety'
                }
            ]
            
            for tech in techniques:
                with st.expander(f"🧘 {tech['name']} - {tech['duration']}"):
                    st.markdown(f"""
                    <div style="color: #CCCCCC;">
                        <strong>Instructions:</strong> {tech['instructions']}
                    </div>
                    <div style="color: #999999; margin-top: 10px;">
                        <strong>Benefits:</strong> {tech['benefits']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"Start {tech['name']}", key=f"start_{tech['name']}"):
                        st.info(f"Starting {tech['name']} session. Find a quiet place and begin.")
    
    def log_stress(self, stress_data):
        """Log stress data"""
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().strftime('%H:%M'),
            **stress_data
        }
        
        st.session_state.stress_history.append(log_entry)
    
    def render_vitals_tracker(self):
        """Render vital signs tracker"""
        st.markdown('<div class="section-header">❤️ VITAL SIGNS TRACKER</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Heart rate tracker
            st.markdown("**❤️ HEART RATE**")
            
            with st.form("heart_rate_form"):
                heart_rate = st.number_input("Resting Heart Rate (BPM)", 
                                            min_value=40, max_value=200, value=72)
                
                measurement_time = st.selectbox(
                    "When measured",
                    ["Upon waking", "After rest", "After exercise", "Random"]
                )
                
                submitted = st.form_submit_button("💾 LOG HEART RATE")
                
                if submitted:
                    self.log_heart_rate(heart_rate, measurement_time)
                    st.success("✅ Heart rate logged!")
        
        with col2:
            # Blood pressure tracker
            st.markdown("**🩺 BLOOD PRESSURE**")
            
            with st.form("blood_pressure_form"):
                col_sys, col_dia = st.columns(2)
                
                with col_sys:
                    systolic = st.number_input("Systolic", min_value=80, max_value=200, value=120)
                
                with col_dia:
                    diastolic = st.number_input("Diastolic", min_value=40, max_value=130, value=80)
                
                submitted = st.form_submit_button("💾 LOG BLOOD PRESSURE")
                
                if submitted:
                    self.log_blood_pressure(systolic, diastolic)
                    st.success("✅ Blood pressure logged!")
        
        # Health metrics dashboard
        st.markdown("**📊 HEALTH METRICS DASHBOARD**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Heart rate gauge
            hr_data = self.get_heart_rate_data()
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = hr_data['current'],
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Heart Rate", 'font': {'color': 'white', 'size': 16}},
                gauge = {
                    'axis': {'range': [hr_data['min'], hr_data['max']], 'tickcolor': "white"},
                    'bar': {'color': "#00FF87"},
                    'steps': [
                        {'range': [hr_data['min'], 60], 'color': "#FF4444"},
                        {'range': [60, 100], 'color': "#00FF87"},
                        {'range': [100, hr_data['max']], 'color': "#FFA500"}
                    ]
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white", 'family': "Arial"},
                height=250
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sleep quality gauge
            sleep_quality = st.session_state.sleep_history[-1]['quality'] \
                if st.session_state.sleep_history else 7
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = sleep_quality,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Sleep Quality", 'font': {'color': 'white', 'size': 16}},
                gauge = {
                    'axis': {'range': [0, 10], 'tickcolor': "white"},
                    'bar': {'color': "#00D4FF"},
                    'steps': [
                        {'range': [0, 4], 'color': "#FF4444"},
                        {'range': [4, 7], 'color': "#FFA500"},
                        {'range': [7, 10], 'color': "#00FF87"}
                    ]
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white", 'family': "Arial"},
                height=250
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col3:
            # Stress level gauge
            stress_level = self.calculate_stress_level()
            
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = stress_level,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Stress Level", 'font': {'color': 'white', 'size': 16}},
                number = {'suffix': "%"},
                gauge = {
                    'axis': {'range': [0, 100], 'tickcolor': "white"},
                    'bar': {'color': "#FFA500" if stress_level < 50 else "#FF4444"},
                    'steps': [
                        {'range': [0, 30], 'color': "#00FF87"},
                        {'range': [30, 70], 'color': "#FFA500"},
                        {'range': [70, 100], 'color': "#FF4444"}
                    ]
                }
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': "white", 'family': "Arial"},
                height=250
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    def log_heart_rate(self, rate, measurement_time):
        """Log heart rate data"""
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().strftime('%H:%M'),
            'heart_rate': rate,
            'measurement_time': measurement_time
        }
        
        st.session_state.heart_rate_data.append(log_entry)
    
    def log_blood_pressure(self, systolic, diastolic):
        """Log blood pressure data"""
        log_entry = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().strftime('%H:%M'),
            'systolic': systolic,
            'diastolic': diastolic,
            'category': self.get_bp_category(systolic, diastolic)
        }
        
        st.session_state.blood_pressure_data.append(log_entry)
    
    def get_bp_category(self, systolic, diastolic):
        """Get blood pressure category"""
        if systolic < 120 and diastolic < 80:
            return "Normal"
        elif systolic < 130 and diastolic < 80:
            return "Elevated"
        elif systolic < 140 or diastolic < 90:
            return "High (Stage 1)"
        else:
            return "High (Stage 2)"
    
    def get_heart_rate_data(self):
        """Get heart rate data for display"""
        if st.session_state.heart_rate_data:
            latest = st.session_state.heart_rate_data[-1]
            current = latest['heart_rate']
        else:
            current = 72
        
        return {
            'current': current,
            'min': 40,
            'max': 200,
            'optimal_min': 60,
            'optimal_max': 100
        }
    
    def get_sleep_data(self):
        """Get sleep data for display"""
        if st.session_state.sleep_history:
            recent = st.session_state.sleep_history[-3:]  # Last 3 days
            data = {}
            for i, sleep in enumerate(recent[::-1]):  # Reverse to show newest last
                day = (datetime.now() - timedelta(days=i)).strftime('%a')
                data[day] = sleep['hours']
        else:
            data = {'Mon': 7, 'Tue': 6.5, 'Wed': 8}
        
        return data
    
    def calculate_stress_level(self):
        """Calculate overall stress level"""
        if not st.session_state.stress_history:
            return 50
        
        # Average of last 3 stress levels
        recent = st.session_state.stress_history[-3:]
        if recent:
            avg_level = sum(s['level'] for s in recent) / len(recent)
            return int((avg_level / 10) * 100)
        
        return 50