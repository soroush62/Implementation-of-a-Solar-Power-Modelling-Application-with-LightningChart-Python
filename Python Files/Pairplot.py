# import numpy as np
# import pandas as pd
# import lightningchart as lc
# from scipy.stats import gaussian_kde

# with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
#     mylicensekey = f.read().strip()
# lc.set_license(mylicensekey)

# def generate_random_color():
#     return lc.Color(
#         np.random.randint(0, 256), 
#         np.random.randint(0, 256), 
#         np.random.randint(0, 256)
#     )

# generation_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Generation_Data.csv')
# weather_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Weather_Sensor_Data.csv')

# generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
# weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

# merged_data = pd.merge(generation_data, weather_data, on=['DATE_TIME', 'PLANT_ID'])
# merged_data['DATE_TIME'] = pd.to_datetime(merged_data['DATE_TIME'])
# features = ['DAILY_YIELD', 'TOTAL_YIELD', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE', 'IRRADIATION', 'AC_POWER']
# source_keys = merged_data['SOURCE_KEY_x'].unique()

# # Create color map with random colors
# color_map = {key: generate_random_color() for key in source_keys}

# # Create dashboard for pair plots
# dashboard = lc.Dashboard(
#     rows=len(features),
#     columns=len(features),
#     theme=lc.Themes.Dark
# )

# def create_density_chart(dashboard, title, values, color, column_index, row_index):
#     chart = dashboard.ChartXY(
#         column_index=column_index,
#         row_index=row_index
#     )
#     chart.set_title(title)

#     density = gaussian_kde(values)
#     x_vals = np.linspace(values.min(), values.max(), 100)
#     y_vals = density(x_vals)

#     series = chart.add_area_series()
#     series.add(x_vals.tolist(), y_vals.tolist())
#     series.set_name('Density')
#     series.set_fill_color(color)

#     chart.get_default_x_axis().set_title('Value')
#     chart.get_default_y_axis().set_title('Density')

# def create_scatter_chart(dashboard, title, x_values, y_values, color, xlabel, ylabel, column_index, row_index):
#     chart = dashboard.ChartXY(
#         column_index=column_index,
#         row_index=row_index
#     )
#     chart.set_title(title)

#     scatter_series = chart.add_point_series()
#     scatter_series.add(x_values, y_values)
#     scatter_series.set_point_color(color)

#     chart.get_default_x_axis().set_title(xlabel)
#     chart.get_default_y_axis().set_title(ylabel)

# # Generate pair plots
# for row_index, y_col in enumerate(features):
#     for column_index, x_col in enumerate(features):
#         if row_index == column_index:
#             for key in source_keys:
#                 values = merged_data[merged_data['SOURCE_KEY_x'] == key][x_col].astype(float).tolist()
#                 title = f'Density of {x_col} by {key}'
#                 create_density_chart(dashboard, title, np.array(values), color_map[key], column_index, row_index)
#         else:
#             for key in source_keys:
#                 x_values = merged_data[merged_data['SOURCE_KEY_x'] == key][x_col].astype(float).tolist()
#                 y_values = merged_data[merged_data['SOURCE_KEY_x'] == key][y_col].astype(float).tolist()
#                 title = f'{x_col} vs {y_col} by {key}'
#                 create_scatter_chart(dashboard, title, x_values, y_values, color_map[key], x_col, y_col, column_index, row_index)

# dashboard.open('browser')





import numpy as np
import pandas as pd
import lightningchart as lc
from scipy.stats import gaussian_kde

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

def generate_random_color():
    return lc.Color(
        np.random.randint(0, 256), 
        np.random.randint(0, 256), 
        np.random.randint(0, 256)
    )

generation_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Generation_Data.csv')
weather_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Weather_Sensor_Data.csv')

generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])

merged_data = pd.merge(generation_data, weather_data, on=['DATE_TIME', 'PLANT_ID'])
merged_data['DATE_TIME'] = pd.to_datetime(merged_data['DATE_TIME'])
features = ['DAILY_YIELD', 'TOTAL_YIELD', 'AMBIENT_TEMPERATURE', 'MODULE_TEMPERATURE',]
source_keys = merged_data['SOURCE_KEY_x'].unique()

# Create color map with random colors
color_map = {key: generate_random_color() for key in source_keys}

# Create dashboard for pair plots
dashboard = lc.Dashboard(
    rows=len(features),
    columns=len(features),
    theme=lc.Themes.Dark
)

def create_density_chart(dashboard, title, values, color, column_index, row_index):
    chart = dashboard.ChartXY(
        column_index=column_index,
        row_index=row_index
    )
    chart.set_title(title)

    density = gaussian_kde(values)
    x_vals = np.linspace(values.min(), values.max(), 100)
    y_vals = density(x_vals)

    series = chart.add_area_series()
    series.add(x_vals.tolist(), y_vals.tolist())
    series.set_name('Density')
    series.set_fill_color(color)

    chart.get_default_x_axis().set_title('Value')
    chart.get_default_y_axis().set_title('Density')

def create_scatter_chart(dashboard, title, x_values, y_values, color, xlabel, ylabel, column_index, row_index):
    chart = dashboard.ChartXY(
        column_index=column_index,
        row_index=row_index
    )
    chart.set_title(title)

    scatter_series = chart.add_point_series()
    scatter_series.add(x_values, y_values)
    scatter_series.set_point_color(color)

    chart.get_default_x_axis().set_title(xlabel)
    chart.get_default_y_axis().set_title(ylabel)

# Generate pair plots
for row_index, y_col in enumerate(features):
    for column_index, x_col in enumerate(features):
        if row_index == column_index:
            for key in source_keys:
                values = merged_data[merged_data['SOURCE_KEY_x'] == key][x_col].astype(float).tolist()
                title = f'Density of {x_col} by {key}'
                create_density_chart(dashboard, title, np.array(values), color_map[key], column_index, row_index)
        else:
            for key in source_keys:
                x_values = merged_data[merged_data['SOURCE_KEY_x'] == key][x_col].astype(float).tolist()
                y_values = merged_data[merged_data['SOURCE_KEY_x'] == key][y_col].astype(float).tolist()
                title = f'{x_col} vs {y_col} by {key}'
                create_scatter_chart(dashboard, title, x_values, y_values, color_map[key], x_col, y_col, column_index, row_index)

dashboard.open('browser')
