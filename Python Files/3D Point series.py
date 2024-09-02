import lightningchart as lc
import pandas as pd
import numpy as np

lc.set_license('mylicensekey')

generation_data = pd.read_csv('Dataset/Plant_2_Generation_Data.csv')
weather_data = pd.read_csv('Dataset/Plant_2_Weather_Sensor_Data.csv')

generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

merged_data = pd.merge(generation_data, weather_data, on=['DATE_TIME', 'PLANT_ID'])

features = ['DAILY_YIELD', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE']

chart = lc.Chart3D(
    title='3D Scatter Plot with Color Palette Based on DAILY_YIELD',
    theme=lc.Themes.Dark
)

x_values = merged_data['DAILY_YIELD'].astype(float).to_numpy()
y_values = merged_data['AMBIENT_TEMPERATURE'].astype(float).to_numpy()
z_values = merged_data['MODULE_TEMPERATURE'].astype(float).to_numpy()

scatter_series = chart.add_point_series()
scatter_series.set_point_shape('sphere')
scatter_series.set_point_size(4.0)

scatter_series.set_palette_point_colors(
    steps=[
        {"value": min(x_values), "color": lc.Color(0, 0, 255)},  # Blue for low values
        {"value": max(x_values), "color": lc.Color(255, 0, 0)}  # Red for high values
    ],
    look_up_property='x',  
    interpolate=True
)

scatter_series.add(x_values, y_values, z_values)

chart.get_default_x_axis().set_title('DAILY_YIELD')
chart.get_default_y_axis().set_title('AMBIENT_TEMPERATURE')
chart.get_default_z_axis().set_title('MODULE_TEMPERATURE')

chart.open()
