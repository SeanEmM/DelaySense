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
        opacity: 0.5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("About DelaySense")

st.markdown("""
### What is DelaySense?

**DelaySense** is a machine learning-powered web app that predicts flight delays based on **weather conditions** and flight information. The goal is to help travelers, airport authorities, and airlines make proactive decisions and avoid unexpected delays.

---

### Project Objectives
- Predict the **delay time** of flights based on weather data.
- Use **real-time weather inputs** to provide actionable predictions.
- Create a clean, interactive interface with **Streamlit**.

---

### How it Works
1. **User enters flight and weather data**
2. The input is **scaled and preprocessed**
3. A trained **Gradient Boosting Classifier** model predicts the delay
4. Output is shown instantly

---

### Technologies Used
- **Python** for core logic
- **Streamlit** for the user interface
- **Scikit-learn** for model development
- **Meteostat** for weather data
- **Pandas, NumPy** for data processing
- **SMOTE** for oversampling the imbalanced data

---       

### Datasets Used
- [Flight Dataset](https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-data-2019-2023-v2/data)  
- [Airport Coordinates](https://www.kaggle.com/datasets/vittoriorossi/balanced-flight-cancellation-and-delay-2019-2023)  
- [Weather Data](https://dev.meteostat.net/python/)


---


### Developed By
**Sonal Varghese**  
*CSE Engineer*   
*[Check out my other Projects!](https://github.com/SeanEmM)*

---

### Note
This project was created as part of a data science course. Predictions are based on historical weather-delay correlations and may not reflect all real-world scenarios.

""")