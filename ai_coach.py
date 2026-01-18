import streamlit as st
from huggingface_hub import InferenceClient
import json
import random
from datetime import datetime

class AICoach:
    def __init__(self):
        self.client = None
        self.initialize_ai_client()
        self.conversation_history = []
    
    def initialize_ai_client(self):
        """Initialize Hugging Face AI client"""
        try:
            HF_TOKEN = st.secrets.get("HF_TOKEN", "")
            if HF_TOKEN:
                self.client = InferenceClient("meta-llama/Meta-Llama-3-8B", token=HF_TOKEN)
                st.session_state.ai_available = True
            else:
                self.client = None
                st.session_state.ai_available = False
        except:
            self.client = None
            st.session_state.ai_available = False
    
    def render(self):
        """Render AI coach interface"""
        st.markdown('<h1 class="main-header">🤖 AI FITNESS COACH</h1>', unsafe_allow_html=True)
        
        if not st.session_state.get('ai_available', False):
            self.render_fallback_mode()
            return
        
        tabs = st.tabs(["Chat with AI", "Quick Questions", "AI Analysis", "History"])
        
        with tabs[0]:
            self.render_ai_chat()
        
        with tabs[1]:
            self.render_quick_questions()
        
        with tabs[2]:
            self.render_ai_analysis()
        
        with tabs[3]:
            self.render_conversation_history()
    
    def render_fallback_mode(self):
        """Render fallback when AI is not available"""
        st.warning("⚠️ AI features require Hugging Face token")
        
        st.info("""
        **To enable AI features:**
        1. Get a free token from [Hugging Face](https://huggingface.co/settings/tokens)
        2. Add it to `.streamlit/secrets.toml` as `HF_TOKEN = "your_token_here"`
        3. Restart the app
        """)
        
        # Show manual recommendations
        st.markdown('<div class="section-header">💡 FITNESS TIPS</div>', unsafe_allow_html=True)
        
        tips = [
            "🏋️‍♂️ **Consistency is key** - Even 20 minutes daily is better than 2 hours once a week",
            "🍎 **Eat protein with every meal** - Helps with muscle repair and keeps you full",
            "💧 **Stay hydrated** - Drink at least 8 glasses of water daily",
            "😴 **Prioritize sleep** - Aim for 7-9 hours for optimal recovery",
            "📊 **Track your progress** - What gets measured gets improved",
            "🧘 **Include rest days** - Muscles grow during recovery, not workouts",
            "🥦 **Eat whole foods** - Focus on vegetables, lean proteins, and complex carbs",
            "🔥 **Mix up your workouts** - Combine strength, cardio, and flexibility"
        ]
        
        for tip in tips:
            st.markdown(f"""
            <div class="challenge-card">
                {tip}
            </div>
            """, unsafe_allow_html=True)
    
    def render_ai_chat(self):
        """Render AI chat interface"""
        st.markdown('<div class="section-header">💬 CHAT WITH YOUR AI COACH</div>', unsafe_allow_html=True)
        
        # Initialize conversation history
        if 'ai_conversation' not in st.session_state:
            st.session_state.ai_conversation = []
        
        # Display conversation history
        for message in st.session_state.ai_conversation:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="background: rgba(0, 255, 135, 0.1); padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 4px solid #00FF87;">
                    <div style="color: #00FF87; font-weight: 600;">You</div>
                    <div style="color: white; margin-top: 5px;">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(0, 212, 255, 0.1); padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 4px solid #00D4FF;">
                    <div style="color: #00D4FF; font-weight: 600;">AI Coach</div>
                    <div style="color: white; margin-top: 5px;">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Chat input
        if prompt := st.chat_input("Ask your AI fitness coach anything..."):
            # Add user message
            st.session_state.ai_conversation.append({
                'role': 'user',
                'content': prompt,
                'timestamp': datetime.now().strftime('%H:%M')
            })
            
            # Generate AI response
            with st.spinner("🤖 AI Coach is thinking..."):
                response = self.generate_ai_response(prompt)
                
                st.session_state.ai_conversation.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': datetime.now().strftime('%H:%M')
                })
            
            st.rerun()
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.ai_conversation = []
            st.rerun()
    
    def generate_ai_response(self, user_message):
        """Generate AI response using Hugging Face"""
        try:
            # Create context from user profile
            context = self.create_user_context()
            
            prompt = f"""{context}

User Question: {user_message}

Please respond as a knowledgeable, supportive, and encouraging fitness coach. 
Provide practical, specific advice based on the user's profile and goals.
Keep responses under 200 words."""

            response = self.client.text_generation(
                prompt,
                max_new_tokens=300,
                temperature=0.7,
                do_sample=True
            )
            
            return response.strip()
            
        except Exception as e:
            return f"I'm having trouble connecting right now. Here's some general advice:\n\n{self.get_fallback_response(user_message)}"
    
    def create_user_context(self):
        """Create context from user profile for AI"""
        if 'profile_data' not in st.session_state:
            return "You are a fitness coach helping a new user."
        
        profile = st.session_state.profile_data
        personal = profile['personal']
        goals = profile['goals']
        fitness = profile['fitness']
        
        context = f"""User Profile:
- Name: {personal.get('name', 'User')}
- Age: {personal.get('age', 'Not specified')}
- Gender: {personal.get('gender', 'Not specified')}
- Height: {personal.get('height', 'Not specified')} cm
- Weight: {personal.get('weight', 'Not specified')} kg
- Fitness Level: {fitness.get('fitness_level', 'Beginner')}
- Primary Goal: {goals.get('primary_goal', 'general_fitness').replace('_', ' ')}
- Target Weight: {goals.get('target_weight', 'Not specified')} kg
- Workout Frequency: {fitness.get('workout_days_per_week', 3)} days/week
"""
        
        return context
    
    def get_fallback_response(self, user_message):
        """Get fallback response when AI is unavailable"""
        fallback_responses = [
            "Focus on consistency in your workouts and nutrition. Small daily improvements lead to big results over time.",
            "Remember to listen to your body. Rest when you need to, and push yourself when you can.",
            "A balanced approach works best: combine strength training, cardio, flexibility work, and proper nutrition.",
            "Stay hydrated throughout the day. Water is essential for all bodily functions including fat metabolism.",
            "Get enough sleep. Recovery is when your body repairs and grows stronger.",
            "Track your progress to stay motivated. Celebrate small wins along the way.",
            "Don't compare your journey to others. Focus on being better than you were yesterday."
        ]
        
        return random.choice(fallback_responses)
    
    def render_quick_questions(self):
        """Render quick questions interface"""
        st.markdown('<div class="section-header">🎯 QUICK QUESTIONS</div>', unsafe_allow_html=True)
        
        quick_questions = [
            {
                'question': "How can I stay motivated?",
                'icon': '🔥'
            },
            {
                'question': "Best workout for beginners?",
                'icon': '🏋️‍♂️'
            },
            {
                'question': "How to lose weight effectively?",
                'icon': '⚖️'
            },
            {
                'question': "Importance of rest days?",
                'icon': '😴'
            },
            {
                'question': "Best time to workout?",
                'icon': '⏰'
            },
            {
                'question': "How much protein do I need?",
                'icon': '🥚'
            }
        ]
        
        cols = st.columns(3)
        
        for i, q in enumerate(quick_questions):
            with cols[i % 3]:
                if st.button(f"{q['icon']} {q['question']}", use_container_width=True):
                    response = self.get_quick_answer(q['question'])
                    
                    st.markdown(f"""
                    <div class="joke-box">
                        <div style="color: #00FF87; font-weight: 600;">AI Coach says:</div>
                        <div style="color: white; margin-top: 10px;">{response}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    def get_quick_answer(self, question):
        """Get answer for quick questions"""
        answers = {
            "How can I stay motivated?": """
            **🎯 Set specific, measurable goals** - "Lose 5kg in 2 months" not just "lose weight"
            **📊 Track your progress** - Use this app to see improvements over time
            **🎉 Celebrate small wins** - Every workout counts, every healthy meal matters
            **🤝 Find accountability** - Share goals with friends or use our challenges feature
            **🔄 Mix it up** - Try new workouts to avoid boredom
            """,
            "Best workout for beginners?": """
            **Start with bodyweight exercises:**
            • Squats (3 sets of 10-15 reps)
            • Push-ups (modified if needed)
            • Planks (hold for 30-60 seconds)
            • Walking (30 minutes daily)
            
            **Frequency:** 3 times per week, with rest days in between
            **Focus on form over intensity** - Quality movements prevent injuries
            """,
            "How to lose weight effectively?": """
            **Science-based approach:**
            1. **Calorie deficit** - Eat 300-500 fewer calories than you burn daily
            2. **High protein** - 1.6-2.2g per kg of body weight to preserve muscle
            3. **Strength training** - Builds muscle which burns more calories at rest
            4. **Cardio** - 150-300 minutes of moderate activity per week
            5. **Sleep** - 7-9 hours nightly for optimal hormone balance
            
            Aim for 0.5-1kg loss per week for sustainable results.
            """,
            "Importance of rest days?": """
            **Rest days are NOT lazy days - they're growth days!**
            
            **Why rest is crucial:**
            • Muscles repair and grow during rest
            • Prevents burnout and overtraining
            • Reduces injury risk
            • Improves performance in next workout
            • Allows nervous system recovery
            
            **Active recovery** (light walking, stretching) is great on rest days!
            """,
            "Best time to workout?": """
            **The best time is when you'll actually do it consistently!**
            
            **Morning benefits:**
            • Boosts metabolism all day
            • Improves mood and energy
            • More consistent (less likely to skip)
            
            **Evening benefits:**
            • Strength peaks in afternoon
            • Body is warmed up from daily activity
            • Can relieve work stress
            
            **Key:** Consistency > Timing
            """,
            "How much protein do I need?": """
            **Daily protein requirements:**
            
            **Sedentary adult:** 0.8g per kg of body weight
            **Active individuals:** 1.2-1.7g per kg
            **Strength athletes:** 1.6-2.2g per kg
            
            **Example for 70kg person:**
            • General fitness: 84-119g daily
            • Muscle building: 112-154g daily
            
            **Spread throughout the day** - 20-40g per meal for optimal absorption
            """
        }
        
        return answers.get(question, "Great question! Consistency and balance are key to fitness success.")
    
    def render_ai_analysis(self):
        """Render AI analysis of user data"""
        st.markdown('<div class="section-header">🔍 AI FITNESS ANALYSIS</div>', unsafe_allow_html=True)
        
        if 'profile_data' not in st.session_state:
            st.warning("Please complete your profile first!")
            return
        
        # Analyze user data
        analysis = self.analyze_user_data()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="stats-card">
                <h4 style="color: #00FF87;">📊 CURRENT STATUS</h4>
                <div style="color: #CCCCCC; margin-top: 1rem;">
                    {analysis['status']}
                </div>
                <div style="color: #00FF87; margin-top: 1.5rem;">
                    ⚡ STRENGTHS
                </div>
                <ul style="color: #999999;">
                    {''.join([f'<li>{s}</li>' for s in analysis['strengths']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stats-card">
                <h4 style="color: #00FF87;">🎯 RECOMMENDATIONS</h4>
                <div style="color: #00D4FF; margin-top: 1rem;">
                    🔥 PRIORITIES
                </div>
                <ul style="color: #999999;">
                    {''.join([f'<li>{p}</li>' for p in analysis['priorities']])}
                </ul>
                <div style="color: #00D4FF; margin-top: 1.5rem;">
                    📈 NEXT STEPS
                </div>
                <ul style="color: #999999;">
                    {''.join([f'<li>{s}</li>' for s in analysis['next_steps']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Generate personalized plan button
        if st.button("🤖 GENERATE PERSONALIZED PLAN", use_container_width=True, type="primary"):
            with st.spinner("AI is creating your personalized fitness plan..."):
                plan = self.generate_personalized_plan()
                
                st.markdown("""
                <div style="background: rgba(0, 255, 135, 0.1); padding: 2rem; border-radius: 15px; 
                            margin-top: 2rem; border: 2px solid #00FF87;">
                    <h3 style="color: #00FF87; text-align: center;">🎯 YOUR PERSONALIZED PLAN</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(plan)
    
    def analyze_user_data(self):
        """Analyze user data and provide insights"""
        if 'profile_data' not in st.session_state:
            return {
                'status': 'Complete your profile for personalized analysis',
                'strengths': ['Ready to start your fitness journey'],
                'priorities': ['Complete profile setup'],
                'next_steps': ['Set up your workout schedule']
            }
        
        profile = st.session_state.profile_data
        goals = profile['goals']
        
        analysis = {
            'status': f"Working toward {goals.get('primary_goal', 'fitness').replace('_', ' ')} goals",
            'strengths': [],
            'priorities': [],
            'next_steps': []
        }
        
        # Analyze based on goals
        primary_goal = goals.get('primary_goal', 'general_fitness')
        
        if primary_goal == 'weight_loss':
            analysis['strengths'].append("Clear weight loss target set")
            analysis['strengths'].append("Specific timeline established")
            analysis['priorities'].append("Create consistent calorie deficit")
            analysis['priorities'].append("Increase daily activity level")
            analysis['next_steps'].append("Log meals daily in Nutrition Hub")
            analysis['next_steps'].append("Start with 3 cardio sessions per week")
        
        elif primary_goal == 'muscle_gain':
            analysis['strengths'].append("Strength-focused goal")
            analysis['strengths'].append("Protein intake awareness")
            analysis['priorities'].append("Progressive overload in workouts")
            analysis['priorities'].append("Adequate protein intake")
            analysis['next_steps'].append("Follow structured strength program")
            analysis['next_steps'].append("Track workout performance")
        
        else:
            analysis['strengths'].append("Holistic approach to fitness")
            analysis['strengths'].append("Balanced goal setting")
            analysis['priorities'].append("Consistency in workouts")
            analysis['priorities'].append("Balanced nutrition")
            analysis['next_steps'].append("Establish regular workout routine")
            analysis['next_steps'].append("Monitor progress weekly")
        
        return analysis
    
    def generate_personalized_plan(self):
        """Generate personalized fitness plan using AI"""
        try:
            context = self.create_user_context()
            
            prompt = f"""{context}

Based on this user profile, create a comprehensive 4-week fitness plan including:

1. Weekly workout schedule (days, types, duration)
2. Nutrition guidelines (calorie target, macronutrient breakdown)
3. Key habits to develop
4. Progress tracking methods
5. Motivation strategies

Make it specific, practical, and achievable. Format with clear sections and bullet points."""

            response = self.client.text_generation(
                prompt,
                max_new_tokens=500,
                temperature=0.7,
                do_sample=True
            )
            
            return response
            
        except:
            return self.get_fallback_plan()
    
    def get_fallback_plan(self):
        """Get fallback plan when AI is unavailable"""
        return """
**4-Week Fitness Foundation Plan**

**🏋️‍♂️ WORKOUT SCHEDULE (3-4 days/week)**
- **Day 1:** Full Body Strength (45 min)
- **Day 2:** Cardio & Core (30 min)
- **Day 3:** Active Recovery (20 min walk + stretching)
- **Day 4:** Repeat Day 1 or try new activity

**🍎 NUTRITION GUIDELINES**
- **Calories:** Maintain slight deficit if weight loss goal, slight surplus if muscle gain
- **Protein:** 1.6-2.2g per kg of body weight daily
- **Hydration:** 8+ glasses of water daily
- **Meals:** 3 main meals + 1-2 snacks

**🔑 KEY HABITS**
1. **Consistency:** Workout at same time daily
2. **Preparation:** Plan meals and workouts weekly
3. **Recovery:** 7-9 hours sleep nightly
4. **Hydration:** Start day with glass of water

**📊 PROGRESS TRACKING**
- Weekly weigh-ins (same time, same scale)
- Workout performance tracking
- Monthly progress photos
- Energy and mood journal

**💪 MOTIVATION STRATEGIES**
- Set weekly mini-goals
- Reward milestones
- Find workout buddy
- Track streaks in app
"""
    
    def render_conversation_history(self):
        """Render conversation history"""
        st.markdown('<div class="section-header">📚 CONVERSATION HISTORY</div>', unsafe_allow_html=True)
        
        if 'ai_conversation' not in st.session_state or not st.session_state.ai_conversation:
            st.info("No conversations yet. Start chatting with your AI Coach!")
            return
        
        for message in st.session_state.ai_conversation:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="background: rgba(0, 255, 135, 0.05); padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 3px solid #00FF87;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #00FF87; font-weight: 600;">You</span>
                        <span style="color: #999999; font-size: 0.8rem;">{message.get('timestamp', '')}</span>
                    </div>
                    <div style="color: white; margin-top: 5px;">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: rgba(0, 212, 255, 0.05); padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 3px solid #00D4FF;">
                    <div style="display: flex; justify-content: space-between;">
                        <span style="color: #00D4FF; font-weight: 600;">AI Coach</span>
                        <span style="color: #999999; font-size: 0.8rem;">{message.get('timestamp', '')}</span>
                    </div>
                    <div style="color: white; margin-top: 5px;">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Export conversation
        if st.button("📥 Export Conversation", use_container_width=True):
            conversation_text = ""
            for message in st.session_state.ai_conversation:
                role = "You" if message['role'] == 'user' else "AI Coach"
                conversation_text += f"{role} ({message.get('timestamp', '')}):\n{message['content']}\n\n"
            
            st.download_button(
                label="Download as Text",
                data=conversation_text,
                file_name=f"ai_coach_conversation_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )