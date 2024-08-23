import pandas as pd

generation_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Generation_Data.csv')
weather_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Weather_Sensor_Data.csv')

generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

print(generation_data.head())
print(weather_data.head())
