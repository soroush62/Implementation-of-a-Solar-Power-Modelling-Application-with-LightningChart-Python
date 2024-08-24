import pandas as pd
import lightningchart as lc
from lightningchart import Color, Dashboard, Themes

with open('D:/Computer Aplication/WorkPlacement/Projects/shared_variable.txt', 'r') as f:
    mylicensekey = f.read().strip()
lc.set_license(mylicensekey)

# Load the dataset
file_path = 'D:/Computer Aplication/WorkPlacement/Hossein/country-level-monthly-temperature-anomalies.csv'
data = pd.read_csv(file_path)

# Function to create a map chart for a given year and month
def create_map_chart(dashboard, data, year, column_index, row_index):
    data_year = data[(data['Year'] == year)]
    data_year = data_year[['Code', 'March']].rename(columns={'Code': 'ISO_A3', 'March': 'value'})

    # Create world map chart
    chart = dashboard.MapChart(column_index=column_index, row_index=row_index)

    # Set temperature anomaly data
    chart.invalidate_region_values(data_year.to_dict(orient='records'))

    # Set color palette
    chart.set_palette_colors(
        steps=[
            {'value': -5, 'color': Color('#0000FF')},  # Blue for cold anomalies
            {'value': 0, 'color': Color('#FFFFFF')},  # White for no anomaly
            {'value': 5, 'color': Color('#FF0000')}   # Red for warm anomalies
        ],
        look_up_property='value',
        percentage_values=False
    )

    # Enable hover highlighting
    chart.set_highlight_on_hover(enabled=True)

    # Add legend
    legend = chart.add_legend(horizontal=True, title=f"March Temperature Anomaly - Year: {year}", data=chart)
    legend.set_font_size(10)  # Adjust font size as needed

    return chart

# Create a dashboard to arrange the charts
dashboard = Dashboard(
    rows=2,
    columns=2,
    theme=Themes.White
)

# Create and add map charts to the dashboard
create_map_chart(dashboard, data, 1990, column_index=0, row_index=0)
create_map_chart(dashboard, data, 2000, column_index=1, row_index=0)
create_map_chart(dashboard, data, 2010, column_index=0, row_index=1)
create_map_chart(dashboard, data, 2020, column_index=1, row_index=1)

# Open the dashboard
dashboard.open(live=True)
