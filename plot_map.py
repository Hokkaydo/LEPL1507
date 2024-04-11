
import geopandas as gpd
import numpy as np
from math import asin
import math
import plotly.graph_objects as go
from plotly.offline import plot

def plot_sphere(fig):
    """plot sphere"""
    col=f'rgb(125, 125, 125)'
    R = np.sqrt(6268.134)
    phi = np.linspace(0,2* np.pi, 45)
    theta = np.linspace(0, np.pi, 45)
    x = np.outer(R*np.cos(phi), R*np.sin(theta))
    y = np.outer(R*np.sin(phi), R*np.sin(theta))
    z = np.outer(R*np.ones(phi.shape[0]), R*np.cos(theta))
    fig.add_surface(x=x, y=y, z=z, colorscale=[[0, col], [1, col]], showscale = False, opacity=1.0, showlegend=False, lighting=dict(diffuse=0.1))
       

def plot_polygon(poly):
    
    xy_coords = poly.exterior.coords.xy
    lon = np.array(xy_coords[0])
    lat = np.array(xy_coords[1])
    
    lon = lon * np.pi/180
    lat = lat * np.pi/180
    
    R = 6268.134
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)
    
    return x, y, z

def plot_countries(fig, file):
    for i in file.index :
        # print(gdf.loc[i].NAME)            # Call a specific attribute
    
        polys = file.loc[i].geometry         # Polygons or MultiPolygons
    
        if polys.geom_type == 'Polygon':
            x, y, z = plot_polygon(polys)
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color=f'rgb(255, 255, 255)'), showlegend=False) )
        
        elif polys.geom_type == 'MultiPolygon':
        
            for poly in polys.geoms:
                x, y, z = plot_polygon(poly)
                fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color=f'rgb(255, 255, 255)'), showlegend=False) )

def draw_circle_on_sphere(a:float, p:float, radius:float):
    '''
        Parametric equation determined by the radius and angular positions (both polar and azimuthal relative to the z-axis) of the circle on the spherical surface
        Parameters:
            a (float): polar angle
            p (float): azimuthal angle
            radius (float): radius of the circle
            
        Returns:
            Circular scatter points on a spherical surface
    '''
    x = []; y = []; z = []
    for i in range(6, 600):
        v = asin(radius/(i*1000))
        u = np.mgrid[0:2*np.pi:30j]
        x1 = (np.sin(v)*np.cos(p)*np.cos(a)*np.cos(u) + np.cos(v)*np.sin(p)*np.cos(a) - np.sin(v)*np.sin(a)*np.sin(u))*(6428.134)
        y1 = (np.sin(v)*np.cos(p)*np.sin(a)*np.cos(u) + np.cos(v)*np.sin(p)*np.sin(a) + np.sin(v)*np.cos(a)*np.sin(u))*6428.134
        z1 = -np.sin(v)*np.sin(p)*np.cos(u)*6428.134 + np.cos(v)*np.cos(p)*6428.134
        x.append(x1) ; y.append(y1) ; z.append(z1)
        
    return x, y, z
    

def spherical_coords(lons, lats):
    '''
        Convert the latitude and longitude of the cities to the spherical coordinates
            
        Parameters:
            lon (list of floats): longitude of the cities
            lats (list of floats): latitude of the cities
                
         Returns:
             x, y, z (list of floats): spherical coordinates of the cities
    '''
    x_coords = []; y_coords = []; z_coords = []
    for lat, lon in zip(lats, lons):
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        x = math.sin(lon_rad) * math.cos(lat_rad)*6318.134
        y = math.sin(lon_rad) * math.sin(lat_rad)*6318.134
        z = math.cos(lon_rad)*6318.134
        x_coords.append(x) ; y_coords.append(y) ; z_coords.append(z)
    return x_coords, y_coords, z_coords

def plot_cities(lons, lats, weights):
    '''
        Place the cities on the spherical surface
                
            lons (list of floats): longitude of the cities
            lats (list of floats): latitude of the cities
            
        Returns:
            None
    '''
    x, y, z = spherical_coords(lons, lats)
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', line=dict(color=f'rgb(190, 0,0)', width = 6), marker=dict(size=weights/np.max(weights)*25), showlegend=False ) )

def plot_satellite_long_lat(long, lat):
    '''
        Place the satellite on the spherical surface
        
            long (list of floats): longitude of the satellite
            lat (list of floats): latitude of the satellite
            
        Returns:
            None
    '''
    x, y, z = spherical_coords(long, lat)
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', line=dict(color=f'rgb(0, 0, 70)', width = 4), showlegend=False ) )
def plot_satellite(pol, azi, rad):
    '''
        Place the satellite on the spherical surface
        
            pol (list of floats): polar angles of the satellite
            a (list of floats): azimuthal angles of the satellite
            radius (float): radius of the surface coverd by the satellite
        Returns:
            None
    '''
    clor =f'rgb(0, 0, 230)'
    
    x = 6371 * np.sin(azi) * np.cos(pol)
    y = 6371 * np.sin(azi) * np.sin(pol)
    z = 6371 * np.cos(azi)
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', line=dict(color=f'rgb(0, 0, 70)', width = 4), showlegend=False ) )
    
    for p, a in zip(pol, azi):
        x, y, z = draw_circle_on_sphere(p, a, rad)
        fig.add_surface(z=z, x=x, y=y, colorscale=[[0, clor], [1, clor]],showscale = False, opacity=0.5, showlegend=False, lighting=dict(diffuse=0.1))

def plot_fig(filename="temp-plot.html", auto_open=True):
    # Read the shapefile.  Creates a DataFrame object
    gdf = gpd.read_file("ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")
    plot_sphere(fig)
    plot_countries(fig, gdf)
    plot(fig, filename=filename, auto_open=auto_open)
    
def create_fig():
    global fig 
    fig = go.Figure()
    fig.update_layout(
    scene = dict(
        xaxis = dict(visible=False),
        yaxis = dict(visible=False),
        zaxis =dict(visible=False)
        )
    )
#Exemple de villes et satellites
def test():
    pol = [np.pi/4, np.pi/3, np.pi/2]
    #vecteur azi pour plot_satellite
    azi = [np.pi, np.pi/2, 0, 3*np.pi/2]
    #radius pour plot_satellite
    rad = 4000
    plot_satellite(pol, azi, rad)
    #vecteur lons pour plot_cities
    latss = [40.7128, 34.0522, 41.8781, 29.7604, 33.4484,
            51.5074, 48.8566, 52.5200, 55.7558, 39.9042,
            35.6895, -33.8688, -23.5505, 19.4326, 19.0760]
    lonss = [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740,
            -0.1278, 2.3522, 13.4050, 37.6176, 116.4074,
            139.6917, 151.2093, -46.6333, -99.1332, 72.8777]
    plot_cities(lonss, latss)
    
#affiche un exemple de villes et de satellites
#test()

#fig.write_html("3d_plot.html")

