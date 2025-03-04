import pandas as pd
import numpy as np
import lightningchart as lc
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import time

lc.set_license('mylicensekey')

generation_data = pd.read_csv('Dataset/Plant_2_Generation_Data.csv')
weather_data = pd.read_csv('Dataset/Plant_2_Weather_Sensor_Data.csv')

generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

merged_data = pd.merge(generation_data, weather_data, on=['DATE_TIME', 'PLANT_ID'])

features = ['AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION']
X = merged_data[features]
y = merged_data['AC_POWER']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

dashboard = lc.Dashboard(theme=lc.Themes.Dark, rows=2, columns=2)

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

module_gauge = dashboard.GaugeChart(row_index=0, column_index=1)
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

power_chart = dashboard.ChartXY(row_index=1, column_index=0, column_span=2, title='Predicted AC Power Over Time')
Area_series = power_chart.add_area_series().set_name('Predicted AC Power')
Area_series.set_fill_color(lc.Color(255, 255, 255))

power_chart.get_default_x_axis().set_title('Time (Seconds)')
power_chart.get_default_y_axis().set_title('Predicted AC Power')

def generate_random_weather_data():
    return {
        'AMBIENT_TEMPERATURE': np.random.uniform(X['AMBIENT_TEMPERATURE'].min(), X['AMBIENT_TEMPERATURE'].max()),
        'MODULE_TEMPERATURE': np.random.uniform(X['MODULE_TEMPERATURE'].min(), X['MODULE_TEMPERATURE'].max()),
        'IRRADIATION': np.random.uniform(X['IRRADIATION'].min(), X['IRRADIATION'].max())
    }

def update_dashboard():
    predicted_values = []
    time_values = []
    start_time = time.time()

    for i in range(1000):  
        random_weather = generate_random_weather_data()
        random_weather_df = pd.DataFrame([random_weather])

        predicted_power = model.predict(random_weather_df)[0]

        current_time = time.time() - start_time
        predicted_values.append(predicted_power)
        time_values.append(current_time)

        Area_series.add(time_values[-1], predicted_values[-1])

        ambient_gauge.set_value(random_weather['AMBIENT_TEMPERATURE'])
        module_gauge.set_value(random_weather['MODULE_TEMPERATURE'])

        time.sleep(0.5)

dashboard.open(live=True)
update_dashboard()