import googlemaps
import json
from pprint import pprint


start = (52.406376, 16.925167)
end = (52.229675, 21.012230)

gmaps = googlemaps.Client(key='AIzaSyCkF7rIDbq8WFxWv8i09_dpeTkf1ueXwRA')


def gen_whole_arr(steps):

    for step in steps:

        encoded_path = step['polyline']['points']
        num_of_seconds = int(step['duration']['value'])

        points = gmaps.elevation_along_path(encoded_path, 10)
        pprint(points)


def find_path(points):
    """
    :param points: List of tuples [(x1,y1), (x2,y2), (x3,y3)] First is starting point, last destination
    :return:
    """
    start, end = points.pop(0), points.pop()
    response = gmaps.directions(start, end, mode='driving', alternatives='false')
    # pprint(response)
    # print(type(response[0]['legs'][0]['steps']))
    gen_whole_arr(response[0]['legs'][0]['steps'])


"""
'overview polyline'
"""


find_path([start,end])




