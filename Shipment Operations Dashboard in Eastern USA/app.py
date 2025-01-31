import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

# Load the necessary data
factories_df = pd.read_csv('C:\\Users\\Lenovo\\Documents\\GitHub\\portfolio\\TDLOG\\Candy_Factories.csv')
sales_df = pd.read_csv('C:\\Users\\Lenovo\\Documents\\GitHub\\portfolio\\TDLOG\\Candy_Sales.csv')
products_df = pd.read_csv('C:\\Users\\Lenovo\\Documents\\GitHub\\portfolio\\TDLOG\\Candy_Products.csv')
uszips_df = pd.read_csv('C:\\Users\\Lenovo\\Documents\\GitHub\\portfolio\\TDLOG\\uszips.csv')  # Load ZIP code data

# Ensure postal codes are strings for merging
sales_df['Postal Code'] = sales_df['Postal Code'].astype(str)
uszips_df['zip'] = uszips_df['zip'].astype(str)

# Merge sales data with uszips to get latitude and longitude for shipment locations
sales_with_location = sales_df.merge(uszips_df[['zip', 'lat', 'lng']], left_on='Postal Code', right_on='zip', how='left')

# Calculate delivery time for heatmap
sales_with_location['Delivery Time'] = (pd.to_datetime(sales_with_location['Ship Date']) - pd.to_datetime(sales_with_location['Order Date'])).dt.days
region_performance = sales_with_location.groupby('Region').agg(avg_delivery_time=('Delivery Time', 'mean')).reset_index()

# Randomly generate delivery agent locations in the eastern USA
np.random.seed(42)
num_agents = 20  # Number of delivery agents
# Define lat/lon ranges to focus on the right half of the USA
agent_lats = np.random.uniform(24.396308, 49.384358, num_agents)  # Approximate latitudes for the right half
agent_lons = np.random.uniform(-100, -66.93457, num_agents)  # Approximate longitudes for eastern USA

# Initialize the Dash app
app = dash.Dash(__name__)

# Define layout with Delivery Performance Heatmap added
app.layout = html.Div([
    html.H1("Shipment Operations Dashboard - Eastern USA"),
    dcc.Tabs([
        dcc.Tab(label='Factory & Shipment Locations', children=[
            dcc.Graph(id="map-graph"),
            html.Label("Filter by Product Type"),
            dcc.Dropdown(
                id='product-type-filter',
                options=[{'label': div, 'value': div} for div in products_df['Division'].unique()],
                multi=True,
                placeholder="Select product types"
            )
        ]),
        dcc.Tab(label='Shipment Metrics', children=[
            dcc.Graph(id="shipment-volume"),
            dcc.Graph(id="delivery-performance-heatmap")
        ]),
        dcc.Tab(label='Product Distribution', children=[
            dcc.Graph(id="product-distribution")
        ])
    ])
])

# Map callback for interactive filtering by product type
@app.callback(
    Output("map-graph", "figure"),
    Input("product-type-filter", "value")
)
def update_map(selected_product_types):
    filtered_data = sales_with_location if not selected_product_types else sales_with_location[sales_with_location['Division'].isin(selected_product_types)]
    
    # Create map with eastern USA limits and add delivery agent markers
    fig = px.scatter_mapbox(
        filtered_data, lat="lat", lon="lng", hover_name="City", color="Division",
        mapbox_style="carto-positron", zoom=3, title="Factory and Shipment Locations in Eastern USA"
    )
    
    # Add delivery agents as red points
    fig.add_scattermapbox(
        lat=agent_lats, lon=agent_lons, mode='markers', marker=dict(size=8, color='red'), 
        name="Delivery Agents"
    )
    
    # Adjust map viewport to focus on eastern USA
    fig.update_layout(mapbox=dict(center=dict(lat=37.5, lon=-83), zoom=4))
    
    return fig

# Heatmap for delivery performance by region
@app.callback(
    Output("delivery-performance-heatmap", "figure"),
    Input("product-type-filter", "value")
)
def update_heatmap(selected_product_types):
    filtered_data = region_performance if not selected_product_types else region_performance[region_performance['Division'].isin(selected_product_types)]
    fig = px.choropleth(filtered_data, locations="Region", locationmode="USA-states", color="avg_delivery_time",
                        color_continuous_scale="YlOrRd", scope="usa",
                        title="Average Delivery Time by Region")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
