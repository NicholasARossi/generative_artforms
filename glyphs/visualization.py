import matplotlib.pyplot as plt
import numpy as np

def render_skeleton(path):
    fig, ax = plt.subplots(figsize=(5, 5))
    size = np.shape(path)[0]
    x_vals_initial = np.arange(size)
    # generate coordinates
    x_vals = []
    y_vals = []
    # create grid
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
    plt.axis('off')

    return fig

def render_path_debug(glyph_path,
                save_location=None):

    fig, ax = plt.subplots(1,3,figsize=(15, 5))
    size = np.shape(glyph_path.grid_path)[0]
    x_vals_initial = np.arange(size)
    # generate coordinates
    x_vals = []
    y_vals = []

    # crete grid
    for i in range(size):
        x_vals.extend(x_vals_initial)
        x_vals_initial = [x + .5 for x in x_vals_initial]
        y_vals.extend([i * np.sin(np.deg2rad(60))] * size)

    ax[1].scatter(x_vals, y_vals)

    # trace path
    x_trace =[]
    y_trace =[]
    for i in range(int(np.max(glyph_path.grid_path))):
        loc = np.argwhere(glyph_path.grid_path==i+1)[0]
        x_trace.append(loc[0]+.5*loc[1])
        y_trace.append(loc[1] * np.sin(np.deg2rad(60)))

    x_trace.append(x_trace[0])
    y_trace.append(y_trace[0])

    ax[1].plot(x_trace,y_trace,color='red')

    ax[1].set_xlim([-1, size+1])
    ax[1].set_ylim([-1, size+1])
    fine_x = []
    fine_y =[]
    counter = 0
    for x,y in glyph_path.all_path_points :
        fine_x.append(x)
        fine_y.append(y)
        ax[1].annotate(counter, (x, y))
        counter +=1
    # complete the loop
    fine_x.append(fine_x[0])
    fine_y.append(fine_y[0])

    ax[1].plot(fine_x,fine_y,color='#d3d3d3')
    ax[1].scatter(fine_x,fine_y,color='#d3d3d3')


    ax[2].fill(fine_x,fine_y,color='#d3d3d3')
    ax[2].set_xlim([-1, size+1])
    ax[2].set_ylim([-1, size+1])

    if save_location:
        fig.savefig(save_location,dpi=300,bbox_inches='tight')



def render_path_fill(path,
                     all_points,
                save_location):

    fig, ax = plt.subplots(figsize=(5, 5))
    size = np.shape(path)[0]


    ax.set_xlim([-1, size+1])
    ax.set_ylim([-1, size+1])
    fine_x = []
    fine_y =[]
    for x,y in all_points:
        fine_x.append(x)
        fine_y.append(y)

    # complete the loop
    fine_x.append(fine_x[0])
    fine_y.append(fine_y[0])


    ax.fill(fine_x,fine_y,color='#d3d3d3')
    plt.axis('off')

    fig.savefig(save_location,dpi=300,bbox_inches='tight')

def render_multipath_fill(paths, save_location, annotate=False):
    size = np.shape(paths[0])[0]
    fig, ax = plt.subplots(figsize=(5, 5))

    ax.set_xlim([-1, np.sqrt(size)*np.sqrt(len(paths))+1])
    ax.set_ylim([-1, np.sqrt(size)*np.sqrt(len(paths))+1])
    num_cols = 5
    row_number = 0
    column_number = 0
    for i, path in enumerate(paths):
        column_number = i%num_cols
        if column_number ==0:
            row_number +=1

        x_offset = column_number*np.sqrt(size)
        y_offset = row_number*np.sqrt(size)
        x,y = zip(*path)
        x = [x_val+x_offset for x_val in x]
        y = [y_val+y_offset for y_val in y]
        x.append(x[0])
        y.append(y[0])
        if annotate:
            ax.annotate(i, (x_offset, y_offset))

        ax.fill(x, y, color='#d3d3d3')

    plt.axis('off')
    fig.savefig(save_location)
