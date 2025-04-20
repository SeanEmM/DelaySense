import streamlit as st

st.markdown(
    """
    <style>
    .stApp {
        background: none;
    }

    body::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: url('https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMXZ6MjhodGR6b2Y1ZjI4dmhpODNoMzBtcGR0bnZwbGcwczFlY3Q2dSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/WoG9QQfmzLO3Ri9mF5/giphy.gif') no-repeat center center fixed;
        background-size: cover;
        opacity: 0.2;
    }
    </style>
    """,
    unsafe_allow_html=True
)



st.title("🚀 DelaySense: Flight Delay Prediction System")
st.subheader("Your smart assistant for forecasting flight delays based on weather conditions")


st.markdown("---")


st.markdown("""
            DelaySense is a machine learning-powered web application that predicts flight delays using real-time weather data. 
With accurate insights and a user-friendly interface, DelaySense aims to assist travelers and airlines in making informed decisions.

- 🧠 Built with: Python, Streamlit, scikit-learn
- 🌤️ Real-time weather data powered by Meteostat
- 📊 Machine Learning Model: Gradient Boosting Classifier
""")

if st.button("Go to Prediction Tool"):
    st.switch_page("pages/predict.py")  

if st.button("Click to learn more about this project"):
    st.switch_page("pages/about.py")
# Footer
st.markdown("---")
st.caption("Developed by Sonal | © 2025 DelaySense")

