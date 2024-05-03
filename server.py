from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import spherical_satellites_repartition as ssr
import numpy as np
import plot_map
from utilities import *
from generate_data import write_file
import os

app = Flask(__name__)

cors = CORS(app, resources={r"/compute": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/plot')
def plot():
    return render_template('temp_plot.html')

@app.route('/compute', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type'])
def compute():
    request_data = request.get_json()
    N_satellites, cities_gps, cities_weights, format, R, H, P, I_necessary, alpha, verbose = request_data.values()

    N_satellites = int(N_satellites)
    N_cities = len(cities_gps)
    cities_gps = np.c_[np.ones(N_cities)*R, np.array(cities_gps).astype(np.float64)]
    cities_spherical = gps2spher(cities_gps)
    cities_weights = np.array(cities_weights).astype(np.float64)
    
    write_file("csv_data", cities_weights, cities_gps.T[1], cities_gps.T[2])
    satellites_gps, cost = ssr.spherical_satellites_repartition(N_satellites=N_satellites, file_name="csv_data")
    #satellites_spherical, cost = ssr.spherical_satellites_repartition(int(N_satellites), cities_spherical[:, 1:], cities_weights, format, R, H, P, I_necessary, alpha, verbose) 
    satellites_spherical = gps2spher(satellites_gps)
    plot_map.create_fig()
    plot_map.plot_cities(cities_spherical, cities_weights)
    plot_map.plot_satellite(satellites_spherical, 3500)
    filename = "temp_plot.html"
    plot_map.plot_fig("templates/" + filename, auto_open=False)
    return {'content': filename, 'cost': cost()}

if __name__ == '__main__':
    app.run(host="0.0.0.0")