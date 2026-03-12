import streamlit as st

st.title("AI Health Routine Coach")

st.write("Enter your daily wellness information to receive a personalized wellness plan.")

name = st.text_input("Name")

sleep_hours = st.number_input("Hours of sleep last night", min_value=0.0, max_value=16.0, step=0.5)

water_intake = st.number_input("Cups of water today", min_value=0, max_value=20)

stress_level = st.slider("Stress level", 1, 5)

movement_goal = st.selectbox(
    "Movement goal",
    ["Low", "Medium", "High"]
)

if st.button("Generate Wellness Plan"):

    response = []

    if sleep_hours < 6:
        response.append("Try getting more sleep tonight.")
    elif sleep_hours < 8:
        response.append("Your sleep is okay but could improve.")
    else:
        response.append("Great job maintaining good sleep.")

    if water_intake < 5:
        response.append("Try drinking more water today.")
    else:
        response.append("Your hydration looks good.")

    if stress_level >= 4:
        response.append("Take a short relaxation break today.")
    else:
        response.append("Your stress level seems manageable.")

    if movement_goal == "Low":
        response.append("Take a short walk today.")
    elif movement_goal == "Medium":
        response.append("Try moderate physical activity.")
    else:
        response.append("Make sure your activity level stays balanced.")

    st.subheader("Your Wellness Plan")

    st.write(f"{name}, here are your suggestions:")

    for r in response:
        st.write("• " + r)
