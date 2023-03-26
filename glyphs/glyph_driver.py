import numpy as np
import matplotlib.pyplot as plt
#
# class Path:
#     def __init__(self,
#                  size,
#                  initial_location =[0,0],
#                  grid = None,
#                  current_location = None):
#         self.size = size
#         if grid is None:
#             self.grid = np.zeros((size, size))
#             self.grid[initial_location[0], initial_location[1]] = 1
#
#         else:
#             self.grid = grid
#             self.grid[current_location[0],current_location[1]] = np.max(self.grid)+1
#
#         self.initial_location = initial_location
#
#
#     def current_location(self):
#         return np.unravel_index(np.argmax(self.grid, axis=None), self.grid.shape)
#
#
#
#     def determine_optional_moves(self):
#         # all legal moves on the grid
#         current_location =  self.current_location()
#         optional_moves = []
#         visted_locs = set(tuple(x) for x in np.argwhere(mypath.grid != 0))
#
#         for (dx,dy) in [[0,1],[1,0],[-1,0],[0,-1],[1,1],[-1,-1],[-1,1],[1,-1]]:
#             px,py = current_location[0]+dx, current_location[1]+dy
#             # check to make sure we're on the board
#             if px>=0 and px<self.size and py>=0 and py<self.size:
#                 # if we're returning home that's ok
#                 if [px,py] == self.initial_location:
#                     optional_moves.append([px,py])
#                 else:
#                     #check to make sure we haven't been there before
#                     if (px,py) not in visted_locs:
#                         optional_moves.append([px, py])
#
#         return optional_moves
#
#     def compute_area(self):
#         pass
#
#     def compute_convexity(self):
#         pass
#



def get_current_location(path):
    return np.unravel_index(np.argmax(path, axis=None), path.shape)

def determine_optional_moves(path):
    current_location = get_current_location(path)
    initial_location = tuple(np.argwhere(path==1)[0])
    size = np.shape(path)[0]
    optional_moves = []
    visted_locs = set(tuple(x) for x in np.argwhere(path != 0))

    for (dx, dy) in [[0, 1], [1, 0], [-1, 0], [0, -1], [1, 1], [-1, -1], [-1, 1], [1, -1]]:
        px, py = current_location[0] + dx, current_location[1] + dy
        # check to make sure we're on the board
        if px >= 0 and px < size and py >= 0 and py < size:
            # if we're returning home that's ok
            if tuple([px, py]) == initial_location:
                optional_moves.append([px, py])
            else:
                # check to make sure we haven't been there before
                if (px, py) not in visted_locs:
                    optional_moves.append([px, py])

    return optional_moves




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



if __name__ == '__main__':
    # generate grid
    size = 2
    initial_location = [0,0]
    path = np.zeros((size, size))
    path[initial_location[0], initial_location[1]] = 1
    all_paths = []
    move(path)
    print(len(all_paths))
    render_path(all_paths[0])

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


