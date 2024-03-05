import plotly.express as px
from plotly.offline import plot

def plot_cities(cities, lats, lons, populations):
    # Create a DataFrame
    data = {'City': cities, 'Latitude': lats, 'Longitude': lons, 'Population': populations}
    
    # Plotly Express scatter_geo plot
    fig = px.scatter_geo(data, lat='Latitude', lon='Longitude', text='City',
                         size='Population', projection="natural earth")
    
    # Update layout
    fig.update_traces(marker=dict(size=10, color='blue', opacity=0.0),
                      selector=dict(mode='markers'))
    fig.update_layout(title='Cities on Map', geo=dict(showcountries=True))
    
    # Show plot
    #fig.show()
    plot(fig)

# Example cities and their coordinates (and corrected populations)
cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
          'London', 'Paris', 'Berlin', 'Moscow', 'Beijing',
          'Tokyo', 'Sydney', 'Sao Paulo', 'Mexico City', 'Mumbai']
lats = [40.7128, 34.0522, 41.8781, 29.7604, 33.4484,
        51.5074, 48.8566, 52.5200, 55.7558, 39.9042,
        35.6895, -33.8688, -23.5505, 19.4326, 19.0760]
lons = [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740,
        -0.1278, 2.3522, 13.4050, 37.6176, 116.4074,
        139.6917, 151.2093, -46.6333, -99.1332, 72.8777]
populations = [8336817, 3979576, 2693976, 2320268, 1680992,
               8908081, 2140526, 3769495, 12615279, 21542000,
               13929286, 5312437, 21292893, 21782378, 12442373]

plot_cities(cities, lats, lons, populations)

