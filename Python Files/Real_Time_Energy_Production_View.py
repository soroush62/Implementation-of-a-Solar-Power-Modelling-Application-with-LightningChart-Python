import numpy as np
import lightningchart as lc
from datetime import datetime, timedelta
import pvlib
import pandas as pd
import time

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

generation_data = pd.read_csv('Dataset/Plant_2_Generation_Data.csv')
weather_data = pd.read_csv('Dataset/Plant_2_Weather_Sensor_Data.csv')

generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

merged_data = pd.merge(generation_data, weather_data, on=['DATE_TIME', 'PLANT_ID'])

merged_data['DATE_TIME'] = pd.to_datetime(merged_data['DATE_TIME'])

data = merged_data.drop_duplicates(subset=['DATE_TIME'])

latitude = 28.7041   # Example latitude (Delhi, India)
longitude = 77.1025  # Example longitude (Delhi, India)

solpos = pvlib.solarposition.get_solarposition(data['DATE_TIME'], latitude, longitude)
data['solar_azimuth'] = solpos['azimuth'].values
data['solar_altitude'] = solpos['apparent_elevation'].values

data = data[data['solar_altitude'] > 0]

dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=3)

ambient_gauge = dashboard.GaugeChart(row_index=0, column_index=0)
ambient_gauge.set_title('Ambient Temperature')
ambient_gauge.set_angle_interval(start=225, end=-45)
ambient_gauge.set_interval(start=0, end=60)
ambient_gauge.set_value_indicators([
    {'start': 0, 'end': 12, 'color': lc.Color(0, 0, 255)},  # Blue
    {'start': 12, 'end': 24, 'color': lc.Color(0, 255, 255)},  # Cyan
    {'start': 24, 'end': 36, 'color': lc.Color(0, 255, 0)},  # Green
    {'start': 36, 'end': 48, 'color': lc.Color(255, 255, 0)},  # Yellow
    {'start': 48, 'end': 60, 'color': lc.Color(255, 0, 0)}  # Red
])
ambient_gauge.set_bar_thickness(30)
ambient_gauge.set_value_indicator_thickness(8)

chart_solar_movement = dashboard.Chart3D(title='3D Solar Movement Over Time', row_index=0, column_index=1)
solar_series = chart_solar_movement.add_point_series()
solar_series.set_point_shape('sphere')
solar_series.set_point_size(10.0)

chart_solar_movement.get_default_x_axis().set_title('Azimuth (Degrees)')
chart_solar_movement.get_default_y_axis().set_title('Altitude (Degrees)')

z_axis = chart_solar_movement.get_default_z_axis()
z_axis.set_tick_strategy('DateTime', time_origin=data['DATE_TIME'].min().timestamp() * 1000)
z_axis.set_title('Date')

module_gauge = dashboard.GaugeChart(row_index=0, column_index=2)
module_gauge.set_title('Module Temperature')
module_gauge.set_angle_interval(start=225, end=-45)
module_gauge.set_interval(start=0, end=60)
module_gauge.set_value_indicators([
    {'start': 0, 'end': 12, 'color': lc.Color(0, 0, 255)},  # Blue
    {'start': 12, 'end': 24, 'color': lc.Color(0, 255, 255)},  # Cyan
    {'start': 24, 'end': 36, 'color': lc.Color(0, 255, 0)},  # Green
    {'start': 36, 'end': 48, 'color': lc.Color(255, 255, 0)},  # Yellow
    {'start': 48, 'end': 60, 'color': lc.Color(255, 0, 0)}  # Red
])
module_gauge.set_bar_thickness(30)
module_gauge.set_value_indicator_thickness(8)

chart_energy_generation = dashboard.ChartXY(title='AC Power Generation Over Time', row_index=1, column_index=0, column_span=3)
energy_series = chart_energy_generation.add_line_series()

chart_energy_generation.get_default_x_axis().set_title('Date').set_tick_strategy('DateTime', time_origin=data['DATE_TIME'].min().timestamp() * 1000)
chart_energy_generation.get_default_y_axis().set_title('AC Power (kW)')

dashboard.open(live=True)

start_time = time.time()

for i in range(len(data)):
    current_row = data.iloc[i]
    
    date_value = current_row['DATE_TIME'].timestamp() * 1000
    
    solar_series.add([current_row['solar_azimuth']], [current_row['solar_altitude']], [date_value])
    
    energy_series.add(date_value, current_row['AC_POWER'])
    
    ambient_gauge.set_value(current_row['AMBIENT_TEMPERATURE'])
    module_gauge.set_value(current_row['MODULE_TEMPERATURE'])
    
    time.sleep(0.2)