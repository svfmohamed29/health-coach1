import streamlit as st


# -----------------------------
# Agent 1: Monitoring Agent
# -----------------------------
def monitoring_agent(sleep_hours, water_intake, stress_level, movement_goal):
    summary = []

    if sleep_hours < 6:
        summary.append("low sleep")
    elif sleep_hours < 8:
        summary.append("moderate sleep")
    else:
        summary.append("good sleep")

    if water_intake < 5:
        summary.append("low hydration")
    else:
        summary.append("good hydration")

    if stress_level >= 4:
        summary.append("high stress")
    elif stress_level == 3:
        summary.append("moderate stress")
    else:
        summary.append("low stress")

    summary.append(f"movement goal: {movement_goal.lower()}")
    return summary


# -----------------------------
# Agent 2: Planning Agent
# -----------------------------
def planning_agent(name, summary):
    plan = []
    timeline = []

    if "low sleep" in summary:
        plan.append("Try getting more sleep tonight.")
        timeline.append(("Evening", "Start winding down earlier and aim for more sleep tonight."))
    elif "moderate sleep" in summary:
        plan.append("Your sleep is fair, but improving consistency may help.")
        timeline.append(("Evening", "Try to keep a more consistent bedtime tonight."))
    else:
        plan.append("Great job maintaining good sleep.")
        timeline.append(("Evening", "Keep following your current sleep routine."))

    if "low hydration" in summary:
        plan.append("Try drinking more water throughout the day.")
        timeline.append(("Morning", "Start your day with a glass of water."))
        timeline.append(("Afternoon", "Drink water again during the middle of the day."))
    else:
        plan.append("Your hydration looks good.")
        timeline.append(("Morning", "Continue your current hydration routine."))

    if "high stress" in summary:
        plan.append("Take a short relaxation or breathing break today.")
        timeline.append(("Afternoon", "Take a 5-minute breathing or relaxation break."))
    elif "moderate stress" in summary:
        plan.append("A short wellness break may help manage stress today.")
        timeline.append(("Afternoon", "Take a short break to reset during the day."))
    else:
        plan.append("Your stress level seems manageable.")
        timeline.append(("Afternoon", "Keep a balanced pace and maintain your routine."))

    if "movement goal: low" in summary:
        plan.append("Take a short walk or do light stretching today.")
        timeline.append(("Evening", "Take a short walk or stretch for a few minutes."))
    elif "movement goal: medium" in summary:
        plan.append("Try moderate physical activity today.")
        timeline.append(("Evening", "Fit in a moderate walk or short workout today."))
    else:
        plan.append("Aim for higher activity, but keep it realistic and balanced.")
        timeline.append(("Evening", "Stay active, but make sure your routine feels manageable."))

    return {
        "name": name,
        "plan": plan,
        "timeline": timeline
    }


# -----------------------------
# Agent 3: Safety / Critic Agent
# -----------------------------
def safety_agent(plan_data):
    safe_plan = []
    safe_timeline = []

    for item in plan_data["plan"]:
        lowered = item.lower()
        if "diagnose" in lowered or "treatment" in lowered or "prescription" in lowered:
            continue
        safe_plan.append(item)

    for time_block, action in plan_data["timeline"]:
        lowered = action.lower()
        if "diagnose" in lowered or "treatment" in lowered or "prescription" in lowered:
            continue
        safe_timeline.append((time_block, action))

    return {
        "name": plan_data["name"],
        "plan": safe_plan,
        "timeline": safe_timeline,
        "safety_note": "This wellness plan is for general support only and does not provide medical advice."
    }


# -----------------------------
# Helper: Wellness Score
# -----------------------------
def calculate_wellness_score(sleep_hours, water_intake, stress_level, movement_goal):
    score = 0

    if sleep_hours >= 8:
        score += 30
    elif sleep_hours >= 6:
        score += 20
    else:
        score += 10

    if water_intake >= 6:
        score += 25
    elif water_intake >= 4:
        score += 15
    else:
        score += 8

    if stress_level <= 2:
        score += 25
    elif stress_level == 3:
        score += 18
    else:
        score += 10

    if movement_goal == "Low":
        score += 10
    elif movement_goal == "Medium":
        score += 15
    else:
        score += 20

    return min(score, 100)


# -----------------------------
# Streamlit Front-End
# -----------------------------
st.set_page_config(page_title="AI Health Routine Coach", page_icon="🌿", layout="centered")

st.title("AI Health Routine Coach")
st.write("Enter your daily wellness information to receive a personalized wellness plan.")

name = st.text_input("Name")

sleep_hours = st.number_input(
    "Hours of sleep last night",
    min_value=0.0,
    max_value=16.0,
    step=0.5
)

water_intake = st.number_input(
    "Cups of water today",
    min_value=0,
    max_value=20
)

stress_level = st.slider("Stress level", 1, 5)

movement_goal = st.selectbox(
    "Movement goal",
    ["Low", "Medium", "High"]
)

if st.button("Generate Wellness Plan"):
    monitored_data = monitoring_agent(
        sleep_hours,
        water_intake,
        stress_level,
        movement_goal
    )

    planned_data = planning_agent(name, monitored_data)
    final_data = safety_agent(planned_data)
    wellness_score = calculate_wellness_score(
        sleep_hours,
        water_intake,
        stress_level,
        movement_goal
    )

    st.subheader("Wellness Snapshot")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Wellness Score", f"{wellness_score}/100")
    with col2:
        if stress_level >= 4:
            st.error("Daily Status: High Stress")
        elif stress_level == 3:
            st.warning("Daily Status: Moderate Stress")
        else:
            st.success("Daily Status: Balanced")

    st.progress(wellness_score / 100)

    st.subheader("Your Wellness Plan")
    paragraph = f"{final_data['name']}, based on your inputs, " + " ".join(final_data["plan"])
    st.write(paragraph)

    st.subheader("Today's Wellness Timeline")
    for time_block, action in final_data["timeline"]:
        st.markdown(f"**{time_block}:** {action}")

    if wellness_score >= 80:
        st.success("You are doing well today. Keep maintaining these healthy habits.")
    elif wellness_score >= 60:
        st.info("You have a solid foundation today, with a few areas to improve.")
    else:
        st.warning("Your wellness plan focuses on improving the basics first today.")

    st.caption(final_data["safety_note"])
