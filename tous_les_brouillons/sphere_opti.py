import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as so
import kmeans

# DATA
r = 6371 # [km] mean radius of Earth
R = r + 35786 # [km] geostationary height
theta = np.deg2rad(5) # Angle of covering of a satellite
cos_theta = np.cos(theta) # cosinus of this angle
max_dist = R*cos_theta - np.sqrt((R**2)*(cos_theta**2) - R**2 + r**2) # maximal distance at which a satellite has an impact

I_ok = (10**((-67-30)/10))*1e4 # Intensity required to satisfy perfectly 10 000 residents
Pt = 50 # Transmission power of a satellite

n_cit = 50 # Number of cities
n_sat = 10 # Number of satellites

# FIGURE
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Sphere https://stackoverflow.com/questions/31768031/plotting-points-on-the-surface-of-a-sphere
phi, theta = np.meshgrid(np.linspace(0, 2*np.pi, 1000), np.linspace(0, np.pi, 1000))
x = r*np.sin(theta)*np.cos(phi)
y = r*np.sin(theta)*np.sin(phi)
z = r*np.cos(theta)
ax.plot_surface(x, y, z, linewidth=0, color='lightskyblue', alpha=0.3)

# Initialization of cities
cities = []
for i in range (n_cit) :
    phi = np.random.rand() * 2*np.pi
    theta = np.random.rand() * np.pi
    cities.append([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])
cities = r * np.array(cities)
cities_weights = np.random.randint(1, 100, n_cit)


print(f"Maximal intensity required is {np.sum(cities_weights)*I_ok}")
ax.scatter(cities[:,0], cities[:,1], cities[:,2], color='purple', label="Cities")

# Initialization of satellites
satellites = []
for i in range (n_sat) :
    phi = np.random.rand() * 2*np.pi
    theta = np.random.rand() * np.pi
    satellites.append([phi, theta])
satellites = np.array(satellites)
#ax.scatter(r*np.sin(satellites[:,1])*np.cos(satellites[:,0]), r*np.sin(satellites[:,1])*np.sin(satellites[:,0]), r*np.cos(satellites[:,1]), color='red', label="Initial position of satellites")
satellites = np.reshape(satellites, 2*len(satellites))

# Cost function
cities_cost = np.zeros(n_cit)
def cost(satellites) :
    satellites = np.reshape(satellites, (n_sat, 2))
    for satellite in satellites : cost_satellite(satellite)
    for i in range (n_cit) :
        cities_cost[i] = min(cities_cost[i], I_ok)
    return -np.sum(cities_cost)

def cost_satellite(satellite) :
    # satellite is in spherical coordinates (only phi, theta ; r is known)
    phi = satellite[0]; theta = satellite[1]
    x = R*np.sin(theta)*np.cos(phi)
    y = R*np.sin(theta)*np.sin(phi)
    z = R*np.cos(theta)
    coord = np.array([x, y, z])

    for i, city in enumerate(cities) :
        dist = np.linalg.norm(city - coord)
        if (dist < max_dist) :
            cities_cost[i] += Pt/(2*np.pi*dist**2*(1-cos_theta))

# Optimization
print (f"Initial cost of satellites is {-cost(satellites)}")

for method in ["Powell", "Nelder-Mead", "Powell"] :
    old_satellites = np.copy(satellites)
    print(method)
    res = so.minimize(cost, satellites, method=method, bounds=so.Bounds(0, 2*np.pi)) # Change bounds for theta
    result = np.reshape(res.x, (len(satellites)//2, 2))
    if (not res.success) : print(f"Error : {res.message}")
    else : print(f"Everything went successfully ! Message : {res.message}")
    print(f"Cost after optimization is {-cost(res.x)}")
    satellites = old_satellites
"""ax.scatter(r*np.sin(result[:,1])*np.cos(result[:,0]), r*np.sin(result[:,1])*np.sin(result[:,0]), r*np.cos(result[:,1]), color='lawngreen', label = "Optimal position of the satellites")
ax.set_aspect('equal')
plt.tight_layout()
plt.legend()
plt.show()"""
#res = so.minimize(cost, satellites, method='Nelder-Mead', bounds=so.Bounds(0, 2*np.pi)) # Change bounds for theta
#result = np.reshape(res.x, (len(satellites)//2, 2))
result = kmeans.spherical_kmeans(cities, [], N_satellites=n_sat)*r
#if (not res.success) : print(f"Error : {res.message}")
#else : print(f"Everything went successfully ! Message : {res.message}")
#print(f"Cost after optimization is {-cost(res.x)}")
ax.scatter(r*np.sin(result[:,1])*np.cos(result[:,0]), r*np.sin(result[:,1])*np.sin(result[:,0]), r*np.cos(result[:,1]), color='lawngreen', label = "Optimal position of the satellites")

ax.set_aspect('equal')
plt.tight_layout()
plt.legend()
plt.show()
