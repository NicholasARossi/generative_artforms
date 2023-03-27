import matplotlib.pyplot as plt
import numpy as np


def render_path_debug(path,all_points,
                save_location):

    fig, ax = plt.subplots(figsize=(5, 5))
    size = np.shape(path)[0]
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
    for i in range(int(np.max(path))):
        loc = np.argwhere(path==i+1)[0]
        x_trace.append(loc[0]+.5*loc[1])
        y_trace.append(loc[1] * np.sin(np.deg2rad(60)))

    x_trace.append(x_trace[0])
    y_trace.append(y_trace[0])

    ax.plot(x_trace,y_trace,color='red')

    ax.set_xlim([-1, size+1])
    ax.set_ylim([-1, size+1])
    fine_x = []
    fine_y =[]
    counter = 0
    for x,y in all_points:
        fine_x.append(x)
        fine_y.append(y)
        ax.annotate(counter, (x, y))
        counter +=1
    ax.plot(fine_x,fine_y,color='#d3d3d3')
    ax.scatter(fine_x,fine_y,color='#d3d3d3')


    fig.savefig(save_location,dpi=300,bbox_inches='tight')
