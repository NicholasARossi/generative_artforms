import matplotlib.pyplot as plt
import numpy as np
import math









def render_path(this_path):

    fig, ax = plt.subplots(figsize=(5, 5))
    size = np.shape(this_path)[0]
    x_vals_initial = np.arange(size)
    # generate coordinates
    x_vals = []
    y_vals = []

    # crete grid
    for i in range(size):
        x_vals.extend(x_vals_initial)
        x_vals_initial = [x + .5 for x in x_vals_initial]
        y_vals.extend([i * np.sin(np.deg2rad(60))] * size)
    ax.scatter(x_vals, y_vals)

    # trace path
    x_trace =[]
    y_trace =[]
    for i in range(int(np.max(this_path))):
        loc = np.argwhere(this_path==i+1)[0]
        x_trace.append(loc[0]+.5*loc[1])
        y_trace.append(loc[1] * np.sin(np.deg2rad(60)))

    x_trace.append(x_trace[0])
    y_trace.append(y_trace[0])

    ax.plot(x_trace,y_trace,color='red')

    ax.set_xlim([-1, size+1])
    ax.set_ylim([-1, size+1])

    fig.savefig('glyph_figures/my_glypy.png',dpi=300,bbox_inches='tight')
