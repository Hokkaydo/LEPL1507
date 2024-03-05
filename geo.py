
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.offline import plot

fig = go.Figure()
size = 50
#Data Creation
d = {'Lat':np.random.randint(90,120,size),
 'Lon':np.random.randint(-180,180,size),
 'colorcode':np.random.randint(-40,20,size)}
df = pd.DataFrame(d)

fig.add_trace(go.Scattergeo(mode = "markers+lines",lon = df['Lon'],lat = df['Lat'],marker = {'size': 10,'color':df['colorcode'],'colorscale':'jet','colorbar_thickness':20}))
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
                    )
                )
)
plot(fig)
