import streamlit as st
import pickle
from PIL import Image
from meteostat import Hourly, Point
from datetime import datetime as dt, timedelta
import numpy as np
import warnings


warnings.simplefilter(action='ignore', category=Warning)
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

def display_result(prediction_text, status):
    color_map = {
        "On Time": "#28a745",         # Green
        "Minor Delay": "#ffc107",     # Yellow
        "Major Delay": "#dc3545",     # Red
    }

    color = color_map.get(status, "#6c757d")  # Fallback: grey

    st.markdown(f"""
        <div style="padding: 20px;
                    background-color: {color};
                    border-radius: 12px;
                    text-align: center;
                    font-size: 26px;
                    font-weight: bold;
                    color: white;
                    margin-top: 25px;">
            ✈️ {prediction_text} EXPECTED!
        </div>
    """, unsafe_allow_html=True)

def convert_time(date, time_str):
    time_str = str(time_str).zfill(4)
    return dt.combine(date, dt.strptime(time_str, "%H%M").time())

def get_weather(lat, lon, time):
    location = Point(lat, lon)
    weather = Hourly(location, time, time + timedelta(hours=1))
    data = weather.fetch()
    print(data)
    data = data.fillna(0)
    return data.iloc[0].to_dict() if not data.empty else {}

def main():
    st.title(':red[Enter Flight Details]')


    location = {"Hartsfield–Jackson Atlanta International Airport (ATL)": (33.6407, -84.4277),
                "Chicago O'Hare International Airport (ORD)": (41.9742, -87.9073),
                "Dallas/Fort Worth International Airport (DFW)": (32.8998, -97.0403),
                "Denver International Airport (DEN)": (39.8561, -104.6737),
                "John F. Kennedy International Airport (JFK)": (40.6413, -73.7781),
                "San Francisco International Airport (SFO)": (37.6213, -122.3790),
                "Los Angeles International Airport (LAX)": (33.9416, -118.4085),
                "Phoenix Sky Harbor International Airport (PHX)": (33.4373, -112.0078),
                "Seattle-Tacoma International Airport (SEA)": (47.4502, -122.3088),
                "Charlotte Douglas International Airport (CLT)": (35.2140, -80.9431),
                "Harry Reid International Airport (LAS)": (36.0840, -115.1537),
                "Orlando International Airport (MCO)": (28.4312, -81.3081),
                "Miami International Airport (MIA)": (25.7959, -80.2870),
                "Boston Logan International Airport (BOS)": (42.3656, -71.0096),
                "Detroit Metropolitan Wayne County Airport (DTW)": (42.2162, -83.3554),
                "Minneapolis−Saint Paul International Airport (MSP)": (44.8848, -93.2223),
                "Philadelphia International Airport (PHL)": (39.8744, -75.2424),
                "LaGuardia Airport (LGA)": (40.7769, -73.8740),
                "Salt Lake City International Airport (SLC)": (40.7899, -111.9791),
                "Ronald Reagan Washington National Airport (DCA)": (38.8512, -77.0402),
                "Baltimore/Washington International Thurgood Marshall Airport (BWI)": (39.1754, -76.6684),
                "Washington Dulles International Airport (IAD)": (38.9531, -77.4565),
                "San Diego International Airport (SAN)": (32.7338, -117.1933),
                "Tampa International Airport (TPA)": (27.9755, -82.5332),
                "Portland International Airport (PDX)": (45.5898, -122.5951),
                "Dallas Love Field (DAL)": (32.8471, -96.8517),
                "Nashville International Airport (BNA)": (36.1263, -86.6774),
                "Austin-Bergstrom International Airport (AUS)": (30.1975, -97.6664),
                "Raleigh–Durham International Airport (RDU)": (35.8776, -78.7875),
                "San Jose International Airport (SJC)": (37.3639, -121.9289),
                "Indianapolis International Airport (IND)": (39.7173, -86.2944),
                "Kansas City International Airport (MCI)": (39.2976, -94.7139),
                "Cleveland Hopkins International Airport (CLE)": (41.4117, -81.8498),
                "St. Louis Lambert International Airport (STL)": (38.7500, -90.3700),
                "Cincinnati/Northern Kentucky International Airport (CVG)": (39.0550, -84.6620),
                "Pittsburgh International Airport (PIT)": (40.4914, -80.2329),
                "Newark Liberty International Airport (EWR)": (40.6895, -74.1745),
                "Milwaukee Mitchell International Airport (MKE)": (42.9472, -87.8966),
                "Jacksonville International Airport (JAX)": (30.4941, -81.6879),
                "Sacramento International Airport (SMF)": (38.6951, -121.5908),
                "New Orleans Louis Armstrong International Airport (MSY)": (29.9934, -90.2580),
                "Honolulu International Airport (HNL)": (21.3245, -157.9251),
                "Anchorage Ted Stevens International Airport (ANC)": (61.1744, -149.9964),
                "Albuquerque International Sunport (ABQ)": (35.0494, -106.6170),
                "El Paso International Airport (ELP)": (31.8075, -106.3784),
                "Boise Airport (BOI)": (43.5644, -116.2228),
                "Omaha Eppley Airfield (OMA)": (41.3032, -95.8941),
                "Des Moines International Airport (DSM)": (41.5339, -93.6631),
                "Reno-Tahoe International Airport (RNO)": (39.4986, -119.7681),
                "Spokane International Airport (GEG)": (47.6250, -117.5375),
                "Fresno Yosemite International Airport (FAT)": (36.7762, -119.7181),
                "Syracuse Hancock International Airport (SYR)": (43.1112, -76.1063),
                "Laredo International Airport (LRD)": (27.5430,-99.4621)
                }
    
    selected_oloc = st.selectbox('Choose Origin Location', location.keys())
    origin_lat, origin_lon = location[selected_oloc]
    selected_dloc = st.selectbox('Choose Destination Location', location.keys())
    dest_lat, dest_lon = location[selected_dloc]

    if selected_oloc == selected_dloc:
        st.warning("Source and destination cannot be the same. Please select different airports.")
        st.stop()
    else:

        current_time = dt.now()
        max_time = current_time + timedelta(hours=24)
        flight_date = st.date_input('Select Flight Date (Next 24 Hours)', min_value=current_time.date(), max_value=max_time.date())

        time_str = st.text_input('Enter Departure Time (HHMM format):')


        if not time_str.isdigit() or len(time_str) not in [3, 4]:
            st.error("Please enter time in HHMM format (e.g., 800 for 08:00, 1430 for 14:30).")
        else:
            flight_datetime = convert_time(flight_date, time_str)

            if flight_datetime < current_time or flight_datetime > max_time:
                st.error("Please enter a time within the next 24 hours.")
            else:
                st.success("Valid time selected!")
        flight_datetime = convert_time(flight_date, time_str) - timedelta(hours=9, minutes=30)

        duration = st.number_input("Estimated Flight Duration (in minutes)", min_value=0, value=90)
        destination_datetime = flight_datetime + timedelta(minutes=duration) 
        destination_datetime1 = flight_datetime + timedelta(minutes=duration) + timedelta(hours=9, minutes=30)
        st.success(f"Destination Date & Time: {destination_datetime1.strftime('%Y-%m-%d %H:%M')}")



        origin_weather = get_weather(origin_lat, origin_lon, flight_datetime)
        dest_weather = get_weather(dest_lat, dest_lon, destination_datetime)

        for key in ['time','rhum','wdir','tsun', 'snow', 'wpgt']:
            origin_weather.pop(key, None)
            dest_weather.pop(key, None)


        origin_weather_values = np.array(list(origin_weather.values()))
        dest_weather_values = np.array(list(dest_weather.values()))

        features = np.concatenate((origin_weather_values, dest_weather_values)).reshape(1, -1)
        print(features)


        scaler = pickle.load(open('model\scaler_final2.sav', 'rb'))
        model = pickle.load(open('model\model_final2.sav', 'rb'))
        
        categ = ['Minor Delay', 'Moderate Delay', 'On-Time', 'Severe Delay']
        
       

        if st.button('Predict'):
                scaled_features = scaler.transform(features)
                result = model.predict(scaled_features)
                pred = np.argmax(result)
                status = categ[pred]
                display_result(status, status)



main()
































 # if st.button('Predict'):
        #     scaled_features = scaler.transform(features)
        #     result = model.predict(scaled_features)
        #     pred = np.argmax(result)
        #     st.write(f'{categ[pred]} EXPECTED! ')