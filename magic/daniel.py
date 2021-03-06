import googlemaps
import polyline
import sys
from pprint import pprint

EPSILON = sys.float_info.epsilon
gmaps = googlemaps.Client(key='AIzaSyCkF7rIDbq8WFxWv8i09_dpeTkf1ueXwRA')


def resize(inp, new_len):
    def interpolate(inp, fi):
        i = int(fi)
        f = fi - i
        return (inp[i] if f < EPSILON else
                inp[i] + f * (inp[i + 1] - inp[i]))

    delta = (len(inp) - 1) / float(new_len - 1)
    return [interpolate(inp, i * delta) for i in range(new_len)]

def gen_whole_arr(steps):
    poly_points = []
    seconds = 0

    for step in steps:

        encoded_path = step['polyline']['points']
        seconds += int(step['duration']['value'])
        poly_points += polyline.decode(encoded_path)

        # points = gmaps.elevation_along_path(encoded_path, 10)

    maped = list(zip(*poly_points))
    x_intered = resize(list(maped[0]), seconds)
    y_intered = resize(list(maped[1]), seconds)

    parsed = list(zip(x_intered, y_intered))
    return parsed, seconds


def new_route(points):
    """
    :param points: List of tuples [(x1,y1), (x2,y2), (x3,y3)] First is starting point, last destination
    :return: List of points, Nth index for Nth request. Number of seconds and route_polyline

    ----
        ((list_of_points, seconds), route_polyline)
    ----

    """
    start, end = points.pop(0), points.pop()
    response = gmaps.directions(start, end, waypoints=points,mode='driving', alternatives='false')
    return  gen_whole_arr(response[0]['legs'][0]['steps']), polyline.decode(response[0]['overview_polyline']['points'])

if __name__ == '__main__':
    pprint(new_route([ (51.2132, 19.2323), (52.2823, 19.9898)]))


"""
'overview polyline'
"""


