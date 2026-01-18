import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Nutrition Center",
    page_icon="🍎",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .nutrition-header {
        font-size: 2.5rem;
        background: linear-gradient(90deg, #00FF87, #00D4FF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 2rem;
    }
    .food-card {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid #00FF87;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .macro-card {
        background: rgba(0, 20, 10, 0.8);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(0, 255, 135, 0.3);
        text-align: center;
    }
    .main-container {
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for nutrition data
if "nutrition_logs" not in st.session_state:
    st.session_state.nutrition_logs = []
if "favorite_foods" not in st.session_state:
    st.session_state.favorite_foods = []
if "meal_plans" not in st.session_state:
    st.session_state.meal_plans = []

# Food database
FOOD_DATABASE = {
    "Proteins": [
        {"name": "Chicken Breast", "calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
        {"name": "Salmon", "calories": 208, "protein": 22, "carbs": 0, "fat": 13},
        {"name": "Eggs (2 large)", "calories": 155, "protein": 13, "carbs": 1.1, "fat": 11},
        {"name": "Greek Yogurt (1 cup)", "calories": 59, "protein": 10, "carbs": 3.6, "fat": 0.4},
        {"name": "Tofu (100g)", "calories": 76, "protein": 8, "carbs": 1.9, "fat": 4.8},
        {"name": "Lean Beef (100g)", "calories": 250, "protein": 26, "carbs": 0, "fat": 15},
    ],
    "Carbohydrates": [
        {"name": "Brown Rice (1 cup)", "calories": 216, "protein": 5, "carbs": 45, "fat": 1.8},
        {"name": "Quinoa (1 cup)", "calories": 222, "protein": 8, "carbs": 39, "fat": 3.6},
        {"name": "Sweet Potato (medium)", "calories": 103, "protein": 2, "carbs": 24, "fat": 0.2},
        {"name": "Oatmeal (1 cup)", "calories": 158, "protein": 6, "carbs": 27, "fat": 3.2},
        {"name": "Whole Wheat Bread (slice)", "calories": 81, "protein": 4, "carbs": 14, "fat": 1},
    ],
    "Vegetables": [
        {"name": "Broccoli (1 cup)", "calories": 31, "protein": 2.5, "carbs": 6, "fat": 0.4},
        {"name": "Spinach (1 cup)", "calories": 7, "protein": 0.9, "carbs": 1, "fat": 0.1},
        {"name": "Bell Peppers (1 cup)", "calories": 31, "protein": 1, "carbs": 7, "fat": 0.3},
        {"name": "Carrots (1 cup)", "calories": 52, "protein": 1, "carbs": 12, "fat": 0.3},
    ],
    "Fruits": [
        {"name": "Apple (medium)", "calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3},
        {"name": "Banana (medium)", "calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4},
        {"name": "Berries (1 cup)", "calories": 85, "protein": 1, "carbs": 21, "fat": 0.5},
        {"name": "Orange (medium)", "calories": 62, "protein": 1.2, "carbs": 15, "fat": 0.2},
    ]
}

def calculate_tdee():
    """Calculate Total Daily Energy Expenditure"""
    if "profile_data" not in st.session_state:
        return 2000  # Default
    
    profile = st.session_state.profile_data
    weight = profile['personal']['weight']
    height = profile['personal']['height']
    age = profile['personal']['age']
    
    # Get activity level
    activity_level = profile.get('lifestyle', {}).get('activity_level', 'Moderate')
    
    # BMR calculation (Mifflin-St Jeor)
    gender = profile['personal']['gender']
    if gender == 'Male':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Activity multipliers
    multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }
    
    return int(bmr * multipliers.get(activity_level, 1.55))

def calculate_daily_goals():
    """Calculate daily nutrition goals"""
    tdee = calculate_tdee()
    
    if "profile_data" not in st.session_state:
        return {
            "calories": 2000,
            "protein": 80,
            "carbs": 250,
            "fat": 67
        }
    
    profile = st.session_state.profile_data
    weight = profile['personal']['weight']
    goal = profile['goals'].get('primary_goal', 'general_fitness')
    
    # Adjust calories based on goal
    if goal == 'weight_loss':
        calories = tdee - 500
    elif goal == 'muscle_gain':
        calories = tdee + 300
    else:
        calories = tdee
    
    # Macronutrient targets
    protein = int(weight * 2.2)  # 2.2g per kg for active individuals
    fat = int((calories * 0.25) / 9)  # 25% from fat
    carbs = int((calories - (protein * 4) - (fat * 9)) / 4)
    
    return {
        "calories": calories,
        "protein": protein,
        "carbs": carbs,
        "fat": fat
    }

def calculate_protein_needs(weight, activity_level):
    """Calculate protein needs based on weight and activity"""
    # Protein multipliers
    multipliers = {
        "Sedentary": 0.8,
        "Light": 1.0,
        "Moderate": 1.3,
        "Active": 1.6,
        "Very Active": 2.0
    }
    
    return weight * multipliers.get(activity_level, 1.3)

# Main App
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="nutrition-header">🍎 NUTRITION CENTER</h1>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard", 
    "📝 Food Logger", 
    "🔍 Calorie Checker", 
    "📋 Meal Plans", 
    "📈 Progress"
])

# Tab 1: Dashboard
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎯 Today's Nutrition Goals")
        
        goals = calculate_daily_goals()
        
        # Calculate today's intake
        today = datetime.now().strftime("%Y-%m-%d")
        today_logs = [log for log in st.session_state.nutrition_logs if log.get("date") == today]
        
        today_calories = sum(log.get("calories", 0) for log in today_logs)
        today_protein = sum(log.get("protein", 0) for log in today_logs)
        today_carbs = sum(log.get("carbs", 0) for log in today_logs)
        today_fat = sum(log.get("fat", 0) for log in today_logs)
        
        # Display progress bars
        metrics = ["Calories", "Protein", "Carbs", "Fat"]
        current = [today_calories, today_protein, today_carbs, today_fat]
        targets = [goals["calories"], goals["protein"], goals["carbs"], goals["fat"]]
        icons = ["🔥", "🥚", "🍞", "🥑"]
        
        for i in range(4):
            percent = min((current[i] / targets[i]) * 100, 100) if targets[i] > 0 else 0
            
            st.markdown(f"""
            <div style="margin: 1.5rem 0;">
                <div style="display: flex; justify-content: space-between; color: #CCCCCC;">
                    <span>{icons[i]} {metrics[i]}</span>
                    <span>{current[i]:.0f}/{targets[i]:.0f}{'g' if i>0 else 'cal'}</span>
                </div>
                <div style="background: rgba(255, 255, 255, 0.1); height: 15px; border-radius: 8px;">
                    <div style="background: linear-gradient(90deg, #00FF87, #00D4FF); 
                               width: {percent}%; height: 100%; border-radius: 8px;"></div>
                </div>
                <div style="color: #999999; text-align: center; font-size: 0.9rem;">
                    {percent:.0f}% of daily goal
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("💡 Quick Tips")
        
        tips = [
            "🍽️ Eat protein with every meal for muscle repair",
            "💧 Drink water before meals to reduce appetite",
            "🥦 Fill half your plate with vegetables",
            "⏰ Don't skip breakfast - it kickstarts metabolism",
            "🧘 Eat mindfully, without distractions",
            "🥑 Include healthy fats for hormone balance"
        ]
        
        for tip in tips:
            st.markdown(f"""
            <div style="background: rgba(0, 255, 135, 0.1); padding: 1rem; border-radius: 10px; 
                        margin: 0.5rem 0; border-left: 4px solid #00FF87;">
                <div style="color: #CCCCCC;">{tip}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick add buttons
        st.subheader("⚡ Quick Add")
        col1, col2, col3 = st.columns(3)
        
        quick_foods = [
            {"name": "Apple", "calories": 95, "protein": 0.5, "carbs": 25, "fat": 0.3},
            {"name": "Protein Shake", "calories": 120, "protein": 25, "carbs": 3, "fat": 1},
            {"name": "Greek Yogurt", "calories": 100, "protein": 17, "carbs": 6, "fat": 0.4}
        ]
        
        for i, food in enumerate(quick_foods):
            with [col1, col2, col3][i]:
                if st.button(f"➕ {food['name']}", use_container_width=True):
                    food_log = {
                        "date": today,
                        "meal": "Snack",
                        "food": food["name"],
                        "calories": food["calories"],
                        "protein": food["protein"],
                        "carbs": food["carbs"],
                        "fat": food["fat"],
                        "time": datetime.now().strftime("%H:%M")
                    }
                    st.session_state.nutrition_logs.append(food_log)
                    st.success(f"Added {food['name']}!")
                    st.rerun()

# Tab 2: Food Logger
with tab2:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🍽️ Log Your Meal")
        
        with st.form("food_log_form"):
            meal_type = st.selectbox("Meal Type", 
                                    ["Breakfast", "Lunch", "Dinner", "Snack", "Pre-workout", "Post-workout"])
            
            food_name = st.text_input("Food Name", placeholder="e.g., Grilled Chicken Salad")
            
            col_cal, col_prot = st.columns(2)
            with col_cal:
                calories = st.number_input("Calories", min_value=0, max_value=2000, value=300)
            with col_prot:
                protein = st.number_input("Protein (g)", min_value=0.0, max_value=200.0, value=25.0, step=0.1)
            
            col_carb, col_fat = st.columns(2)
            with col_carb:
                carbs = st.number_input("Carbs (g)", min_value=0.0, max_value=200.0, value=30.0, step=0.1)
            with col_fat:
                fat = st.number_input("Fat (g)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
            
            notes = st.text_area("Notes", placeholder="Any additional notes...")
            
            submitted = st.form_submit_button("💾 Log Meal", type="primary")
            
            if submitted:
                if food_name:
                    food_log = {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "meal": meal_type,
                        "food": food_name,
                        "calories": calories,
                        "protein": protein,
                        "carbs": carbs,
                        "fat": fat,
                        "notes": notes,
                        "time": datetime.now().strftime("%H:%M")
                    }
                    st.session_state.nutrition_logs.append(food_log)
                    st.success(f"✅ {meal_type} logged successfully!")
                    st.balloons()
                else:
                    st.warning("Please enter a food name")
    
    with col2:
        st.subheader("📚 Food Database")
        
        category = st.selectbox("Browse Foods", list(FOOD_DATABASE.keys()))
        
        for food in FOOD_DATABASE[category]:
            with st.expander(f"{food['name']} - {food['calories']} cal"):
                st.markdown(f"""
                <div style="color: #CCCCCC;">
                    <strong>Nutrition per serving:</strong><br>
                    🥚 Protein: {food['protein']}g<br>
                    🍞 Carbs: {food['carbs']}g<br>
                    🥑 Fat: {food['fat']}g
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Add to Today", key=f"add_{food['name']}"):
                    food_log = {
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "meal": "From Database",
                        "food": food["name"],
                        "calories": food["calories"],
                        "protein": food["protein"],
                        "carbs": food["carbs"],
                        "fat": food["fat"],
                        "time": datetime.now().strftime("%H:%M")
                    }
                    st.session_state.nutrition_logs.append(food_log)
                    st.success(f"Added {food['name']}!")
                    st.rerun()

# Tab 3: Calorie Checker
with tab3:
    st.subheader("🔍 Calorie & Protein Checker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="food-card">
            <h4 style="color: #00FF87;">🧮 Calculate Nutrition</h4>
            <p style="color: #CCCCCC;">Check calories and macros for any food</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Food calculator
        with st.form("calculator_form"):
            food_input = st.text_input("Enter Food Item", placeholder="e.g., chicken breast, rice, apple")
            quantity = st.number_input("Quantity (grams)", min_value=1, max_value=1000, value=100)
            
            if st.form_submit_button("Calculate"):
                if food_input:
                    # Simple calculation based on common foods
                    food_lower = food_input.lower()
                    
                    # Estimate based on food type
                    if "chicken" in food_lower:
                        calories = int(quantity * 1.65)
                        protein = int(quantity * 0.31)
                        carbs = int(quantity * 0)
                        fat = int(quantity * 0.036)
                    elif "rice" in food_lower or "pasta" in food_lower:
                        calories = int(quantity * 1.3)
                        protein = int(quantity * 0.03)
                        carbs = int(quantity * 0.28)
                        fat = int(quantity * 0.003)
                    elif "apple" in food_lower or "fruit" in food_lower:
                        calories = int(quantity * 0.52)
                        protein = int(quantity * 0.003)
                        carbs = int(quantity * 0.14)
                        fat = int(quantity * 0.002)
                    else:
                        # Default estimates
                        calories = int(quantity * 1.5)
                        protein = int(quantity * 0.1)
                        carbs = int(quantity * 0.2)
                        fat = int(quantity * 0.05)
                    
                    st.markdown(f"""
                    <div style="background: rgba(0, 255, 135, 0.1); padding: 1.5rem; border-radius: 15px; margin-top: 1rem;">
                        <h4 style="color: #00FF87;">📊 Nutrition for {quantity}g of {food_input}</h4>
                        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem;">
                            <div class="macro-card">
                                <div style="color: white; font-size: 1.5rem;">🔥</div>
                                <div style="color: white; font-size: 1.2rem;">{calories}</div>
                                <div style="color: #CCCCCC;">Calories</div>
                            </div>
                            <div class="macro-card">
                                <div style="color: white; font-size: 1.5rem;">🥚</div>
                                <div style="color: white; font-size: 1.2rem;">{protein}g</div>
                                <div style="color: #CCCCCC;">Protein</div>
                            </div>
                            <div class="macro-card">
                                <div style="color: white; font-size: 1.5rem;">🍞</div>
                                <div style="color: white; font-size: 1.2rem;">{carbs}g</div>
                                <div style="color: #CCCCCC;">Carbs</div>
                            </div>
                            <div class="macro-card">
                                <div style="color: white; font-size: 1.5rem;">🥑</div>
                                <div style="color: white; font-size: 1.2rem;">{fat}g</div>
                                <div style="color: #CCCCCC;">Fat</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="food-card">
            <h4 style="color: #00FF87;">📊 Common Food Nutrition</h4>
            <p style="color: #CCCCCC;">Reference values per 100g</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create reference table
        reference_foods = [
            ["Chicken Breast", 165, 31, 0, 3.6],
            ["Salmon", 208, 22, 0, 13],
            ["Brown Rice", 112, 2.6, 23, 0.9],
            ["Broccoli", 34, 2.8, 7, 0.4],
            ["Apple", 52, 0.3, 14, 0.2],
            ["Egg", 155, 13, 1.1, 11]
        ]
        
        df = pd.DataFrame(reference_foods, columns=["Food", "Calories", "Protein (g)", "Carbs (g)", "Fat (g)"])
        st.dataframe(df.style.background_gradient(subset=["Calories", "Protein (g)"], cmap="Greens"), 
                    use_container_width=True)
        
        # Protein calculator
        st.subheader("🥚 Protein Needs Calculator")
        
        weight = st.number_input("Your Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, key="protein_weight")
        activity = st.select_slider("Activity Level", 
                                   ["Sedentary", "Light", "Moderate", "Active", "Very Active"],
                                   key="protein_activity")
        
        protein_needs = calculate_protein_needs(weight, activity)
        
        st.metric("Daily Protein Needs", f"{protein_needs:.1f}g")

# Tab 4: Meal Plans
with tab4:
    st.subheader("📋 Personalized Meal Plans")
    
    if "profile_data" not in st.session_state:
        st.warning("Please complete your profile first!")
    else:
        profile = st.session_state.profile_data
        goals = calculate_daily_goals()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="food-card">
                <h4 style="color: #00FF87;">🎯 Your Daily Targets</h4>
                <div style="color: #CCCCCC; margin-top: 1rem;">
                    <strong>Calories:</strong> {goals['calories']}<br>
                    <strong>Protein:</strong> {goals['protein']}g<br>
                    <strong>Carbs:</strong> {goals['carbs']}g<br>
                    <strong>Fat:</strong> {goals['fat']}g
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Generate meal plan button
            if st.button("🤖 Generate AI Meal Plan", use_container_width=True, type="primary"):
                with st.spinner("Creating personalized meal plan..."):
                    # Create sample meal plan
                    meal_plan = {
                        "breakfast": {
                            "name": "Protein Oatmeal",
                            "calories": 350,
                            "protein": 25,
                            "carbs": 45,
                            "fat": 8,
                            "ingredients": ["Oats", "Protein powder", "Berries", "Almonds"]
                        },
                        "lunch": {
                            "name": "Chicken & Quinoa Bowl",
                            "calories": 450,
                            "protein": 35,
                            "carbs": 40,
                            "fat": 15,
                            "ingredients": ["Chicken breast", "Quinoa", "Mixed vegetables", "Olive oil"]
                        },
                        "dinner": {
                            "name": "Salmon with Sweet Potato",
                            "calories": 500,
                            "protein": 30,
                            "carbs": 35,
                            "fat": 20,
                            "ingredients": ["Salmon", "Sweet potato", "Broccoli", "Lemon"]
                        },
                        "snacks": {
                            "name": "Greek Yogurt & Fruits",
                            "calories": 200,
                            "protein": 15,
                            "carbs": 25,
                            "fat": 5,
                            "ingredients": ["Greek yogurt", "Mixed berries", "Honey"]
                        }
                    }
                    
                    st.session_state.meal_plans.append({
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "plan": meal_plan
                    })
                    
                    st.success("✅ Meal plan generated!")
        
        with col2:
            if st.session_state.meal_plans:
                latest_plan = st.session_state.meal_plans[-1]["plan"]
                
                st.markdown("""
                <div class="food-card">
                    <h4 style="color: #00FF87;">🍽️ Today's Meal Plan</h4>
                </div>
                """, unsafe_allow_html=True)
                
                for meal, details in latest_plan.items():
                    with st.expander(f"{meal.title()} - {details['calories']} calories", expanded=True):
                        st.markdown(f"""
                        <div style="color: #CCCCCC;">
                            <strong>Ingredients:</strong> {', '.join(details['ingredients'])}<br><br>
                            <strong>Nutrition:</strong><br>
                            🥚 Protein: {details['protein']}g<br>
                            🍞 Carbs: {details['carbs']}g<br>
                            🥑 Fat: {details['fat']}g
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button(f"✅ Log {meal.title()}", key=f"log_{meal}"):
                            food_log = {
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "meal": meal.title(),
                                "food": details["name"],
                                "calories": details["calories"],
                                "protein": details["protein"],
                                "carbs": details["carbs"],
                                "fat": details["fat"],
                                "time": "Planned"
                            }
                            st.session_state.nutrition_logs.append(food_log)
                            st.success(f"Logged {details['name']}!")
                            st.rerun()
            else:
                st.info("Generate a meal plan to get started!")

# Tab 5: Progress
with tab5:
    st.subheader("📈 Nutrition Progress")
    
    if not st.session_state.nutrition_logs:
        st.info("No nutrition data yet. Start logging your meals!")
    else:
        # Convert logs to DataFrame
        df = pd.DataFrame(st.session_state.nutrition_logs)
        df["date"] = pd.to_datetime(df["date"])
        
        # Weekly summary
        st.markdown("### 📊 Weekly Summary")
        
        # Get last 7 days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        weekly_data = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
        
        if not weekly_data.empty:
            # Group by date
            daily_summary = weekly_data.groupby("date").agg({
                "calories": "sum",
                "protein": "sum",
                "carbs": "sum"
            }).reset_index()
            
            # Create charts
            col1, col2 = st.columns(2)
            
            with col1:
                # Calories chart
                fig_cal = go.Figure()
                fig_cal.add_trace(go.Bar(
                    x=daily_summary["date"].dt.strftime("%a"),
                    y=daily_summary["calories"],
                    name="Calories",
                    marker_color="#00FF87"
                ))
                
                # Add target line
                goals = calculate_daily_goals()
                fig_cal.add_hline(y=goals["calories"], line_dash="dash", 
                                 line_color="#FFA500", annotation_text="Target")
                
                fig_cal.update_layout(
                    title="Daily Calories (Last 7 Days)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                    xaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
                )
                
                st.plotly_chart(fig_cal, use_container_width=True)
            
            with col2:
                # Macronutrient pie chart
                total_protein = weekly_data["protein"].sum()
                total_carbs = weekly_data["carbs"].sum()
                total_fat = weekly_data["fat"].sum() if "fat" in weekly_data.columns else 0
                
                fig_macro = go.Figure(data=[go.Pie(
                    labels=["Protein", "Carbs", "Fat"],
                    values=[total_protein, total_carbs, total_fat],
                    hole=0.3,
                    marker_colors=["#00FF87", "#00D4FF", "#FFA500"]
                )])
                
                fig_macro.update_layout(
                    title="Macronutrient Distribution",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white")
                )
                
                st.plotly_chart(fig_macro, use_container_width=True)
        
        # Recent meals
        st.markdown("### 📋 Recent Meals")
        
        recent_logs = st.session_state.nutrition_logs[-10:][::-1]  # Last 10, newest first
        
        for log in recent_logs:
            with st.container():
                st.markdown(f"""
                <div style="background: rgba(0, 255, 135, 0.05); padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="color: #00FF87; font-weight: 600;">{log.get('meal', 'Meal')}: {log.get('food', 'Food')}</div>
                            <div style="color: #CCCCCC; font-size: 0.9rem;">
                                {log.get('date', '')} | {log.get('time', '')}
                            </div>
                        </div>
                        <div style="color: #00FF87; font-weight: 600;">{log.get('calories', 0)} cal</div>
                    </div>
                    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;">
                        <div style="text-align: center;">
                            <div style="color: white;">🥚</div>
                            <div style="color: #CCCCCC; font-size: 0.9rem;">{log.get('protein', 0)}g</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: white;">🍞</div>
                            <div style="color: #CCCCCC; font-size: 0.9rem;">{log.get('carbs', 0)}g</div>
                        </div>
                        <div style="text-align: center;">
                            <div style="color: white;">🥑</div>
                            <div style="color: #CCCCCC; font-size: 0.9rem;">{log.get('fat', 0)}g</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)