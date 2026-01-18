import streamlit as st
import random
from datetime import datetime, timedelta

class Gamification:
    def __init__(self):
        self.challenges = self.load_challenges()
        self.rewards = self.load_rewards()
        self.initialize_gamification_data()
    
    def initialize_gamification_data(self):
        """Initialize gamification data"""
        defaults = {
            'total_points': 0,
            'level': 1,
            'badges': [],
            'completed_challenges': [],
            'redeemed_rewards': []
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def load_challenges(self):
        """Load available challenges"""
        return [
            {
                'id': 1,
                'title': '7-Day Streak',
                'description': 'Complete your daily logging for 7 consecutive days',
                'points': 100,
                'duration': '7 days',
                'type': 'consistency',
                'requirements': {'streak_days': 7}
            },
            {
                'id': 2,
                'title': 'Water Warrior',
                'description': 'Meet your water goal for 5 days in a row',
                'points': 75,
                'duration': '5 days',
                'type': 'health',
                'requirements': {'water_days': 5}
            },
            {
                'id': 3,
                'title': 'Workout Week',
                'description': 'Complete 5 workouts in 7 days',
                'points': 150,
                'duration': '7 days',
                'type': 'fitness',
                'requirements': {'workouts_week': 5}
            },
            {
                'id': 4,
                'title': 'Nutrition Ninja',
                'description': 'Log all meals for 3 consecutive days',
                'points': 50,
                'duration': '3 days',
                'type': 'nutrition',
                'requirements': {'nutrition_days': 3}
            },
            {
                'id': 5,
                'title': 'Sleep Champion',
                'description': 'Get 7+ hours of sleep for 4 nights',
                'points': 80,
                'duration': '4 days',
                'type': 'recovery',
                'requirements': {'sleep_nights': 4}
            }
        ]
    
    def load_rewards(self):
        """Load available rewards"""
        return [
            {
                'id': 1,
                'name': 'Rest Day Pass',
                'description': 'Skip a day guilt-free',
                'cost': 50,
                'type': 'utility'
            },
            {
                'id': 2,
                'name': 'Custom Workout',
                'description': 'AI-generated personalized workout',
                'cost': 100,
                'type': 'feature'
            },
            {
                'id': 3,
                'name': 'Nutrition Analysis',
                'description': 'Detailed analysis of your eating habits',
                'cost': 75,
                'type': 'insight'
            },
            {
                'id': 4,
                'name': 'Avatar Customization',
                'description': 'Unlock special avatar features',
                'cost': 150,
                'type': 'cosmetic'
            }
        ]
    
    def render(self):
        """Render gamification interface"""
        st.markdown('<h1 class="main-header">🎮 FITNESS GAMIFICATION</h1>', unsafe_allow_html=True)
        
        tabs = st.tabs(["🏆 Level & Points", "🎯 Challenges", "🎁 Rewards", "🛡️ Badges"])
        
        with tabs[0]:
            self.render_level_points()
        
        with tabs[1]:
            self.render_challenges()
        
        with tabs[2]:
            self.render_rewards()
        
        with tabs[3]:
            self.render_badges()
    
    def render_level_points(self):
        """Render level and points system"""
        st.markdown('<div class="section-header">🏆 YOUR FITNESS LEVEL</div>', unsafe_allow_html=True)
        
        # Calculate level progress
        total_points = st.session_state.get('total_points', 0)
        current_level = st.session_state.get('level', 1)
        
        points_for_next_level = current_level * 100
        progress_percent = min((total_points % 100) / 1, 100)  # 100 points per level
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <div style="text-align: center;">
                    <div style="color: #00FF87; font-size: 4rem; font-weight: 800;">{current_level}</div>
                    <div style="color: #CCCCCC; font-size: 1.2rem;">Fitness Level</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <div style="text-align: center;">
                    <div style="color: #00FF87; font-size: 4rem; font-weight: 800;">{total_points}</div>
                    <div style="color: #CCCCCC; font-size: 1.2rem;">Total Points</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress to next level
        st.markdown("**📈 PROGRESS TO NEXT LEVEL**")
        
        st.markdown(f"""
        <div style="margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; color: #CCCCCC;">
                <span>Level {current_level} → Level {current_level + 1}</span>
                <span>{progress_percent:.0f}%</span>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); height: 20px; border-radius: 10px;">
                <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                           width: {progress_percent}%; height: 100%; border-radius: 10px;"></div>
            </div>
            <div style="color: #999999; text-align: center; margin-top: 10px;">
                {points_for_next_level - (total_points % 100)} points to next level
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Daily points breakdown
        st.markdown("**🔥 TODAY'S POINTS**")
        
        daily_points = self.calculate_todays_points()
        
        col1, col2, col3, col4 = st.columns(4)
        
        point_categories = [
            ('💧 Water', daily_points.get('water', 0), 10),
            ('🏋️‍♂️ Workout', daily_points.get('workout', 0), 20),
            ('🍎 Nutrition', daily_points.get('nutrition', 0), 10),
            ('📝 Logging', daily_points.get('logging', 0), 5)
        ]
        
        for i, (label, points, max_points) in enumerate(point_categories):
            with [col1, col2, col3, col4][i]:
                percent = (points / max_points) * 100 if max_points > 0 else 0
                st.markdown(f"""
                <div style="text-align: center;">
                    <div style="color: #00FF87; font-size: 1.5rem;">{points}/{max_points}</div>
                    <div style="color: #CCCCCC; font-size: 0.9rem;">{label}</div>
                    <div style="background: rgba(255, 255, 255, 0.1); height: 5px; border-radius: 3px; margin-top: 5px;">
                        <div style="background: #00FF87; width: {percent}%; height: 100%; border-radius: 3px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # How to earn more points
        st.markdown("**🎯 HOW TO EARN POINTS**")
        
        earning_methods = [
            ("Complete a workout", "+20 points"),
            ("Meet water goal", "+10 points"),
            ("Log all meals", "+10 points"),
            ("Complete daily check-in", "+5 points"),
            ("Finish a challenge", "+50-150 points"),
            ("7-day streak", "+100 points")
        ]
        
        for method, points in earning_methods:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; 
                        padding: 0.5rem; margin: 0.3rem 0; background: rgba(255, 255, 255, 0.05); 
                        border-radius: 8px;">
                <span style="color: #CCCCCC;">{method}</span>
                <span style="color: #00FF87; font-weight: 600;">{points}</span>
            </div>
            """, unsafe_allow_html=True)
    
    def calculate_todays_points(self):
        """Calculate points earned today"""
        points = {
            'water': 0,
            'workout': 0,
            'nutrition': 0,
            'logging': 0
        }
        
        # Water points
        water_target = st.session_state.profile_data['nutrition']['water_target'] \
            if 'profile_data' in st.session_state else 8
        current_water = st.session_state.get('water_intake', 0)
        
        if current_water >= water_target:
            points['water'] = 10
        elif current_water >= water_target * 0.5:
            points['water'] = 5
        
        # Workout points
        today = datetime.now().strftime('%Y-%m-%d')
        if 'workout_history' in st.session_state:
            today_workouts = [w for w in st.session_state.workout_history 
                             if w.get('date') == today]
            if today_workouts:
                points['workout'] = 20
        
        # Nutrition points
        if 'nutrition_logs' in st.session_state:
            today_meals = [m for m in st.session_state.nutrition_logs 
                          if m.get('date') == today]
            if len(today_meals) >= 2:  # At least 2 meals logged
                points['nutrition'] = 10
        
        # Daily logging points
        if 'mood_history' in st.session_state:
            today_moods = [m for m in st.session_state.mood_history 
                          if m.get('date') == today]
            if today_moods:
                points['logging'] = 5
        
        return points
    
    def render_challenges(self):
        """Render challenges interface"""
        st.markdown('<div class="section-header">🎯 FITNESS CHALLENGES</div>', unsafe_allow_html=True)
        
        # Active challenges
        st.markdown("**🔥 ACTIVE CHALLENGES**")
        
        active_challenges = self.get_active_challenges()
        
        if active_challenges:
            for challenge in active_challenges:
                progress = self.calculate_challenge_progress(challenge)
                
                st.markdown(f"""
                <div class="challenge-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <div style="color: #00FF87; font-weight: 600;">{challenge['title']}</div>
                            <div style="color: #CCCCCC; font-size: 0.9rem;">{challenge['description']}</div>
                        </div>
                        <div style="color: #00FF87; font-weight: 600;">{challenge['points']} pts</div>
                    </div>
                    
                    <div style="margin-top: 1rem;">
                        <div style="display: flex; justify-content: space-between; color: #CCCCCC; font-size: 0.9rem;">
                            <span>Progress</span>
                            <span>{progress}%</span>
                        </div>
                        <div style="background: rgba(255, 255, 255, 0.1); height: 8px; border-radius: 4px;">
                            <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                                       width: {progress}%; height: 100%; border-radius: 4px;"></div>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 10px; margin-top: 1rem;">
                        <button style="flex: 1; padding: 8px; background: rgba(0, 255, 135, 0.2); 
                                   border: 1px solid #00FF87; border-radius: 5px; color: #00FF87;">
                            Update Progress
                        </button>
                        <button style="flex: 1; padding: 8px; background: #00FF87; border: none; 
                                   border-radius: 5px; color: black; font-weight: 600;">
                            Complete
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active challenges. Start a new one below!")
        
        # Available challenges
        st.markdown("**📋 AVAILABLE CHALLENGES**")
        
        available_challenges = self.get_available_challenges()
        
        cols = st.columns(2)
        
        for i, challenge in enumerate(available_challenges[:4]):  # Show 4 challenges
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background: rgba(0, 255, 135, 0.05); padding: 1rem; border-radius: 10px; 
                            border: 1px solid rgba(0, 255, 135, 0.3); margin-bottom: 1rem;">
                    <div style="color: #00FF87; font-weight: 600;">{challenge['title']}</div>
                    <div style="color: #CCCCCC; font-size: 0.9rem; margin: 0.5rem 0;">{challenge['description']}</div>
                    <div style="display: flex; justify-content: space-between; color: #999999; font-size: 0.8rem;">
                        <span>🏅 {challenge['points']} points</span>
                        <span>⏱️ {challenge['duration']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Start Challenge", key=f"start_challenge_{challenge['id']}", use_container_width=True):
                    self.start_challenge(challenge)
                    st.success(f"Started: {challenge['title']}!")
                    st.rerun()
    
    def get_active_challenges(self):
        """Get active challenges"""
        # For now, return empty. In full implementation, would check session state
        return []
    
    def get_available_challenges(self):
        """Get available challenges"""
        return self.challenges
    
    def calculate_challenge_progress(self, challenge):
        """Calculate progress for a challenge"""
        # Simplified progress calculation
        return random.randint(20, 80)
    
    def start_challenge(self, challenge):
        """Start a new challenge"""
        if 'active_challenges' not in st.session_state:
            st.session_state.active_challenges = []
        
        challenge['start_date'] = datetime.now().strftime('%Y-%m-%d')
        challenge['progress'] = 0
        
        st.session_state.active_challenges.append(challenge)
    
    def render_rewards(self):
        """Render rewards interface"""
        st.markdown('<div class="section-header">🎁 REWARDS SHOP</div>', unsafe_allow_html=True)
        
        total_points = st.session_state.get('total_points', 0)
        
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <div style="color: #00FF87; font-size: 3rem; font-weight: 800;">{total_points}</div>
            <div style="color: #CCCCCC;">Available Points</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Available rewards
        st.markdown("**🛍️ AVAILABLE REWARDS**")
        
        cols = st.columns(2)
        
        for i, reward in enumerate(self.rewards):
            with cols[i % 2]:
                can_afford = total_points >= reward['cost']
                bg_color = 'rgba(0, 255, 135, 0.1)' if can_afford else 'rgba(255, 255, 255, 0.05)'
                border_color = '#00FF87' if can_afford else '#666666'
                text_color = '#00FF87' if can_afford else '#666666'
                
                st.markdown(f"""
                <div style="background: {bg_color}; padding: 1rem; border-radius: 10px; 
                            border: 2px solid {border_color}; margin-bottom: 1rem;">
                    <div style="color: {text_color}; font-weight: 600; font-size: 1.1rem;">{reward['name']}</div>
                    <div style="color: #CCCCCC; font-size: 0.9rem; margin: 0.5rem 0;">{reward['description']}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: #00FF87; font-weight: 600; font-size: 1.2rem;">{reward['cost']} pts</span>
                        <span style="color: #999999; font-size: 0.8rem;">{reward['type'].upper()}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if can_afford:
                    if st.button(f"Redeem", key=f"redeem_{reward['id']}", use_container_width=True):
                        self.redeem_reward(reward)
                        st.success(f"Redeemed: {reward['name']}!")
                        st.rerun()
                else:
                    st.button(f"Need {reward['cost'] - total_points} more pts", 
                             disabled=True, use_container_width=True)
    
    def redeem_reward(self, reward):
        """Redeem a reward"""
        total_points = st.session_state.get('total_points', 0)
        
        if total_points >= reward['cost']:
            # Deduct points
            st.session_state.total_points = total_points - reward['cost']
            
            # Add to redeemed rewards
            if 'redeemed_rewards' not in st.session_state:
                st.session_state.redeemed_rewards = []
            
            reward_copy = reward.copy()
            reward_copy['redeemed_date'] = datetime.now().strftime('%Y-%m-%d')
            st.session_state.redeemed_rewards.append(reward_copy)
            
            # Apply reward effect
            self.apply_reward_effect(reward)
    
    def apply_reward_effect(self, reward):
        """Apply the effect of a redeemed reward"""
        if reward['id'] == 1:  # Rest Day Pass
            st.session_state.rest_day_passes = st.session_state.get('rest_day_passes', 0) + 1
        elif reward['id'] == 2:  # Custom Workout
            st.session_state.custom_workout_available = True
        # Add effects for other rewards
    
    def render_badges(self):
        """Render badges interface"""
        st.markdown('<div class="section-header">🛡️ BADGES & ACHIEVEMENTS</div>', unsafe_allow_html=True)
        
        badges = self.get_user_badges()
        
        if badges:
            cols = st.columns(4)
            
            for i, badge in enumerate(badges):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem;">
                        <div style="font-size: 3rem; color: #00FF87;">{badge['emoji']}</div>
                        <div style="color: white; font-weight: 600; margin: 0.5rem 0;">{badge['name']}</div>
                        <div style="color: #999999; font-size: 0.8rem;">{badge['description']}</div>
                        <div style="color: #00FF87; font-size: 0.9rem; margin-top: 0.5rem;">
                            Earned: {badge['earned_date']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No badges earned yet. Complete challenges and reach milestones to earn badges!")
        
        # Upcoming badges
        st.markdown("**🎯 UPCOMING BADGES**")
        
        upcoming_badges = [
            {'name': 'Consistency King', 'emoji': '👑', 'requirements': '30-day streak'},
            {'name': 'Nutrition Pro', 'emoji': '🍎', 'requirements': 'Log meals for 14 days'},
            {'name': 'Workout Warrior', 'emoji': '⚔️', 'requirements': '50 workouts'},
            {'name': 'Hydration Hero', 'emoji': '💧', 'requirements': 'Perfect water for 21 days'}
        ]
        
        for badge in upcoming_badges:
            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 1rem; margin: 0.5rem 0; 
                        background: rgba(255, 255, 255, 0.05); border-radius: 10px;">
                <div style="font-size: 2rem; margin-right: 1rem; color: #666666;">{badge['emoji']}</div>
                <div style="flex: 1;">
                    <div style="color: #CCCCCC; font-weight: 600;">{badge['name']}</div>
                    <div style="color: #999999; font-size: 0.9rem;">{badge['requirements']}</div>
                </div>
                <div style="color: #666666;">🔒</div>
            </div>
            """, unsafe_allow_html=True)
    
    def get_user_badges(self):
        """Get user's earned badges"""
        earned_badges = []
        
        # Check for streak badge
        if st.session_state.get('streak_days', 0) >= 7:
            earned_badges.append({
                'name': 'Week Warrior',
                'emoji': '🔥',
                'description': '7-day streak',
                'earned_date': 'Recently'
            })
        
        # Check for workout badge
        if 'workout_history' in st.session_state:
            if len(st.session_state.workout_history) >= 10:
                earned_badges.append({
                    'name': 'Fitness Starter',
                    'emoji': '💪',
                    'description': '10 workouts completed',
                    'earned_date': 'Recently'
                })
        
        return earned_badges