
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import sys
import pandas as pd
from math import asin
import requests
import plotly.graph_objects as go
from plotly.offline import plot

def plot_back(fig):
    """back half of sphere"""
    clor=f'rgb(220, 220, 220)'
    R = np.sqrt(6368.134)
    u_angle = np.linspace(0, np.pi, 25)
    v_angle = np.linspace(0, np.pi, 25)
    x_dir = np.outer(R*np.cos(u_angle), R*np.sin(v_angle))
    y_dir = np.outer(R*np.sin(u_angle), R*np.sin(v_angle))
    z_dir = np.outer(R*np.ones(u_angle.shape[0]), R*np.cos(v_angle))
    fig.add_surface(z=z_dir, x=x_dir, y=y_dir, colorscale=[[0, clor], [1, clor]], opacity=1.0, showlegend=False, lighting=dict(diffuse=0.1)) # opacity=fig.sphere_alpha, colorscale=[[0, fig.sphere_color], [1, fig.sphere_color]])


def plot_front(fig):
    """front half of sphere"""
    clor=f'rgb(220, 220, 220)'
    R = np.sqrt(6368.134)
    u_angle = np.linspace(-np.pi, 0, 25)
    v_angle = np.linspace(0, np.pi, 25)
    x_dir = np.outer(R*np.cos(u_angle), R*np.sin(v_angle))
    y_dir = np.outer(R*np.sin(u_angle), R*np.sin(v_angle))
    z_dir = np.outer(R*np.ones(u_angle.shape[0]), R*np.cos(v_angle))
    fig.add_surface(z=z_dir, x=x_dir, y=y_dir, colorscale=[[0, clor], [1, clor]], opacity=1.0, showlegend=False, lighting=dict(diffuse=0.1)) # opacity=fig.sphere_alpha, colorscale=[[0, fig.sphere_color], [1, fig.sphere_color]])
        

def plot_polygon(poly):
    
    xy_coords = poly.exterior.coords.xy
    lon = np.array(xy_coords[0])
    lat = np.array(xy_coords[1])
    
    lon = lon * np.pi/180
    lat = lat * np.pi/180
    
    R = 6378.134
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)
    
    return x, y, z

def plot_orbit() :
    angle = np.linspace(0, 2.0*np.pi, 144)
    R = 6878.134
    x = R*np.cos(angle)
    y = R*np.sin(angle)
    z = np.zeros(144)
    
    return x, y, z

# Read the shapefile.  Creates a DataFrame object
gdf = gpd.read_file("ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp")
fig = go.Figure()
plot_front(fig)
plot_back(fig)

marker = dict(color=[f'rgb({np.random.randint(0,256)}, {np.random.randint(0,256)}, {np.random.randint(0,256)})' for _ in range(25)],
           size=10)

for i in gdf.index :
    # print(gdf.loc[i].NAME)            # Call a specific attribute
    
    polys = gdf.loc[i].geometry         # Polygons or MultiPolygons
    
    if polys.geom_type == 'Polygon':
        x, y, z = plot_polygon(polys)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color=f'rgb(0, 0,0)'), showlegend=False) )
        
    elif polys.geom_type == 'MultiPolygon':
        
        for poly in polys.geoms:
            x, y, z = plot_polygon(poly)
            fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color=f'rgb(0, 0,0)'), showlegend=False) )
            


def draw_circle_on_sphere(p:float, a:float, radius:float):
    '''
        Parametric equation determined by the radius and angular positions (both polar and azimuthal relative to the z-axis) of the circle on the spherical surface
        Parameters:
            p (float): polar angle
            a (float): azimuthal angle
            radius (float): radius of the circle
            
        Returns:
            Circular scatter points on a spherical surface
    '''
    v = asin(radius/6371)
    u = np.mgrid[0:2*np.pi:30j]
    
    x = (np.sin(v)*np.cos(p)*np.cos(a)*np.cos(u) + np.cos(v)*np.sin(p)*np.cos(a) - np.sin(v)*np.sin(a)*np.sin(u))*6418.134
    y = (np.sin(v)*np.cos(p)*np.sin(a)*np.cos(u) + np.cos(v)*np.sin(p)*np.sin(a) + np.sin(v)*np.cos(a)*np.sin(u))*6418.134
    z = -np.sin(v)*np.sin(p)*np.cos(u)*6418.134 + np.cos(v)*np.cos(p)*6418.134
    
    return x, y, z



def cities_coord(lon, lats):
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
        x = math.cos(lat_rad) * math.cos(lon_rad)*6418.134
        y = math.cos(lat_rad) * math.sin(lon_rad)*6418.134
        z = math.sin(lat_rad)*6418.134
        x_coords.append(x)
        y_coords.append(y)
        z_coords.append(z)
    return x_coords, y_coords, z_coords

def plot_cities(lons, lats):
    '''
        Place the cities on the spherical surface
                
            lons (list of floats): longitude of the cities
            lats (list of floats): latitude of the cities
            
        Returns:
            None
    '''
    x, y, z = cities_coord(lats, lons)
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', line=dict(color=f'rgb(255, 0,0)', width = 10), showlegend=False ) )
    
def plot_satellite(pol, azi, rad):
    '''
        Place the satellite on the spherical surface
        
            pol (list of floats): polar angles of the satellite
            a (list of floats): azimuthal angles of the satellite
            radius (float): radius of the surface coverd by the satellite
        Returns:
            None
    '''    
    for p, a in zip(pol, azi):
        x, y, z = draw_circle_on_sphere(p, a, rad)
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines', line=dict(color=f'rgb(0, 0,255)', width = 10), showlegend=False) )


fig.write_html("3d_plot.html")
plot(fig)
