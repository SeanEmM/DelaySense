
import pandas as pd
from meteostat import Point,Hourly
import datetime
import warnings
import os
warnings.simplefilter(action='ignore', category=Warning)

from datetime import timedelta
def time_coversion(date,time):
  time = str(time).zfill(4)
  if time=='2400':
    date+=timedelta(days=1)
    time="0000"
  return datetime.datetime.combine(date,datetime.datetime.strptime(time,"%H%M").time())

def batch_fetch_weather(locations, filename):
    weather_dict = {}
    file_exists = os.path.isfile(filename)  # Check if file already exists

    for row in locations.itertuples(index=False, name=None):
        lat, lon, time = row
        loc = Point(lat, lon)

        weather = Hourly(loc, time, time + timedelta(hours=1)).fetch()

        if not weather.empty:
            weather_data = weather.iloc[0].to_dict()
            weather_dict[(lat, lon, time)] = weather_data

            # Convert data to DataFrame
            weather_df = pd.DataFrame([{**{'latitude': lat, 'longitude': lon, 'time': time}, **weather_data}])

            # Save the data immediately
            weather_df.to_csv(filename, mode='a', index=False, header=not file_exists)
            file_exists = True  # After first write, set header=False

    return weather_dict

def map_weather(lat,lon,time,weather_dict):
  return weather_dict.get((lat,lon,time),{})



df = pd.read_csv('flights_sample_3m.csv')
df2 = pd.read_csv('airport_location.csv')

df['DELAY_DUE_WEATHER'] = df['DELAY_DUE_WEATHER'].fillna(0)



df.drop(['DEP_DELAY','DEP_TIME','ARR_TIME','TAXI_OUT','WHEELS_OFF','WHEELS_ON','TAXI_IN','ARR_DELAY','CANCELLATION_CODE','DIVERTED','CRS_ELAPSED_TIME','ELAPSED_TIME','AIR_TIME','DELAY_DUE_SECURITY','DELAY_DUE_NAS','DELAY_DUE_CARRIER','DELAY_DUE_LATE_AIRCRAFT'],axis=1,inplace=True)

# **Joining both DataFrames**

df = df.merge(df2, left_on='ORIGIN', right_on='airport', how='left')
df.rename(columns={'latitude':'origin_latitude','longitude':'origin_longitude'},inplace=True)
df.drop(columns=['airport'],axis=1,inplace=True)

df = df.merge(df2, left_on='DEST', right_on='airport', how='left')
df.rename(columns={'latitude':'DEST_latitude','longitude':'DEST_longitude'},inplace=True)
df.drop(columns=['airport'],axis=1,inplace=True)

flight_data = df.iloc[:50000,:]



flight_data['FL_DATE'] = pd.to_datetime(flight_data['FL_DATE'])



flight_data['dept_date_time'] = flight_data.apply(lambda x: time_coversion(x['FL_DATE'], x['CRS_DEP_TIME']),axis=1)

flight_data['arr_date_time'] = flight_data.apply(lambda y: time_coversion(y['FL_DATE'], y['CRS_ARR_TIME']),axis=1)


unique_origin = flight_data[['origin_latitude','origin_longitude','dept_date_time']].drop_duplicates()


unique_dest = flight_data[['DEST_latitude','DEST_longitude','arr_date_time']].drop_duplicates()


unique_location = pd.concat([unique_origin,unique_dest]).drop_duplicates()


departure_weather = batch_fetch_weather(unique_origin, 'departure_weather.csv')
arrival_weather = batch_fetch_weather(unique_dest, 'arrival_weather.csv')
















# filtered_data = flight_data[(flight_data['dept_date_time'].dt.day<=2) & (flight_data['dept_date_time'].dt.year==2022) & (flight_data['dept_date_time'].dt.month.isin([7]))]
# # filtered_data = flight_data[(flight_data['dept_date_time'].dt.day<=2) & (flight_data['dept_date_time'].dt.year==2022) & (flight_data['dept_date_time'].dt.month.isin([5]))]
# # filtered_data = flight_data[(flight_data['dept_date_time'].dt.year==2022) & (flight_data['dept_date_time'].dt.month.isin([5,6,7]))]
# # filtered_data = filtered_data[filtered_data['DELAY_DUE_WEATHER']>0]
# # filtered_data = filtered_data[(filtered_data['dept_date_time'].dt.year==2022) & (filtered_data['dept_date_time'].dt.month.isin([5]))]

# filtered_data.drop(['CANCELLED','FL_DATE','AIRLINE','AIRLINE_DOT','AIRLINE_CODE','DOT_CODE','FL_NUMBER','ORIGIN','ORIGIN_CITY','DEST','DEST_CITY','CRS_DEP_TIME','CRS_ARR_TIME','DISTANCE'],axis=1,inplace=True)



# filtered_data = pd.concat([temp1,temp2],ignore_index=True)

# filtered_data.reset_index(drop=True,inplace=True)

# **Collecting Weather Data**

#
# flight_data['departure_weather'] = flight_data.apply(lambda row:map_weather(row['origin_latitude'],row['origin_longitude'],row['dept_date_time'],departure_weather),axis = 1)
#
# flight_data['arrival_weather'] = flight_data.apply(lambda row:map_weather(row['DEST_latitude'],row['DEST_longitude'],row['arr_date_time'],arrival_weather),axis = 1)
#
# # filtered_data['departure_weather'] = filtered_data.apply(lambda row:batch_fetch_weather(row['origin_latitude'],row['origin_longitude'],row['dept_date_time']) )
#
# departure_weather_df = flight_data['departure_weather'].apply(pd.Series).add_prefix('departure_')
#
# arrival_weather_df = flight_data['arrival_weather'].apply(pd.Series).add_prefix('arrival_')
#
# flight_data = pd.concat([flight_data,departure_weather_df,arrival_weather_df],axis=1).drop(columns=['departure_weather','arrival_weather'])
#
# # filtered_data.drop(['arrival_tsun','arrival_snow', 'departure_tsun','departure_wpgt','departure_snow','arrival_wpgt'],axis=1,inplace=True)
#
# flight_data.to_csv('w1.csv',index=False)


# def fetch_weather(lat,lon,time):
#     loc = Point(lat,lon)
#     weather = Hourly(loc,time,time+timedelta(hours=1)).fetch()
#     return weather_dict

# def fetch_weather(location):
#     lat,lon,time = location
#     key = (lat,lon,time)
#     if key in weather_cache:
#       return key, weather_cache[key]
#     loc = Point(lat,lon)
#     weather = Hourly(loc,time,time+timedelta(hours=1)).fetch()
#     if not weather.empty:
#       weather_cache[key] = weather.iloc[0].to_dict()
#       return key, weather.iloc[0].to_dict()
#     else:
#       return key, {}

# from multiprocessing import Pool
# pool = Pool(processes=10)
# weather_results = pool.map(fetch_weather,location_list)
# pool.close()
# pool.join()

# departure_times = filtered_data['dept_date_time'].unique()
# arrival_times = filtered_data['arr_date_time'].unique()

# departure_weather = {}
# for _, row in filtered_data[['origin_latitude', 'origin_longitude']].drop_duplicates().iterrows():
#     lat, lon = row['origin_latitude'], row['origin_longitude']

#     # Iterate over each departure time
#     for dep_time in departure_times:
#         print(f"Fetching weather for lat: {lat}, lon: {lon}, departure_time: {dep_time}")

#         # Ensure that fetch_weather gets one datetime value at a time
#         departure_weather[(lat, lon, dep_time)] = fetch_weather(lat, lon, dep_time)

# dept_weather_df = filtered_data['departure_weather']

# filtered_weather_data = filtered_data.drop(['CANCELLED','DISTANCE','CRS_ARR_TIME','CRS_DEP_TIME'],axis=1)


# flight_data['origin_weather']= flight_data.apply(lambda x : get_weather(x['origin_latitude'],x['origin_longitude'],x['arr_date_time']),axis=1)

# flight_data['dept_weather']= flight_data.apply(lambda x : get_weather(x['DEST_latitude'],x['DEST_longitude'],x['arr_date_time']),axis=1)

# from sklearn.preprocessing import LabelEncoder
# encoder = LabelEncoder()
# col = ['AIRLINE','AIRLINE_DOT','AIRLINE_CODE','ORIGIN','ORIGIN_CITY','DEST','DEST_CITY']
# for i in col:
#   flight_data[i]=encoder.fit_transform(flight_data[i])
#   print(encoder.classes_)

# flight_data





