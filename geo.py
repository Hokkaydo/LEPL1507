from math import sqrt
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.offline import plot
import kmeans
import conversion

fig = go.Figure()
size = 50

n_cities = 100
n_sat = 10

r = 6371

# Initialization of cities
cities = []
for i in range (n_cities) :
    phi = np.random.rand() * 2*np.pi
    theta = np.random.rand() * np.pi
    #cities.append((phi, theta))
    cities.append([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
cities = r * np.array(cities)
cities_weights = np.random.randint(1, 100, n_cities)

# shape (n, 3)
satellites_cart = kmeans.spherical_kmeans(cities, [], n_sat)

def spherical_to_lat_long(data):
    return 180/np.pi * data

print(conversion.polar(*satellites_cart.T))
satellites_polar = np.array(conversion.polar(*satellites_cart.T))[1:]
cities_polar = np.array(conversion.polar(*cities.T))[1:]

satellites_lat, satellites_long = spherical_to_lat_long(satellites_polar)
cities_lat, cities_long = spherical_to_lat_long(cities_polar)


#Data Creation
satsd = {'Lat':satellites_lat,
 'Lon':satellites_long,
 'colorcode': ['blue']*n_sat}
satsdf = pd.DataFrame(satsd)

citiesd = {'Lat': cities_lat, 'Lon': cities_long, 'colorcode': ['red']*n_cities}
citiesdf = pd.DataFrame(citiesd)


# Coverage circles

t = np.linspace(0, 2*np.pi, 100)*180/np.pi
R = 15 
Rcost = t#R*np.cos(t)*180/np.pi
Rsint = t#R*np.sin(t)*180/np.pi

#for i in range(n_sat):
lon, lat = Rsint + satellites_lat[3], Rcost + satellites_long[3]
#fig.add_trace(go.Scattergeo(mode = "lines",lon = lon,lat = lat,marker = {'size': 10,'color': satsd['colorcode'],'colorscale':'jet','colorbar_thickness':20}))


fig.add_trace(go.Scattergeo(mode = "markers",lon = satsdf['Lon'],lat = satsdf['Lat'],marker = {'size': 10,'color': satsd['colorcode'],'colorscale':'jet','colorbar_thickness':20}))

fig.add_trace(go.Scattergeo(mode = "markers", lon = citiesdf['Lon'], lat=citiesdf['Lat'], marker={'size': 10, 'color': citiesdf['colorcode'], 'colorscale': 'jet', 'colorbar_thickness': 20}))


fig.update_layout(  geo = dict(
                    showland = True,
                    showcountries = True,
                    showocean = True,
                    countrywidth = 0.5,
                    landcolor = 'rgb(178, 178, 178)',
                    lakecolor = 'rgb(255, 255, 255)',
                    oceancolor = 'rgb(255, 255, 255)',
                    projection = dict(
                        type = 'orthographic',
                    ),
                    lonaxis = dict(
                        showgrid = True,
                        gridcolor = 'rgb(102, 102, 102)',
                        gridwidth = 0.5
                    ),
                    lataxis = dict(
                        showgrid = True,
                        gridcolor = 'rgb(102, 102, 102)',
                        gridwidth = 0.5
                    ),
                )
)



plot(fig)

