import numpy as np
import matplotlib.pyplot as plt
from glyphs.core import determine_optional_moves, GlyphPath
from glyphs.visualization import render_path_fill
#

all_paths = []



def main(size):

    #todo randomize initial location
    initial_location = [0,0]
    path = np.zeros((size, size))
    path[initial_location[0], initial_location[1]] = 1
    explorer = GridExplorer()
    explorer.move(path)

    select_paths =  explorer.all_paths[:10]

    for i,path in enumerate(select_paths):

        rotations = np.random.choice(2,size**2).reshape((size,size))
        glyph_path = GlyphPath(path, rotations)
        glyph_path.run_all()
        render_path_fill(path,glyph_path.all_path_points,f'glyph_figures/{i}.png')

if __name__ == '__main__':

    # generate grid
    size = 3

    main(size)



    # # print(mypath.grid)
    #
    #
    # # print(mypath.current_location())
    #
    # # print('optional moves')
    # # print(mypath.determine_optional_moves())
    #
    # all_paths = []
    # move(mypath,first_move=True)
    #
    #
    # print(len(all_paths))
    #
    # # filter paths
    #
    #
    #
    # render_path(all_paths[0])


