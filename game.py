import streamlit as st
import random
import streamlit.components.v1 as components

def generate_target_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def calculate_match(target, guess):
    return round(100 - (sum(abs(t - g) for t, g in zip(target, guess)) / 7.65), 2)

st.set_page_config(page_title="PX Match - Color Challenge", page_icon="🎨", layout="wide")
st.title("🎨 PX Match - Color Challenge")
st.markdown("Try to match the target color using the sliders! 🎯")

# Initialize session state for score if not present
if 'total_score' not in st.session_state:
    st.session_state.total_score = 0
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

# Generate a target color
if 'target_color' not in st.session_state:
    st.session_state.target_color = generate_target_color()

target_color = st.session_state.target_color

# Display the target color with a styled box
st.markdown(
    f'<div style="width:120px; height:120px; background-color:rgb{target_color}; border-radius:10px; border:4px solid black; margin: auto;"></div>',
    unsafe_allow_html=True,
)
st.markdown(f"### Target Color: RGB {target_color}")

st.markdown("---")

# Responsive layout for better UI
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎨 Adjust Your Color")
    guess_r = st.slider("Red", 0, 255, 127, step=1, key="r", format="%d")
    guess_g = st.slider("Green", 0, 255, 127, step=1, key="g", format="%d")
    guess_b = st.slider("Blue", 0, 255, 127, step=1, key="b", format="%d")
    guess_color = (guess_r, guess_g, guess_b)

with col2:
    st.subheader("🎨 Your Selected Color")
    st.markdown(
        f'<div style="width:120px; height:120px; background-color:rgb{guess_color}; border-radius:10px; border:4px solid black; margin: auto;"></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f"### Selected Color: RGB {guess_color}")

st.markdown("---")

# Buttons and match calculation
col3, col4 = st.columns([1, 1])

with col3:
    if st.button("Check Match 🎯", use_container_width=True):
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
            st.success("🎉 Amazing! Perfect Match!")
        elif score > 80:
            st.info("🔥 Great job! Very close!")
        elif score > 60:
            st.warning("⚡ Good effort, but try again!")
        else:
            st.error("❌ Too far off! Adjust your colors and retry.")

        # Display final score
        if st.session_state.attempts > 0:
            avg_score = round(st.session_state.total_score / st.session_state.attempts, 2)
            st.info(f"🏆 Final Score: {avg_score}% (Based on {st.session_state.attempts} attempts)")

with col4:
    if st.button("New Color 🔄", use_container_width=True):
        st.session_state.target_color = generate_target_color()
        st.rerun()

st.markdown("---")
st.info("Challenge yourself to get as close as possible to the target color! 🎨")
