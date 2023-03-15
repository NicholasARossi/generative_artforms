import rtree


class PathIndex:
    def __init__(self, path_graph):
        self.idx = rtree.index.Index()
        self.path_graph = path_graph
        for index, coordinate in path_graph.iter_starts_with_index():
            self.idx.add(index, coordinate + coordinate)

    def get_nearest(self, coordinate):
        return next(self.idx.nearest(coordinate))

    def delete(self, index):
        coordinate = self.path_graph.get_coordinates(index)
        self.idx.delete(index, coordinate + coordinate)

    def delete_pair(self, index):
        self.delete(index)
        self.delete(self.path_graph.get_disjoint(index))

def greedy_walk(path_graph):
    path_index = PathIndex(path_graph)
    location = path_graph.get_coordinates(path_graph.ORIGIN)
    while True:
        try:
            next_point = path_index.get_nearest(location)
        except StopIteration:
            break
        location = path_graph.get_coordinates(next_point, True)
        path_index.delete_pair(next_point)
        yield next_point


from collections import Counter


def check_valid_solution(solution, graph):
    """Check that the solution is valid: every path is visited exactly once."""
    expected = Counter(
        i for (i, _) in graph.iter_starts_with_index()
        if i < graph.get_disjoint(i)
    )
    actual = Counter(
        min(i, graph.get_disjoint(i))
        for i in solution
    )

    difference = Counter(expected)
    difference.subtract(actual)
    difference = {k: v for k, v in difference.items() if v != 0}
    if difference:
        print('Solution is not valid!'
              'Difference in node counts (expected - actual): {}'.format(difference))
        return False
    return True


def get_route_from_solution(solution, graph):
    """Converts a solution (a list of node indices) into a list
    of paths suitable for rendering."""

    # As a guard against comparing invalid "solutions",
    # ensure that this solution is valid.
    assert check_valid_solution(solution, graph)

    return [graph.get_path(i) for i in solution]
