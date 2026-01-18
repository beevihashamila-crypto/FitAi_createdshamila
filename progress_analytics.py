import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

class ProgressAnalytics:
    def __init__(self):
        pass
    
    def render(self):
        """Render progress analytics interface"""
        st.markdown('<h1 class="main-header">📈 PROGRESS ANALYTICS</h1>', unsafe_allow_html=True)
        
        tabs = st.tabs(["BMI Tracker", "Fitness Goals", "Workout Progress", "Nutrition Progress", "Health Trends"])
        
        with tabs[0]:
            self.render_bmi_tracker()
        
        with tabs[1]:
            self.render_fitness_goals()
        
        with tabs[2]:
            self.render_workout_progress()
        
        with tabs[3]:
            self.render_nutrition_progress()
        
        with tabs[4]:
            self.render_health_trends()
    
    def render_bmi_tracker(self):
        """Render BMI tracking interface"""
        st.markdown('<div class="section-header">⚖️ BMI TRACKER</div>', unsafe_allow_html=True)
        
        if 'profile_data' not in st.session_state:
            st.warning("Please complete your profile first!")
            return
        
        profile = st.session_state.profile_data
        personal = profile['personal']
        goals = profile['goals']
        
        # Calculate current BMI
        height_m = personal['height'] / 100
        current_weight = personal['weight']
        target_weight = goals['target_weight']
        
        current_bmi = self.calculate_bmi()
        target_bmi = target_weight / (height_m ** 2) if height_m > 0 else 0
        
        bmi_category = self.get_bmi_category(current_bmi)
        target_category = self.get_bmi_category(target_bmi)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Current BMI display
            category_colors = {
                'Underweight': '#FFA500',
                'Normal': '#00FF87',
                'Overweight': '#FFA500',
                'Obese': '#FF4444'
            }
            
            color = category_colors.get(bmi_category, '#00FF87')
            
            st.markdown(f"""
            <div class="stats-card">
                <h4 style="color: {color};">CURRENT BMI</h4>
                <div style="text-align: center; margin: 1.5rem 0;">
                    <div style="color: white; font-size: 3.5rem; font-weight: 800;">{current_bmi:.1f}</div>
                    <div style="color: {color}; font-size: 1.2rem; margin-top: 0.5rem;">{bmi_category}</div>
                </div>
                <div style="color: #CCCCCC; text-align: center;">
                    Weight: {current_weight} kg | Height: {personal['height']} cm
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Target BMI display
            target_color = category_colors.get(target_category, '#00FF87')
            
            st.markdown(f"""
            <div class="stats-card">
                <h4 style="color: {target_color};">TARGET BMI</h4>
                <div style="text-align: center; margin: 1.5rem 0;">
                    <div style="color: white; font-size: 3.5rem; font-weight: 800;">{target_bmi:.1f}</div>
                    <div style="color: {target_color}; font-size: 1.2rem; margin-top: 0.5rem;">{target_category}</div>
                </div>
                <div style="color: #CCCCCC; text-align: center;">
                    Target Weight: {target_weight} kg
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # BMI Progress
        weight_difference = target_weight - current_weight
        progress_percent = 0
        
        if weight_difference > 0:  # Need to gain weight
            if current_weight < target_weight:
                progress_percent = (current_weight / target_weight) * 100
        else:  # Need to lose weight
            start_weight = current_weight + abs(weight_difference) * 2
            if start_weight > current_weight:
                progress_percent = ((start_weight - current_weight) / abs(weight_difference)) * 100
        
        progress_percent = min(progress_percent, 100)
        
        st.markdown("**📊 PROGRESS TO GOAL**")
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; color: #CCCCCC;">
                <span>Progress</span>
                <span>{progress_percent:.1f}%</span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); height: 20px; border-radius: 10px;">
                <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                           width: {progress_percent}%; height: 100%; border-radius: 10px;"></div>
            </div>
            <div style="color: #999999; text-align: center; margin-top: 10px;">
                {abs(weight_difference):.1f} kg {'to gain' if weight_difference > 0 else 'to lose'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # BMI Chart
        st.markdown("**📈 BMI CHART**")
        
        # Create sample BMI history
        bmi_history = self.create_bmi_history(current_bmi, target_bmi)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(bmi_history.keys()),
            y=list(bmi_history.values()),
            mode='lines+markers',
            line=dict(color='#00FF87', width=3),
            marker=dict(size=8, color='#00D4FF'),
            name='BMI'
        ))
        
        # Add target line
        fig.add_hline(y=target_bmi, line_dash="dash", line_color="#FFA500", 
                     annotation_text="Target", annotation_position="bottom right")
        
        # Add healthy range
        fig.add_hrect(y0=18.5, y1=24.9, fillcolor="rgba(0, 255, 135, 0.1)", 
                     layer="below", line_width=0)
        
        fig.update_layout(
            title="BMI Progress Over Time",
            xaxis_title="Date",
            yaxis_title="BMI",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations based on BMI
        recommendations = self.get_bmi_recommendations(current_bmi, target_bmi)
        
        st.markdown("**💡 RECOMMENDATIONS**")
        
        for rec in recommendations:
            st.info(rec)
    
    def calculate_bmi(self):
        """Calculate BMI from profile data"""
        if 'profile_data' not in st.session_state:
            return 22.0
        
        profile = st.session_state.profile_data
        height_m = profile['personal']['height'] / 100
        weight = profile['personal']['weight']
        
        if height_m > 0:
            return weight / (height_m ** 2)
        return 22.0
    
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
    
    def create_bmi_history(self, current_bmi, target_bmi):
        """Create sample BMI history"""
        history = {}
        
        for i in range(30, 0, -1):
            date = (datetime.now() - timedelta(days=i)).strftime('%m/%d')
            # Simulate progress toward target
            progress = i / 30
            bmi = current_bmi + (target_bmi - current_bmi) * (1 - progress)
            history[date] = round(bmi, 1)
        
        return history
    
    def get_bmi_recommendations(self, current_bmi, target_bmi):
        """Get recommendations based on BMI"""
        recommendations = []
        
        if current_bmi < 18.5:
            recommendations.append("Focus on calorie-dense, nutritious foods")
            recommendations.append("Include strength training to build muscle mass")
            recommendations.append("Consider smaller, more frequent meals")
        
        elif current_bmi > 25:
            recommendations.append("Create a consistent calorie deficit")
            recommendations.append("Combine cardio and strength training")
            recommendations.append("Focus on whole foods and protein")
        
        if abs(target_bmi - current_bmi) > 2:
            recommendations.append(f"Aim to {'gain' if target_bmi > current_bmi else 'lose'} "
                                 f"{abs(target_bmi - current_bmi):.1f} BMI points")
        
        if not recommendations:
            recommendations.append("Maintain your current healthy habits")
            recommendations.append("Focus on body composition rather than weight")
        
        return recommendations
    
    def render_fitness_goals(self):
        """Render fitness goals tracking"""
        st.markdown('<div class="section-header">🎯 FITNESS GOALS TRACKER</div>', unsafe_allow_html=True)
        
        if 'profile_data' not in st.session_state:
            st.warning("Please complete your profile first!")
            return
        
        goals = st.session_state.profile_data['goals']
        
        # Primary goal
        primary_goal = goals.get('primary_goal', 'general_fitness')
        secondary_goals = goals.get('secondary_goals', [])
        
        col1, col2 = st.columns(2)
        
        with col1:
            goal_descriptions = {
                'weight_loss': 'Reduce body fat percentage',
                'muscle_gain': 'Increase lean muscle mass',
                'endurance': 'Improve cardiovascular fitness',
                'flexibility': 'Increase range of motion',
                'general_fitness': 'Overall health improvement'
            }
            
            st.markdown(f"""
            <div class="stats-card">
                <h4 style="color: #00FF87;">🎯 PRIMARY GOAL</h4>
                <div style="text-align: center; margin: 1.5rem 0;">
                    <div style="color: white; font-size: 2rem; font-weight: 600;">
                        {primary_goal.replace('_', ' ').title()}
                    </div>
                    <div style="color: #CCCCCC; margin-top: 1rem;">
                        {goal_descriptions.get(primary_goal, 'Custom fitness goal')}
                    </div>
                </div>
                <div style="color: #999999; text-align: center;">
                    Timeline: {goals.get('timeline', '3_months').replace('_', ' ').title()}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if secondary_goals:
                goals_list = '<br>'.join([f"• {g.replace('_', ' ').title()}" for g in secondary_goals])
            else:
                goals_list = "No secondary goals set"
            
            st.markdown(f"""
            <div class="stats-card">
                <h4 style="color: #00FF87;">📋 SECONDARY GOALS</h4>
                <div style="color: #CCCCCC; margin: 1.5rem 0; min-height: 120px;">
                    {goals_list}
                </div>
                <div style="color: #999999; text-align: center;">
                    {len(secondary_goals)} goal{'s' if len(secondary_goals) != 1 else ''} set
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Goal progress tracking
        st.markdown("**📊 GOAL PROGRESS**")
        
        goal_progress = self.calculate_goal_progress(primary_goal)
        
        for goal, progress in goal_progress.items():
            st.markdown(f"""
            <div style="margin: 1rem 0;">
                <div style="display: flex; justify-content: space-between; color: #CCCCCC;">
                    <span>{goal.replace('_', ' ').title()}</span>
                    <span>{progress['percent']:.0f}%</span>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); height: 15px; border-radius: 8px;">
                    <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                               width: {progress['percent']}%; height: 100%; border-radius: 8px;"></div>
                </div>
                <div style="color: #999999; font-size: 0.9rem;">
                    {progress['status']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Milestone tracker
        st.markdown("**🏆 MILESTONES**")
        
        milestones = self.get_milestones(primary_goal)
        
        cols = st.columns(3)
        for i, milestone in enumerate(milestones[:3]):
            with cols[i]:
                status = "✅" if milestone['achieved'] else "⏳"
                color = "#00FF87" if milestone['achieved'] else "#666666"
                
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px; 
                            border: 1px solid {color}; text-align: center;">
                    <div style="color: {color}; font-size: 2rem;">{status}</div>
                    <div style="color: white; margin: 0.5rem 0;">{milestone['title']}</div>
                    <div style="color: #999999; font-size: 0.9rem;">{milestone['description']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    def calculate_goal_progress(self, primary_goal):
        """Calculate progress toward goals"""
        progress = {}
        
        # Weight goal progress
        if 'profile_data' in st.session_state:
            profile = st.session_state.profile_data
            current_weight = profile['personal']['weight']
            target_weight = profile['goals']['target_weight']
            
            if primary_goal == 'weight_loss':
                if current_weight < target_weight:
                    percent = 100
                    status = "Goal achieved! 🎉"
                else:
                    # Assuming starting weight was current_weight + (current_weight - target_weight)
                    start_weight = current_weight + (current_weight - target_weight)
                    percent = ((start_weight - current_weight) / (start_weight - target_weight)) * 100
                    status = f"{current_weight - target_weight:.1f} kg to go"
            else:
                percent = 50  # Default for other goals
                status = "In progress"
            
            progress['weight'] = {'percent': min(percent, 100), 'status': status}
        
        # Workout consistency progress
        if 'workout_history' in st.session_state:
            workouts = st.session_state.workout_history
            recent_workouts = [w for w in workouts 
                              if datetime.strptime(w.get('date', '2000-01-01'), '%Y-%m-%d') 
                              >= datetime.now() - timedelta(days=30)]
            
            percent = min((len(recent_workouts) / 12) * 100, 100)  # 12 workouts/month target
            progress['consistency'] = {
                'percent': percent,
                'status': f"{len(recent_workouts)} workouts this month"
            }
        
        return progress
    
    def get_milestones(self, primary_goal):
        """Get milestones for the primary goal"""
        milestones = [
            {
                'title': 'First Week Complete',
                'description': '7 consecutive days of tracking',
                'achieved': st.session_state.get('streak_days', 0) >= 7
            },
            {
                'title': 'Consistent Month',
                'description': '20+ workouts in 30 days',
                'achieved': False
            },
            {
                'title': 'Nutrition Master',
                'description': '7 days of perfect nutrition',
                'achieved': False
            }
        ]
        
        return milestones
    
    def render_workout_progress(self):
        """Render workout progress tracking"""
        st.markdown('<div class="section-header">🏋️‍♂️ WORKOUT PROGRESS</div>', unsafe_allow_html=True)
        
        if 'workout_history' not in st.session_state or not st.session_state.workout_history:
            st.info("No workout data yet. Complete your first workout!")
            return
        
        workouts = st.session_state.workout_history
        
        # Statistics
        total_workouts = len(workouts)
        total_calories = sum(w.get('calories', 0) for w in workouts)
        total_duration = sum(w.get('duration', 0) for w in workouts)
        
        # Last 30 days
        recent_date = datetime.now() - timedelta(days=30)
        recent_workouts = [w for w in workouts 
                          if datetime.strptime(w.get('date', '2000-01-01'), '%Y-%m-%d') >= recent_date]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Workouts", total_workouts)
        with col2:
            st.metric("Calories Burned", f"{total_calories:,}")
        with col3:
            st.metric("Total Hours", f"{total_duration/60:.0f}")
        
        # Weekly progress chart
        st.markdown("**📈 WEEKLY PROGRESS**")
        
        weekly_data = self.calculate_weekly_workouts()
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(weekly_data.keys()),
                y=list(weekly_data.values()),
                marker_color='#00FF87',
                text=list(weekly_data.values()),
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Workouts Per Week (Last 8 Weeks)",
            xaxis_title="Week",
            yaxis_title="Number of Workouts",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance metrics
        st.markdown("**⚡ PERFORMANCE METRICS**")
        
        if recent_workouts:
            avg_calories = sum(w.get('calories', 0) for w in recent_workouts) / len(recent_workouts)
            avg_duration = sum(w.get('duration', 0) for w in recent_workouts) / len(recent_workouts)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #00FF87; font-size: 1.2rem;">🔥 AVERAGE CALORIES</div>
                    <div style="text-align: center; margin: 1rem 0;">
                        <div style="color: white; font-size: 2.5rem; font-weight: 800;">{avg_calories:.0f}</div>
                        <div style="color: #CCCCCC;">per workout</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #00FF87; font-size: 1.2rem;">⏱️ AVERAGE DURATION</div>
                    <div style="text-align: center; margin: 1rem 0;">
                        <div style="color: white; font-size: 2.5rem; font-weight: 800;">{avg_duration:.0f}</div>
                        <div style="color: #CCCCCC;">minutes</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    def calculate_weekly_workouts(self):
        """Calculate workouts per week for last 8 weeks"""
        if 'workout_history' not in st.session_state:
            return {}
        
        workouts = st.session_state.workout_history
        weekly_data = {}
        
        for i in range(8, 0, -1):
            week_start = datetime.now() - timedelta(weeks=i)
            week_end = week_start + timedelta(days=7)
            
            week_workouts = [w for w in workouts 
                            if week_start <= datetime.strptime(w.get('date', '2000-01-01'), '%Y-%m-%d') < week_end]
            
            week_label = f"Week {9-i}"
            weekly_data[week_label] = len(week_workouts)
        
        return weekly_data
    
    def render_nutrition_progress(self):
        """Render nutrition progress tracking"""
        st.markdown('<div class="section-header">🍎 NUTRITION PROGRESS</div>', unsafe_allow_html=True)
        
        if 'nutrition_logs' not in st.session_state or not st.session_state.nutrition_logs:
            st.info("No nutrition data yet. Log your first meal!")
            return
        
        nutrition_logs = st.session_state.nutrition_logs
        
        # Today's nutrition
        today = datetime.now().strftime('%Y-%m-%d')
        today_logs = [log for log in nutrition_logs if log.get('date') == today]
        
        if today_logs:
            today_calories = sum(log.get('calories', 0) for log in today_logs)
            today_protein = sum(log.get('protein', 0) for log in today_logs)
            
            # Get targets using local functions
            protein_target = self.get_protein_target_local()
            calorie_target = self.get_calorie_target_local()
            
            col1, col2 = st.columns(2)
            
            with col1:
                cal_percent = min((today_calories / calorie_target) * 100, 100) if calorie_target > 0 else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #00FF87; font-size: 1.2rem;">🔥 TODAY'S CALORIES</div>
                    <div style="text-align: center; margin: 1rem 0;">
                        <div style="color: white; font-size: 2.5rem; font-weight: 800;">{today_calories}</div>
                        <div style="color: #CCCCCC;">/ {calorie_target} target</div>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); height: 10px; border-radius: 5px;">
                        <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                                   width: {cal_percent}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                    <div style="color: #999999; text-align: center; margin-top: 10px;">
                        {cal_percent:.0f}% of daily goal
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                prot_percent = min((today_protein / protein_target) * 100, 100) if protein_target > 0 else 0
                st.markdown(f"""
                <div class="metric-card">
                    <div style="color: #00FF87; font-size: 1.2rem;">🥚 TODAY'S PROTEIN</div>
                    <div style="text-align: center; margin: 1rem 0;">
                        <div style="color: white; font-size: 2.5rem; font-weight: 800;">{today_protein:.0f}g</div>
                        <div style="color: #CCCCCC;">/ {protein_target}g target</div>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); height: 10px; border-radius: 5px;">
                        <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                                   width: {prot_percent}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                    <div style="color: #999999; text-align: center; margin-top: 10px;">
                        {prot_percent:.0f}% of daily goal
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Weekly nutrition trend
        st.markdown("**📊 WEEKLY NUTRITION TREND**")
        
        weekly_nutrition = self.calculate_weekly_nutrition()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=list(weekly_nutrition.keys()),
            y=[n['calories'] for n in weekly_nutrition.values()],
            mode='lines+markers',
            name='Calories',
            line=dict(color='#00FF87', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=list(weekly_nutrition.keys()),
            y=[n['protein'] for n in weekly_nutrition.values()],
            mode='lines+markers',
            name='Protein (g)',
            line=dict(color='#00D4FF', width=3),
            yaxis='y2'
        ))
        
        fig.update_layout(
            title="Weekly Nutrition Intake",
            xaxis_title="Week",
            yaxis_title="Calories",
            yaxis2=dict(
                title="Protein (g)",
                overlaying='y',
                side='right'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def calculate_weekly_nutrition(self):
        """Calculate weekly nutrition data"""
        if 'nutrition_logs' not in st.session_state:
            return {}
        
        nutrition_logs = st.session_state.nutrition_logs
        weekly_data = {}
        
        for i in range(4, 0, -1):
            week_start = datetime.now() - timedelta(weeks=i)
            week_end = week_start + timedelta(days=7)
            
            week_logs = [log for log in nutrition_logs 
                        if week_start <= datetime.strptime(log.get('date', '2000-01-01'), '%Y-%m-%d') < week_end]
            
            week_calories = sum(log.get('calories', 0) for log in week_logs)
            week_protein = sum(log.get('protein', 0) for log in week_logs)
            
            week_label = f"Week {5-i}"
            weekly_data[week_label] = {
                'calories': week_calories,
                'protein': week_protein
            }
        
        return weekly_data
    
    # NEW: Local functions to replace nutrition_engine imports
    def get_calorie_target_local(self):
        """Calculate calorie target locally"""
        if 'profile_data' not in st.session_state:
            return 2000
        
        profile = st.session_state.profile_data
        goals = profile['goals']
        primary_goal = goals.get('primary_goal', 'general_fitness')
        
        # Calculate TDEE locally
        tdee = self.calculate_tdee_local()
        
        # Adjust based on goal
        adjustments = {
            'weight_loss': -500,
            'muscle_gain': +300,
            'endurance': +200,
            'general_fitness': 0
        }
        
        adjustment = adjustments.get(primary_goal, 0)
        return max(1200, tdee + adjustment)
    
    def get_protein_target_local(self):
        """Calculate protein target locally"""
        if 'profile_data' not in st.session_state:
            return 80
        
        profile = st.session_state.profile_data
        weight = profile['personal']['weight']
        goals = profile['goals']
        primary_goal = goals.get('primary_goal', 'general_fitness')
        
        # Protein per kg based on goal
        protein_per_kg = {
            'weight_loss': 2.0,
            'muscle_gain': 2.2,
            'endurance': 1.6,
            'general_fitness': 1.8
        }
        
        multiplier = protein_per_kg.get(primary_goal, 1.8)
        return int(weight * multiplier)
    
    def calculate_tdee_local(self):
        """Calculate Total Daily Energy Expenditure locally"""
        if 'profile_data' not in st.session_state:
            return 2000
        
        profile = st.session_state.profile_data
        personal = profile['personal']
        lifestyle = profile['lifestyle']
        
        # BMR calculation (Mifflin-St Jeor)
        if personal['gender'] == 'Male':
            bmr = 10 * personal['weight'] + 6.25 * personal['height'] - 5 * personal['age'] + 5
        else:
            bmr = 10 * personal['weight'] + 6.25 * personal['height'] - 5 * personal['age'] - 161
        
        # Activity multiplier
        activity_map = {
            'Sedentary': 1.2,
            'Light': 1.375,
            'Moderate': 1.55,
            'Active': 1.725,
            'Very Active': 1.9
        }
        
        activity = lifestyle.get('activity_level', 'Moderate')
        multiplier = activity_map.get(activity, 1.55)
        
        return int(bmr * multiplier)
    
    def render_health_trends(self):
        """Render health trends tracking"""
        st.markdown('<div class="section-header">❤️ HEALTH TRENDS</div>', unsafe_allow_html=True)
        
        # Health metrics overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Sleep trend
            if st.session_state.get('sleep_history'):
                avg_sleep = sum(s['hours'] for s in st.session_state.sleep_history[-7:]) / 7
            else:
                avg_sleep = 7
            
            sleep_color = '#00FF87' if avg_sleep >= 7 else '#FFA500' if avg_sleep >= 6 else '#FF4444'
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: {sleep_color}; font-size: 1.2rem;">💤 AVERAGE SLEEP</div>
                <div style="text-align: center; margin: 1rem 0;">
                    <div style="color: white; font-size: 2.5rem; font-weight: 800;">{avg_sleep:.1f}</div>
                    <div style="color: #CCCCCC;">hours/night</div>
                </div>
                <div style="color: #999999; text-align: center;">
                    Last 7 days
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Water trend
            avg_water = st.session_state.get('water_intake', 0)
            water_target = st.session_state.profile_data['nutrition']['water_target'] \
                if 'profile_data' in st.session_state else 8
            
            water_percent = min((avg_water / water_target) * 100, 100) if water_target > 0 else 0
            water_color = '#00FF87' if water_percent >= 80 else '#FFA500' if water_percent >= 50 else '#FF4444'
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: {water_color}; font-size: 1.2rem;">💧 DAILY WATER</div>
                <div style="text-align: center; margin: 1rem 0;">
                    <div style="color: white; font-size: 2.5rem; font-weight: 800;">{avg_water:.0f}</div>
                    <div style="color: #CCCCCC;">glasses/day</div>
                </div>
                <div style="color: #999999; text-align: center;">
                    Target: {water_target} glasses
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Mood trend
            if st.session_state.get('mood_history'):
                mood_values = {
                    'happy': 5,
                    'energized': 4,
                    'neutral': 3,
                    'tired': 2,
                    'sad': 1,
                    'angry': 0
                }
                
                recent_moods = st.session_state.mood_history[-7:]
                avg_mood = sum(mood_values.get(m['mood'], 3) for m in recent_moods) / len(recent_moods)
            else:
                avg_mood = 3
            
            mood_color = '#00FF87' if avg_mood >= 4 else '#FFA500' if avg_mood >= 2.5 else '#FF4444'
            mood_text = ['Angry', 'Sad', 'Tired', 'Neutral', 'Energized', 'Happy'][int(avg_mood)]
            
            st.markdown(f"""
            <div class="metric-card">
                <div style="color: {mood_color}; font-size: 1.2rem;">😊 AVERAGE MOOD</div>
                <div style="text-align: center; margin: 1rem 0;">
                    <div style="color: white; font-size: 2.5rem; font-weight: 800;">{mood_text}</div>
                    <div style="color: #CCCCCC;">{avg_mood:.1f}/5.0</div>
                </div>
                <div style="color: #999999; text-align: center;">
                    Last 7 days
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Health improvement chart
        st.markdown("**📈 HEALTH IMPROVEMENT TREND**")
        
        health_data = self.create_health_trend_data()
        
        fig = go.Figure()
        
        metrics = ['Sleep', 'Water', 'Mood', 'Activity']
        colors = ['#00FF87', '#00D4FF', '#FFA500', '#FF4444']
        
        for i, metric in enumerate(metrics):
            fig.add_trace(go.Scatter(
                x=list(health_data.keys()),
                y=[h[metric.lower()] for h in health_data.values()],
                mode='lines+markers',
                name=metric,
                line=dict(color=colors[i], width=2)
            ))
        
        fig.update_layout(
            title="Health Metrics Trend (Last 4 Weeks)",
            xaxis_title="Week",
            yaxis_title="Score (0-100)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("**💡 HEALTH RECOMMENDATIONS**")
        
        recommendations = self.get_health_recommendations()
        
        for rec in recommendations:
            st.info(rec)
    
    def create_health_trend_data(self):
        """Create health trend data"""
        data = {}
        
        for i in range(4, 0, -1):
            week_label = f"Week {5-i}"
            
            # Simulate improving health metrics
            import random
            base_sleep = 70 + i * 5
            base_water = 60 + i * 7
            base_mood = 65 + i * 8
            base_activity = 50 + i * 10
            
            data[week_label] = {
                'sleep': min(base_sleep + random.randint(-5, 5), 100),
                'water': min(base_water + random.randint(-5, 5), 100),
                'mood': min(base_mood + random.randint(-5, 5), 100),
                'activity': min(base_activity + random.randint(-5, 5), 100)
            }
        
        return data
    
    def get_health_recommendations(self):
        """Get health recommendations based on trends"""
        recommendations = []
        
        if 'profile_data' in st.session_state:
            profile = st.session_state.profile_data
            
            # Sleep recommendations
            if profile['health']['sleep_hours'] < 7:
                recommendations.append(f"Aim for 7-9 hours of sleep. Current: {profile['health']['sleep_hours']} hours")
            
            # Water recommendations
            water_target = profile['nutrition']['water_target']
            current_water = st.session_state.get('water_intake', 0)
            if current_water < water_target:
                recommendations.append(f"Drink more water: {current_water}/{water_target} glasses today")
            
            # Stress recommendations
            if profile['health']['stress_level'] == 'High':
                recommendations.append("Practice stress management techniques daily")
        
        if not recommendations:
            recommendations.append("Your health metrics are looking good! Keep up the great work!")
        
        return recommendations
    
    def render_mini_dashboard(self):
        """Render mini progress dashboard for main page"""
        if 'profile_data' not in st.session_state:
            return
        
        # Calculate progress
        bmi = self.calculate_bmi()
        bmi_category = self.get_bmi_category(bmi)
        
        # Streak
        streak = st.session_state.get('streak_days', 0)
        
        # Workouts this week
        if 'workout_history' in st.session_state:
            workouts_week = len([w for w in st.session_state.workout_history 
                                if datetime.strptime(w.get('date', '2000-01-01'), '%Y-%m-%d').isocalendar()[1] 
                                == datetime.now().isocalendar()[1]])
        else:
            workouts_week = 0
        
        st.markdown(f"""
        <div style="background: rgba(0, 20, 10, 0.8); padding: 1.5rem; border-radius: 15px;">
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1rem;">
                <div style="text-align: center;">
                    <div style="color: #00FF87; font-size: 1.5rem;">⚖️</div>
                    <div style="color: white; font-size: 1.2rem;">{bmi:.1f}</div>
                    <div style="color: #CCCCCC; font-size: 0.8rem;">BMI ({bmi_category})</div>
                </div>
                <div style="text-align: center;">
                    <div style="color: #00FF87; font-size: 1.5rem;">🔥</div>
                    <div style="color: white; font-size: 1.2rem;">{streak}</div>
                    <div style="color: #CCCCCC; font-size: 0.8rem;">Day Streak</div>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="color: #00FF87; font-size: 0.9rem;">🏋️‍♂️ {workouts_week} workouts this week</div>
                <div style="color: #999999; font-size: 0.8rem; margin-top: 0.5rem;">
                    Keep up the momentum! 💪
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)