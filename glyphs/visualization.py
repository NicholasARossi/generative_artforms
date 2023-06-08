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

    for i,kernal in  enumerate(glyph_path.kernals[:-2]):
        x, y = zip(*kernal.shape_points)

        if kernal.rotation == 'ccw':
            ax[0].fill(x,y,color = '#ff8888')
        else:
            ax[0].fill(x, y, color='darkturquoise')
        ax[0].annotate(i,(kernal.center_point[0],kernal.center_point[1]))
    ax[0].set_xlim([-1, size + 1.5])
    ax[0].set_ylim([-1, size + 1.5])

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


    ax[1].plot(x_trace,y_trace,color='red')

    ax[1].set_xlim([-1, size+1.5])
    ax[1].set_ylim([-1, size+1.5])
    fine_x = []
    fine_y =[]
    counter = 0
    for x,y in glyph_path.all_path_points :
        fine_x.append(x)
        fine_y.append(y)
        ax[1].annotate(counter, (x, y))
        counter +=1

    ax[1].plot(fine_x,fine_y,color='#d3d3d3')
    ax[1].scatter(fine_x,fine_y,color='#d3d3d3')


    ax[2].fill(fine_x,fine_y,color='#d3d3d3')
    ax[2].set_xlim([-1, size+1.5])
    ax[2].set_ylim([-1, size+1.5])

    ax[0].set_title('kernals with rotation')
    ax[1].set_title('path points')
    ax[2].set_title('fill')
    if save_location:
        fig.savefig(save_location,dpi=300,bbox_inches='tight')

    return fig

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

def render_multipath_fill(glyphs,
                          save_location,
                          annotate=False,
                          width_height_ratio =1,
                          color_profile = 'RdYlBu_r'):
    # size = np.shape(glyphs[0].all_path_points)[0]
    static_offset = 5
    num_cols = np.ceil(np.sqrt(len(glyphs))*width_height_ratio)
    fig, ax = plt.subplots(figsize=(num_cols,len(glyphs)/num_cols ))
    ax.set_xlim([-.5, static_offset*num_cols+2])

    ax.set_ylim([-.5, static_offset*len(glyphs)/num_cols+2])

    row_number = 0
    column_number = 0
    cm = plt.cm.get_cmap(color_profile)
    for i, glyph in enumerate(glyphs):
        column_number = i%num_cols
        if column_number ==0 and i!=0:
            row_number +=1

        x_offset = column_number*static_offset
        y_offset = row_number*static_offset
        x,y = zip(*glyph.all_path_points)
        x = [x_val+x_offset for x_val in x]
        y = [y_val+y_offset for y_val in y]
        x.append(x[0])
        y.append(y[0])
        if annotate:
            ax.annotate(i, (x_offset, y_offset))


        ax.fill(x, y, color=cm(i))

    plt.axis('off')
    ax.margins(x=0)
    ax.margins(y=0)
    if save_location:
        fig.savefig(save_location,bbox_inches='tight',pad_inches=0)

    return fig

def render_multipath_lines(glyphs, save_location, annotate=False,width_height_ratio =1):
    # size = np.shape(glyphs[0].all_path_points)[0]
    static_offset = 5
    num_cols = np.ceil(np.sqrt(len(glyphs))*width_height_ratio)
    fig, ax = plt.subplots(figsize=(num_cols,len(glyphs)/num_cols ))
    ax.set_xlim([-.5, static_offset*num_cols+2])

    ax.set_ylim([-.5, static_offset*len(glyphs)/num_cols+2])


    row_number = 0
    column_number = 0

    for i, glyph in enumerate(glyphs):
        column_number = i%num_cols
        if column_number ==0 and i!=0:
            row_number +=1

        x_offset = column_number*static_offset
        y_offset = row_number*static_offset
        x,y = zip(*glyph.all_path_points)
        x = [x_val+x_offset for x_val in x]
        y = [y_val+y_offset for y_val in y]
        x.append(x[0])
        y.append(y[0])
        if annotate:
            ax.annotate(i, (x_offset, y_offset))

        ax.plot(x, y, color='#d3d3d3')

    plt.axis('off')
    ax.margins(x=0)
    ax.margins(y=0)
    if save_location:
        fig.savefig(save_location,bbox_inches='tight',pad_inches=0)
    return fig
