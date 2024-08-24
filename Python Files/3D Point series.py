import pandas as pd
import lightningchart as lc
import numpy as np
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

# Create grid data for the surface plot
grid_x, grid_y = np.meshgrid(
    np.linspace(x_values.min(), x_values.max(), 100),
    np.linspace(y_values.min(), y_values.max(), 100)
)

# Perform interpolation
grid_z = griddata(
    (x_values, y_values), z_values,
    (grid_x, grid_y),
    method='linear'
)

# Fill NaN values with the mean of the z_values
nan_mask = np.isnan(grid_z)
grid_z[nan_mask] = np.nanmean(z_values)

# Initialize a 3D chart
chart = lc.Chart3D(
    theme=lc.Themes.Dark,
    title='3D Surface of DAILY_YIELD vs MODULE_TEMPERATURE and AMBIENT_TEMPERATURE'
)

# Create a SurfaceGridSeries
surface_series = chart.add_surface_grid_series(
    columns=grid_z.shape[1],
    rows=grid_z.shape[0]
)

# Set start and end coordinates
surface_series.set_start(x=x_values.min(), z=y_values.min())
surface_series.set_end(x=x_values.max(), z=y_values.max())

# Set step size
surface_series.set_step(
    x=(x_values.max() - x_values.min()) / grid_z.shape[1],
    z=(y_values.max() - y_values.min()) / grid_z.shape[0]
)

# Invalidate height map
surface_series.invalidate_height_map(grid_z.tolist())

# Hide the wireframe (mesh lines)
surface_series.hide_wireframe()

# Define custom palette
surface_series.set_palette_colors(
    steps=[
        {"value": np.nanmin(grid_z), "color": lc.Color(0, 0, 255)},       # Blue for lower values
        {"value": np.nanpercentile(grid_z, 25), "color": lc.Color(0, 255, 255)},  # Cyan for lower mid values
        {"value": np.nanmedian(grid_z), "color": lc.Color(0, 255, 0)},    # Green for median values
        {"value": np.nanpercentile(grid_z, 75), "color": lc.Color(255, 255, 0)},  # Yellow for upper mid values
        {"value": np.nanmax(grid_z), "color": lc.Color(255, 0, 0)}        # Red for higher values
    ],
    look_up_property='value',
    percentage_values=False
)

# Invalidate intensity values (for color mapping)
surface_series.invalidate_intensity_values(grid_z.tolist())

# Set axis titles
chart.get_default_x_axis().set_title('MODULE_TEMPERATURE')
chart.get_default_y_axis().set_title('DAILY_YIELD')
chart.get_default_z_axis().set_title('AMBIENT_TEMPERATURE')

chart.add_legend(data=surface_series)

# Open the chart
chart.open()
