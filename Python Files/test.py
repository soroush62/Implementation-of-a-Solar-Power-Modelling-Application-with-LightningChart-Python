import pandas as pd

generation_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Generation_Data.csv')
weather_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Weather_Sensor_Data.csv')

generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

print(generation_data.head())
print(weather_data.head())

merged_data = pd.merge(generation_data, weather_data, on=['DATE_TIME', 'PLANT_ID'])

print(merged_data.head())

selected_features = merged_data[['DC_POWER', 'AC_POWER', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION']]

corr_matrix = selected_features.corr()

heatmap_data = corr_matrix.values.tolist()

# Initialize the heatmap chart
chart = lc.ChartXY(
    theme=lc.Themes.White,
    title='Correlation Heatmap of Solar Plant Features'
)

# Create the heatmap grid series
series = chart.add_heatmap_grid_series(
    columns=len(heatmap_data),
    rows=len(heatmap_data[0])
)

# Customize the heatmap
series.hide_wireframe()
series.set_intensity_interpolation(False)
series.invalidate_intensity_values(heatmap_data)

# Define color steps for the heatmap
series.set_palette_colors(
    steps=[
        {"value": -1.0, "color": lc.Color(0, 0, 255)},  # Blue for negative correlation
        {"value": 0.0, "color": lc.Color(255, 255, 255)},  # White for no correlation
        {"value": 1.0, "color": lc.Color(255, 0, 0)}  # Red for positive correlation
    ],
    look_up_property='value',
    percentage_values=False
)

# Customize the x and y axes
x_axis = chart.get_default_x_axis()
x_axis.set_title('Feature Index')
x_axis.set_interval(0, len(selected_features.columns))

y_axis = chart.get_default_y_axis()
y_axis.set_title('Feature Index')
y_axis.set_interval(0, len(selected_features.columns))

# Open the chart
chart.open()


