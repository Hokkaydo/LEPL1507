from flask import Flask, request
from flask_cors import CORS, cross_origin
import spherical_satellites_repartition as ssr
import numpy as np
import plot_map
from utilities import *
import os

app = Flask(__name__)

cors = CORS(app, resources={r"/compute": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/compute', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def compute():
    request_data = request.get_json()
    print(request_data)
    N_satellites, cities_coordinates, cities_weights, format, R, H, P, I_necessary, alpha, verbose = request_data.values()
    N_satellites = int(N_satellites)
    cities_coordinates = np.array(cities_coordinates).astype(np.float64)
    cities_spherical = cities_coordinates.copy()
    cities_spherical.T[0] += 180
    cities_spherical.T[1] += 90
    
    cities_spherical = lat_long_to_spherical(np.array(cities_coordinates).astype(np.float64))
    cities_weights = np.array(cities_weights).astype(np.float64)
    satellites_polar, cost = ssr.spherical_satellites_repartition(int(N_satellites), cities_spherical, cities_weights, format, R, H, P, I_necessary, alpha, verbose)
        
    satellites_long_lat = spherical_to_lat_long(satellites_polar)
    print(satellites_long_lat)
    plot_map.create_fig()
    plot_map.plot_cities(cities_coordinates.T[0], cities_coordinates.T[1], cities_weights)
    plot_map.plot_satellite_long_lat(*satellites_long_lat.T)
    filename = "temp_plot.html"
    plot_map.plot_fig(filename, auto_open=False)
    return {'content': os.path.abspath(filename), 'cost': cost()}

if __name__ == '__main__':
    app.run()