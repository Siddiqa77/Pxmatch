import streamlit as st
import random

# Function to generate a random target color
def generate_target_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

# Function to calculate the match percentage
def calculate_match(target, guess):
    return round(100 - (sum(abs(t - g) for t, g in zip(target, guess)) / 7.65), 2)

# Streamlit page config
st.set_page_config(page_title="PX Match - Color Challenge", page_icon="🎨", layout="wide")

# Title and instructions
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #ffffff;
            background-color: #4A90E2;
            padding: 10px;
            border-radius: 10px;
        }
    </style>
    <div class="title">🎨 PX Match - Color Challenge</div>
    """, 
    unsafe_allow_html=True
)

st.write("### Try to match the target color using the sliders! 🎯")

# Initialize session state
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'target_color' not in st.session_state:
    st.session_state.target_color = generate_target_color()

target_color = st.session_state.target_color

# Responsive layout with color boxes
st.markdown("### 🎯 Target Color vs Your Selected Color")
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 🎯 Target Color")
    st.markdown(
        f'<div style="width:150px; height:150px; background-color:rgb{target_color}; border-radius:10px; border:4px solid black; margin: auto;"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**RGB: {target_color}**")

with col2:
    st.markdown("#### 🎨 Your Selected Color")
    guess_r = st.slider("Red", 0, 255, 127, step=1, key="r")
    guess_g = st.slider("Green", 0, 255, 127, step=1, key="g")
    guess_b = st.slider("Blue", 0, 255, 127, step=1, key="b")
    guess_color = (guess_r, guess_g, guess_b)
    
    st.markdown(
        f'<div style="width:150px; height:150px; background-color:rgb{guess_color}; border-radius:10px; border:4px solid black; margin: auto;"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"**RGB: {guess_color}**")

st.markdown("---")

# Match Button and Score Display
col3, col4 = st.columns([1, 1])

with col3:
    if st.button("🎯 Check Match", use_container_width=True):
        score = calculate_match(target_color, guess_color)
        st.session_state.total_score += score
        st.session_state.attempts += 1
        st.success(f"Match Score: {score}%")

        if score == 100:
            st.balloons()
            st.success("🎉 Hurrah! You won the game!")
            st.markdown(
                """
                <audio autoplay>
                    <source src="https://www.myinstants.com/media/sounds/tadaa.mp3" type="audio/mp3">
                </audio>
                <script>
                    var audio = new Audio('https://www.myinstants.com/media/sounds/hurray.mp3');
                    audio.play();
                </script>
                """,
                unsafe_allow_html=True,
            )
        elif score > 95:
            st.balloons()
            st.success("🔥 Amazing! Almost Perfect Match!")
        elif score > 80:
            st.info("👍 Great job! Very close!")
        elif score > 60:
            st.warning("⚡ Good effort, but try again!")
        else:
            st.error("❌ Too far off! Adjust your colors and retry.")

        # Display final score
        if st.session_state.attempts > 0:
            avg_score = round(st.session_state.total_score / st.session_state.attempts, 2)
            st.info(f"🏆 Final Score: {avg_score}% (Based on {st.session_state.attempts} attempts)")

with col4:
    if st.button("🔄 New Color", use_container_width=True):
        st.session_state.target_color = generate_target_color()
        st.rerun()

st.markdown("---")

# Footer Message
st.markdown(
    """
    <style>
        .footer {
            text-align: center;
            font-size: 16px;
            color: #666;
        }
    </style>
    <div class="footer">Challenge yourself to get as close as possible to the target color! 🎨</div>
    """,
    unsafe_allow_html=True
)
