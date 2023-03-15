import matplotlib.pyplot as plt
plt.style.use('bmh')


def dist(p1, p2):
    return abs(p1 - p2)

def cost_of_route(path, origin=0.+0j):
    # Cost from the origin to the start of the first path
    cost = dist(origin, path[0].start)
    # Cost between the end of each path and the start of the next
    cost += sum(
        dist(path[i].end, path[i+1].start) for i in range(len(path) - 1)
    )
    # Cost to return back to the origin
    cost += dist(path[-1].end, origin)
    return cost


def ink_transit_curve(route, origin=0. + 0.j, label=None):
    ink_distance = 0.
    transit_distance = 0.
    curve = list()
    last_end = origin

    for path in route:
        transit_distance += dist(last_end, path.start)
        ink_distance += path.length()
        curve.append((transit_distance, ink_distance))
        last_end = path.end
    transit_distance += dist(last_end, origin)
    curve.append((transit_distance, ink_distance))

    plt.plot(*zip(*curve), label=label)
    plt.xlabel('Pen-up travel distance')
    plt.ylabel('Ink on page')
