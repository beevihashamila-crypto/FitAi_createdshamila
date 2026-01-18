import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="Goal Tracker",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .goals-header {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #00FF87, #00D4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 2rem;
    }
    .goal-card {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid #00FF87;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    .goal-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0, 255, 135, 0.2);
    }
    .milestone-card {
        background: rgba(0, 20, 10, 0.8);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(0, 255, 135, 0.3);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for goals
if "user_goals" not in st.session_state:
    st.session_state.user_goals = []
if "goal_progress" not in st.session_state:
    st.session_state.goal_progress = {}
if "milestones" not in st.session_state:
    st.session_state.milestones = []
if "show_goal_form" not in st.session_state:
    st.session_state.show_goal_form = False
if "show_progress_charts" not in st.session_state:
    st.session_state.show_progress_charts = False
if "selected_goal_for_update" not in st.session_state:
    st.session_state.selected_goal_for_update = None

# Sample goals if none exist
if not st.session_state.user_goals:
    st.session_state.user_goals = [
        {
            "id": 1,
            "title": "Lose 5kg",
            "category": "weight",
            "target": 5,
            "current": 0,
            "unit": "kg",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
            "priority": "high",
            "status": "active"
        },
        {
            "id": 2,
            "title": "Run 5km without stopping",
            "category": "fitness",
            "target": 5,
            "current": 2,
            "unit": "km",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=60)).strftime("%Y-%m-%d"),
            "priority": "medium",
            "status": "active"
        },
        {
            "id": 3,
            "title": "Drink 2L water daily",
            "category": "health",
            "target": 30,
            "current": 15,
            "unit": "days",
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "priority": "high",
            "status": "active"
        }
    ]

# Main App
st.markdown('<h1 class="goals-header">🎯 GOAL TRACKER</h1>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard", 
    "➕ Set Goals", 
    "📈 Progress", 
    "🏆 Milestones"
])

# Tab 1: Dashboard
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Active Goals")
        
        active_goals = [g for g in st.session_state.user_goals if g.get("status") == "active"]
        
        if active_goals:
            for goal in active_goals:
                # Calculate progress
                if goal["target"] > 0:
                    progress = (goal["current"] / goal["target"]) * 100
                else:
                    progress = 0
                
                # Days remaining
                end_date = datetime.strptime(goal["end_date"], "%Y-%m-%d")
                days_remaining = max(0, (end_date - datetime.now()).days)
                
                # Priority color
                priority_colors = {
                    "high": "#FF4444",
                    "medium": "#FFA500",
                    "low": "#00FF87"
                }
                priority_color = priority_colors.get(goal.get("priority", "medium"), "#00FF87")
                
                # Display goal card using Streamlit components
                with st.container():
                    col_title, col_value = st.columns([3, 1])
                    
                    with col_title:
                        st.markdown(f"""
                        <div style="color: {priority_color}; font-weight: 600; font-size: 1.2rem; margin-bottom: 0.5rem;">
                            {goal['title']}
                        </div>
                        <div style="color: #CCCCCC; font-size: 0.9rem;">
                            📅 {goal['start_date']} → {goal['end_date']} ({days_remaining} days remaining)
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col_value:
                        st.markdown(f"""
                        <div style="color: #00FF87; font-weight: 600; font-size: 1.2rem; text-align: right;">
                            {goal['current']}/{goal['target']}{goal['unit']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Progress bar
                st.markdown(f"""
                <div style="margin-top: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; color: #CCCCCC; font-size: 0.9rem;">
                        <span>Progress</span>
                        <span>{progress:.0f}%</span>
                    </div>
                    <div style="background: rgba(255, 255, 255, 0.1); height: 10px; border-radius: 5px; margin-top: 0.2rem;">
                        <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                                   width: {min(progress, 100)}%; height: 100%; border-radius: 5px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(f"📝 Update", key=f"update_{goal['id']}", use_container_width=True):
                        st.session_state.selected_goal_for_update = goal['id']
                        st.rerun()
                
                with btn_col2:
                    if st.button(f"✅ Complete", key=f"complete_{goal['id']}", use_container_width=True):
                        goal['status'] = "completed"
                        goal['completed_date'] = datetime.now().strftime("%Y-%m-%d")
                        
                        # Add milestone
                        milestone = {
                            "goal_id": goal['id'],
                            "title": f"Completed: {goal['title']}",
                            "description": f"Achieved target of {goal['target']}{goal['unit']}",
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "type": "goal_completion"
                        }
                        st.session_state.milestones.append(milestone)
                        
                        st.success(f"Goal '{goal['title']}' marked as completed!")
                        st.rerun()
                
                st.divider()
        else:
            st.info("No active goals. Set your first goal to get started!")
    
    with col2:
        st.subheader("📊 Goal Statistics")
        
        if active_goals:
            # Calculate stats
            total_goals = len(active_goals)
            completed_goals = len([g for g in st.session_state.user_goals if g.get("status") == "completed"])
            
            # Calculate average progress safely
            progress_sum = 0
            valid_goals = 0
            for g in active_goals:
                if g["target"] > 0:
                    progress_sum += (g["current"] / g["target"]) * 100
                    valid_goals += 1
            
            avg_progress = progress_sum / valid_goals if valid_goals > 0 else 0
            
            # Display stats
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.markdown(f"""
                <div class="milestone-card" style="margin-bottom: 1rem;">
                    <div style="color: #00FF87; font-size: 2rem;">{total_goals}</div>
                    <div style="color: #CCCCCC;">Active Goals</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_stat2:
                st.markdown(f"""
                <div class="milestone-card" style="margin-bottom: 1rem;">
                    <div style="color: #00FF87; font-size: 2rem;">{completed_goals}</div>
                    <div style="color: #CCCCCC;">Completed</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_stat3:
                st.markdown(f"""
                <div class="milestone-card">
                    <div style="color: #00FF87; font-size: 2rem;">{avg_progress:.0f}%</div>
                    <div style="color: #CCCCCC;">Avg Progress</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active goals to display statistics")
        
        # Quick actions
        st.subheader("⚡ Quick Actions")
        
        if st.button("🎯 Set New Goal", use_container_width=True):
            st.session_state.show_goal_form = True
            st.rerun()
        
        if st.button("📊 View Progress Charts", use_container_width=True):
            st.session_state.show_progress_charts = True
        
        # Motivation quote
        st.subheader("💪 Motivation")
        
        quotes = [
            "The only bad workout is the one that didn't happen.",
            "Don't wish for it, work for it.",
            "Progress, not perfection.",
            "Your body can stand almost anything. It's your mind you have to convince.",
            "The hardest lift is lifting your butt off the couch.",
            "Small daily improvements lead to stunning results."
        ]
        
        quote = random.choice(quotes)
        
        st.markdown(f"""
        <div style="background: rgba(0, 255, 135, 0.1); padding: 1.5rem; border-radius: 15px; 
                    margin-top: 1rem; border-left: 5px solid #00FF87;">
            <div style="color: #CCCCCC; font-style: italic;">"{quote}"</div>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Set Goals
with tab2:
    st.subheader("➕ Set New Goal")
    
    with st.form("goal_form", border=True):
        col1, col2 = st.columns(2)
        
        with col1:
            goal_title = st.text_input("Goal Title", placeholder="e.g., Lose 5kg, Run 5km, Drink more water")
            goal_category = st.selectbox("Category", 
                                        ["Weight", "Fitness", "Nutrition", "Health", "Mental", "Other"])
            
            col_target, col_current = st.columns(2)
            with col_target:
                target_value = st.number_input("Target Value", min_value=0.1, max_value=1000.0, value=5.0, step=0.1)
            with col_current:
                current_value = st.number_input("Current Value", min_value=0.0, max_value=1000.0, value=0.0, step=0.1)
            
            unit = st.selectbox("Unit", ["kg", "lbs", "km", "miles", "days", "times", "liters", "glasses", "hours", "%"])
        
        with col2:
            priority = st.select_slider("Priority", ["Low", "Medium", "High"], value="Medium")
            
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input("Start Date", datetime.now())
            with col_end:
                end_date = st.date_input("End Date", datetime.now() + timedelta(days=30))
            
            description = st.text_area("Description", 
                                      placeholder="Describe your goal in detail. Why is it important to you?",
                                      height=100)
            
            reminders = st.checkbox("Enable weekly reminders")
        
        submitted = st.form_submit_button("🎯 Set Goal", type="primary")
        
        if submitted:
            if goal_title and target_value > 0:
                new_goal = {
                    "id": len(st.session_state.user_goals) + 1,
                    "title": goal_title,
                    "category": goal_category.lower(),
                    "target": float(target_value),
                    "current": float(current_value),
                    "unit": unit,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "priority": priority.lower(),
                    "description": description,
                    "reminders": reminders,
                    "status": "active",
                    "created_date": datetime.now().strftime("%Y-%m-%d")
                }
                
                st.session_state.user_goals.append(new_goal)
                
                # Initialize progress tracking
                goal_key = f"goal_{new_goal['id']}"
                if goal_key not in st.session_state.goal_progress:
                    st.session_state.goal_progress[goal_key] = []
                
                st.success(f"✅ Goal '{goal_title}' set successfully!")
                st.balloons()
                
                # Show next steps
                st.info("""
                **Next steps:**
                1. Track your progress regularly
                2. Update your progress in the Progress tab
                3. Celebrate small wins along the way
                4. Adjust if needed - goals can evolve!
                """)
            else:
                st.warning("Please enter a goal title and target value")

# Tab 3: Progress
with tab3:
    st.subheader("📈 Goal Progress Tracking")
    
    if not st.session_state.user_goals:
        st.info("No goals to track. Set your first goal!")
    else:
        # Goal selector - only active goals
        active_goals = [g for g in st.session_state.user_goals if g['status'] == 'active']
        
        if active_goals:
            goal_options = {f"{g['id']}: {g['title']}": g['id'] for g in active_goals}
            
            selected_goal_label = st.selectbox("Select Goal to Track", list(goal_options.keys()))
            selected_goal_id = goal_options[selected_goal_label]
            
            selected_goal = next((g for g in st.session_state.user_goals if g['id'] == selected_goal_id), None)
            
            if selected_goal:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Update progress
                    st.markdown("### 📝 Update Progress")
                    
                    with st.form("progress_form"):
                        new_value = st.number_input(
                            f"Current {selected_goal['unit']}",
                            min_value=0.0,
                            max_value=float(selected_goal['target'] * 2),
                            value=float(selected_goal['current']),
                            step=0.1
                        )
                        
                        notes = st.text_area("Progress Notes", placeholder="How did you make progress? Any challenges?")
                        
                        submit_progress = st.form_submit_button("💾 Update Progress", type="primary")
                        
                        if submit_progress:
                            # Update goal
                            selected_goal['current'] = new_value
                            
                            # Add to progress history
                            goal_key = f"goal_{selected_goal['id']}"
                            if goal_key not in st.session_state.goal_progress:
                                st.session_state.goal_progress[goal_key] = []
                            
                            progress_entry = {
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "value": new_value,
                                "notes": notes,
                                "timestamp": datetime.now().strftime("%H:%M")
                            }
                            
                            st.session_state.goal_progress[goal_key].append(progress_entry)
                            
                            # Check if goal is completed
                            if new_value >= selected_goal['target']:
                                selected_goal['status'] = "completed"
                                selected_goal['completed_date'] = datetime.now().strftime("%Y-%m-%d")
                                
                                # Add milestone
                                milestone = {
                                    "goal_id": selected_goal['id'],
                                    "title": f"Completed: {selected_goal['title']}",
                                    "description": f"Achieved target of {selected_goal['target']}{selected_goal['unit']}",
                                    "date": datetime.now().strftime("%Y-%m-%d"),
                                    "type": "goal_completion"
                                }
                                st.session_state.milestones.append(milestone)
                                
                                st.success(f"🎉 Congratulations! You've completed '{selected_goal['title']}'!")
                                st.balloons()
                            else:
                                st.success("Progress updated!")
                
                with col2:
                    # Progress visualization
                    st.markdown("### 📊 Progress Chart")
                    
                    goal_key = f"goal_{selected_goal['id']}"
                    progress_data = st.session_state.goal_progress.get(goal_key, [])
                    
                    if progress_data:
                        # Create progress chart
                        dates = [p["date"] for p in progress_data]
                        values = [p["value"] for p in progress_data]
                        
                        fig = go.Figure()
                        
                        fig.add_trace(go.Scatter(
                            x=dates,
                            y=values,
                            mode='lines+markers',
                            name='Progress',
                            line=dict(color='#00FF87', width=3),
                            marker=dict(size=8, color='#00D4FF')
                        ))
                        
                        # Add target line
                        fig.add_hline(y=selected_goal['target'], line_dash="dash", 
                                     line_color="#FFA500", annotation_text="Target")
                        
                        fig.update_layout(
                            title=f"Progress: {selected_goal['title']}",
                            xaxis_title="Date",
                            yaxis_title=f"Value ({selected_goal['unit']})",
                            paper_bgcolor='rgba(0,0,0,0)',
                            plot_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white'),
                            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No progress data yet. Update your progress to see the chart.")
                
                # Progress history
                st.markdown("### 📋 Progress History")
                
                if progress_data:
                    for entry in reversed(progress_data[-5:]):  # Show last 5 entries
                        st.markdown(f"""
                        <div style="background: rgba(0, 255, 135, 0.05); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <div style="color: #00FF87; font-weight: 600;">{entry['date']} {entry['timestamp']}</div>
                                <div style="color: white; font-weight: 600;">{entry['value']}{selected_goal['unit']}</div>
                            </div>
                            <div style="color: #CCCCCC; margin-top: 0.5rem;">{entry.get('notes', 'No notes')}</div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No progress entries yet. Make your first update!")
            else:
                st.warning("Selected goal not found!")
        else:
            st.info("No active goals to track. Complete some goals or set new ones!")

# Tab 4: Milestones
with tab4:
    st.subheader("🏆 Milestones & Achievements")
    
    if st.session_state.milestones:
        # Group by type
        completed_goals = [m for m in st.session_state.milestones if m['type'] == 'goal_completion']
        
        if completed_goals:
            st.markdown("### ✅ Completed Goals")
            
            cols = st.columns(3)
            for i, milestone in enumerate(completed_goals[-3:]):  # Last 3
                with cols[i % 3]:
                    st.markdown(f"""
                    <div class="milestone-card">
                        <div style="color: #00FF87; font-size: 2rem;">🏆</div>
                        <div style="color: white; font-weight: 600; margin: 0.5rem 0;">{milestone['title']}</div>
                        <div style="color: #CCCCCC; font-size: 0.9rem;">{milestone['description']}</div>
                        <div style="color: #999999; font-size: 0.8rem; margin-top: 0.5rem;">{milestone['date']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Upcoming milestones
        st.markdown("### 🎯 Upcoming Milestones")
        
        upcoming = [
            {"title": "7-Day Streak", "description": "Log consistently for 7 days", "progress": "3/7"},
            {"title": "First 5kg", "description": "Lose your first 5kg", "progress": "2/5 kg"},
            {"title": "Fitness Consistency", "description": "Complete 10 workouts", "progress": "6/10"},
        ]
        
        for milestone in upcoming:
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 1rem; margin: 0.5rem 0; 
                        background: rgba(255, 255, 255, 0.05); border-radius: 10px;">
                <div style="font-size: 2rem; margin-right: 1rem; color: #666666;">🎯</div>
                <div style="flex: 1;">
                    <div style="color: #CCCCCC; font-weight: 600;">{milestone['title']}</div>
                    <div style="color: #999999; font-size: 0.9rem;">{milestone['description']}</div>
                </div>
                <div style="color: #00FF87; font-weight: 600;">{milestone['progress']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No milestones yet. Complete your first goal to earn a milestone!")
        
        # Sample achievements to aim for
        st.markdown("### 🎯 Achievements to Unlock")
        
        achievements = [
            {"icon": "🔥", "title": "Consistency King", "description": "7-day streak", "status": "🔒"},
            {"icon": "💪", "title": "Fitness Starter", "description": "Complete 5 workouts", "status": "🔒"},
            {"icon": "🥦", "title": "Nutrition Pro", "description": "Log meals for 5 days", "status": "🔒"},
            {"icon": "💧", "title": "Hydration Hero", "description": "Meet water goal 7 days", "status": "🔒"},
        ]
        
        cols = st.columns(2)
        for i, achievement in enumerate(achievements):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
                    <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                        <div style="font-size: 1.5rem; margin-right: 0.5rem;">{achievement['icon']}</div>
                        <div style="color: #CCCCCC; font-weight: 600;">{achievement['title']}</div>
                        <div style="margin-left: auto; color: #666666;">{achievement['status']}</div>
                    </div>
                    <div style="color: #999999; font-size: 0.9rem;">{achievement['description']}</div>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🎯 Goal Tracker v1.0 • Track your progress, achieve your dreams!")