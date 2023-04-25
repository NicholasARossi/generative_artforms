import numpy as np
import matplotlib.pyplot as plt
from glyphs.core import determine_optional_moves, GlyphPath
from glyphs.visualization import render_path_fill
#

all_paths = []


def move(path):

    optional_moves = determine_optional_moves(path)
    for optional_move in optional_moves:
        if tuple(optional_move) == tuple(np.argwhere(path==1)[0]):
            all_paths.append(path)
        else:
            # move to the location and recurse
            new_path = path.copy()
            new_path[optional_move[0],optional_move[1]] =np.max(new_path)+1
            move(new_path)


def main(size):

    #todo randomize initial location
    initial_location = [0,0]
    path = np.zeros((size, size))
    path[initial_location[0], initial_location[1]] = 1
    move(path)

    select_paths =  all_paths[:10]

    for i,path in enumerate(select_paths):
        #TODO randomize rotations
        try:
            rotations = np.random.choice(2,size**2).reshape((size,size))
            glyph_path = GlyphPath(path, rotations)
            glyph_path.add_kernals()
            all_points = glyph_path.follow_path()
            render_path_fill(path,all_points,f'glyph_figures/{i}.png')
        except:
            print('failure')
            print(path)
            print(rotations)
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


