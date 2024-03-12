import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.offline import plot
import kmeans

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
    cities.append((phi, theta))
    #cities.append([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
cities = r * np.array(cities)
cities_weights = np.random.randint(1, 100, n_cities)

satellites = kmeans.spherical_kmeans(cities, [], n_sat)


def spherical_to_lat_long(data):
    return 180/np.pi * r * data

satellites_lat, satellites_long = spherical_to_lat_long(satellites.T)
cities_lat, cities_long = spherical_to_lat_long(cities.T)


#Data Creation
satsd = {'Lat':satellites_lat,
 'Lon':satellites_long,
 'colorcode': ['blue']*n_sat}
satsdf = pd.DataFrame(satsd)

citiesd = {'Lat': cities_lat, 'Lon': cities_long, 'colorcode': ['red']*n_cities}
citiesdf = pd.DataFrame(citiesd)


# Coverage circles

t = np.linspace(0, 2*np.pi, 100)
R = 15 
Rcost = R*np.cos(t)
Rsint = R*np.sin(t)

for i in range(n_sat):
    lon, lat = Rcost + satellites_lat[i], Rsint + satellites_long[i]
    fig.add_trace(go.Scattergeo(mode = "lines",lon = lon,lat = lat,marker = {'size': 10,'color': satsd['colorcode'],'colorscale':'jet','colorbar_thickness':20}))


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



R = 0.75
center_lon = 9.18951
center_lat = 45.46427
t = np.linspace(0, 2*np.pi, 100)
circle_lon =center_lon + R*np.cos(t)
circle_lat =center_lat +  R*np.sin(t)


coords=[]
for lo, la in zip(list(circle_lon), list(circle_lat)):
    coords.append([lo, la]) 

layers=[dict(sourcetype = 'geojson',
             source={ "type": "Feature",
                     "geometry": {"type": "LineString",
                                  "coordinates": coords
                                  }
                    },
             color=   'red',
             type = 'line',   
             line=dict(width=1.5)
            )]

fig.update_layout(
    title_text='Your title',
    width=850,
    height=850,
    mapbox=dict(
        #accesstoken="",
        layers=layers,
        bearing=0,
        center=dict(
            lat=45.8257,
            lon=10.8746, 
        ),
        pitch=0,
        zoom=5.6,
        style='outdoors')
   )
plot(fig)

