# Weather-Based Flight Delay Classification – DelaySense

## Overview

Flight delays are a major challenge in the aviation industry, affecting passengers, airline operations, and airport logistics. Weather conditions are a key contributor to these delays, yet they are often underutilized in predictive models.

**DelaySense** is a machine learning project that classifies flight delays into multiple categories using historical flight and weather data. It leverages weather insights to help airlines and airports anticipate disruptions and enhance operational planning.

---

## Why Predict Flight Delays?

Predicting delays allows for:

- Proactive decision-making for airlines and airports  
- Better resource allocation  
- Improved passenger experience with timely notifications  
- Reduced operational inefficiencies  

---

## Data Description

The dataset was sourced from a public repository with over **3 million rows**, out of which **750,000 rows** were used after filtering and cleaning. Real-time weather data was added using the **Meteostat API**.

### Flight Data Columns:

- `FL_DATE`: Date of the flight  
- `OP_UNIQUE_CARRIER`: Airline carrier code  
- `ORIGIN`, `DEST`: Departure and arrival airport codes  
- `DEP_TIME`, `ARR_TIME`: Actual departure and arrival times  
- `CRS_DEP_TIME`, `CRS_ARR_TIME`: Scheduled departure and arrival times  
- `DELAY_DUE_WEATHER`: Delay in minutes due to weather (used to classify)

### Weather Data Columns:

- `temperature`: Air temperature in °C  
- `wind_speed`: Wind speed in km/h  
- `humidity`: Relative humidity percentage  
- `precipitation`: Precipitation in mm  
- `visibility`: Visibility in km  
- `conditions`: Weather condition (e.g., clear, fog, rain)  

---

## Classification Labels

The continuous weather delay values were converted into categorical delay classes:

```python
conditions = [
    (df1['DELAY_DUE_WEATHER'] <= 30),
    (df1['DELAY_DUE_WEATHER'] > 30) & (df1['DELAY_DUE_WEATHER'] <= 120),
    (df1['DELAY_DUE_WEATHER'] > 120) & (df1['DELAY_DUE_WEATHER'] <= 600),
    (df1['DELAY_DUE_WEATHER'] > 600)
]
```
### Resulting classes:
- On-Time
- Minor Delay
- Moderate Delay
- Severe Delay
 

### Additional Preprocessing Steps:

- Combined flight and weather data based on timestamp and location  
- Converted date and time columns to datetime format  
- Created derived features like hour of the day, day of the week  

---

## Model & Performance

- **Model Used**: GradientBoostingClassifier
- **Data Preprocessing**:
  - Combined flight and weather data by timestamp and location
  - Converted time columns to datetime
  - Engineered features like `hour`, `day_of_week`, etc.
- **Imbalance Handling**: Used **SMOTE** to balance delay class distribution
- **Accuracy Achieved**: **72%**

---

## Technologies Used

- **Python** (Pandas, NumPy, Scikit-learn)  
- **Machine Learning Models** (Gradient Boosting Regressor)  
- **Imbalanced-learn** (SMOTE for oversampling)  
- **Meteostat API** (for real-time weather data)  
- **Matplotlib & Seaborn** (for data visualization)  
- **Jupyter Notebook** (for model development)  
- **Streamlit** (for dashboard)

---

## Project Challenges

- **Real-time Data Limitations**: Weather data collection for multiple airports and timestamps was time-intensive.  
- **Data Imbalance**: Majority of flights had minimal or no delay, so SMOTE was used to balance the regression target.  

---

## Future Improvements

- Increase time span of data collection 
- Include more features such as aircraft type, route distance, or airline reputation  
- Try deep learning models or hybrid ensembles for improved accuracy  
