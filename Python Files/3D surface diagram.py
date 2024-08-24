import numpy as np
import pandas as pd
import lightningchart as lc
from scipy.interpolate import griddata

# Read the license key from a file
with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
generation_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Generation_Data.csv')
weather_data = pd.read_csv('D:/wenprograming23/src/team6/Implementation-of-a-Solar-Power-Modelling-Application-with-LightningChart-Python/Dataset/Plant_2_Weather_Sensor_Data.csv')

# Merge the data on DATE_TIME and PLANT_ID
generation_data['DATE_TIME'] = pd.to_datetime(generation_data['DATE_TIME'])
weather_data['DATE_TIME'] = pd.to_datetime(weather_data['DATE_TIME'])
merged_data = pd.merge(generation_data, weather_data, on=['DATE_TIME', 'PLANT_ID'])

# Extract the relevant features
x_values = merged_data['MODULE_TEMPERATURE'].astype(float).to_numpy()
y_values = merged_data['AMBIENT_TEMPERATURE'].astype(float).to_numpy()
z_values = merged_data['DAILY_YIELD'].astype(float).to_numpy()

# Create a grid for X and Y
grid_x, grid_y = np.mgrid[x_values.min():x_values.max():100j, y_values.min():y_values.max():100j]

# Interpolate Z values over the grid
grid_z = griddata((x_values, y_values), z_values, (grid_x, grid_y), method='cubic')

# Initialize a 3D chart
chart = lc.Chart3D(
    theme=lc.Themes.Dark,
    title='3D Surface Plot of DAILY_YIELD vs. MODULE_TEMPERATURE and AMBIENT_TEMPERATURE'
)

# Create the surface series
surface_series = chart.add_surface_grid_series(
    columns=grid_x.shape[0],
    rows=grid_y.shape[1]
)

surface_series.set_start(x=grid_x.min(), z=grid_y.min())
surface_series.set_end(x=grid_x.max(), z=grid_y.max())

surface_series.set_step(x=(grid_x.max() - grid_x.min()) / grid_x.shape[0], z=(grid_y.max() - grid_y.min()) / grid_y.shape[1])
surface_series.set_intensity_interpolation(True)
surface_series.invalidate_intensity_values(grid_z.tolist())

# Invalidate height map with the interpolated Z values
surface_series.invalidate_height_map(grid_z.tolist())

surface_series.hide_wireframe()

# Define custom palette
surface_series.set_palette_colors(
    steps=[
        {"value": np.nanmin(grid_z), "color": lc.Color(0, 0, 255)},  # Blue for lower values
        {"value": np.nanpercentile(grid_z, 25), "color": lc.Color(0, 255, 255)},  # Cyan for lower mid values
        {"value": np.nanmedian(grid_z), "color": lc.Color(0, 255, 0)},  # Green for median values
        {"value": np.nanpercentile(grid_z, 75), "color": lc.Color(255, 255, 0)},  # Yellow for upper mid values
        {"value": np.nanmax(grid_z), "color": lc.Color(255, 0, 0)}  # Red for higher values
    ],
    look_up_property='value',
    percentage_values=False
)

# Set axis titles
chart.get_default_x_axis().set_title('MODULE_TEMPERATURE')
chart.get_default_y_axis().set_title('DAILY_YIELD')
chart.get_default_z_axis().set_title('AMBIENT_TEMPERATURE')

chart.add_legend(data=surface_series)

# Open the chart
chart.open()
