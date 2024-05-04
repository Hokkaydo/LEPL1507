from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import spherical_satellites_repartition as ssr
import numpy as np
import plot_map
from utilities import *
import uuid
import os
from threading import Timer  


app = Flask(__name__)

cors = CORS(app, resources={r"/compute": {"origins": "*"}})
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/plot/<id>")
def plot(id):
    return render_template(f"tmp/plot_{id}.html")


@app.route("/compute", methods=["POST"])
@cross_origin(origin="*", headers=["Content-Type"])
def compute():
    request_data = request.get_json()

    (
        N_satellites,
        csv,
        cities,
        weights,
        R,
        optimize_decided,
        optimize_locally,
        csv_content,
    ) = request_data.values()

    N_satellites = int(N_satellites)
    N_cities = len(cities)
    cities = np.c_[np.ones(N_cities) * R, np.array(cities).astype(np.float64)]

    weights = np.array(weights).astype(np.float64)

    if csv:
        with open("csv_data.csv", "w") as f:
            import base64

            f.write(base64.b64decode(csv_content).decode("utf-8"))
        (satellites_gps, cost), coverage = (
            ssr.spherical_satellites_repartition(
                N_satellites=N_satellites,
                file_name="csv_data.csv",
                optimisation_decided=optimize_decided,
                optimize=optimize_locally,
            ),
            ssr.problem.coverage(),
        )
    else:
        (satellites_gps, cost), coverage = (
            ssr.spherical_satellites_repartition_gps(
                N_satellites, cities, weights, optimize=optimize_locally
            ),
            ssr.problem.coverage(),
        )

    cities = ssr.problem.cities_coordinates
    weights = ssr.problem.cities_weights

    satellites_spherical = gps2spher(satellites_gps)
    
    plot_map.create_fig()
    plot_map.plot_cities(gps2spher(cities), weights)
    plot_map.plot_satellite(satellites_spherical, 4511)
    
    id = str(uuid.uuid4())
    filename = "templates/tmp/plot_" + id + ".html"
    plot_map.plot_fig(filename, auto_open=False)
    set_timeout(lambda: os.remove(filename), 30)
    
    return {"coverage": f"{coverage * 100 :.2f}", "cost": cost(), "id": id}
     
def set_timeout(fn, time, *args, **kwargs): 
    t = Timer(time, fn, args=args, kwargs=kwargs) 
    t.start() 
    return t 

if __name__ == "__main__":
    app.run(host="0.0.0.0")
