import json
import os
import geopy.distance
from geopy.distance import great_circle
import sys
from scipy.spatial import KDTree


class BusRoute:

    def __init__(self, route_name: str, price: float, points=None):
        if points is None:
            points = []
        self.route_name = route_name
        self.price = price
        self.points: list[tuple] = points

    def __str__(self):
        return f'Bus route:: Name: {self.route_name}, Price: {self.price}, Points: {len(self.points)}'


class RouteManger:

    __ROUTES: list[BusRoute] = []

    @staticmethod
    def load_points() -> list[BusRoute]:
        """
        Returns a list of BusRoute objects
        :return: list[BusRoute]
        """

        if len(RouteManger.__ROUTES) > 0:
            print('Routes already loaded...')
            return RouteManger.__ROUTES

        print('Loading routes')
        files = os.listdir('routes/')

        json_data = []

        for file in files:
            with open(f'routes/{file}', 'r') as json_file:
                json_data.append(json.load(json_file))

        for json_object in json_data:
            route_name = json_object['name']
            price = json_object['price']
            points = json_object['points']

            bus_route = BusRoute(route_name, price)

            for point in points:
                lat = point['lat']
                lon = point['lon']
                bus_route.points.append((lat, lon))

            RouteManger.__ROUTES.append(bus_route)

        del json_data, files
        return RouteManger.__ROUTES

    @staticmethod
    def build_kd_tree(routes):
        points = [(lat, lon) for route in routes for lat, lon in route.points]
        kdtree = KDTree(points)
        return kdtree

    @staticmethod
    def find_best_route(origin: tuple, dest: tuple):

        routes: list[BusRoute] = RouteManger.load_points()
        origin_distance = sys.maxsize
        dest_distance = sys.maxsize

        best_route_origin = None
        best_route_dest = None

        for route in routes:
            for point in route.points:
                dist_origin = geopy.distance.distance(point, origin)
                dist_dest = geopy.distance.distance(point, dest)

                if dist_origin < origin_distance:
                    origin_distance = dist_origin
                    best_route_origin = route.route_name

                if dist_dest < dest_distance:
                    dest_distance = dist_dest
                    best_route_dest = route.route_name

        print(f'Origin:: Route: {best_route_origin}, Distance: {origin_distance}')
        print(f'Dest:: Route: {best_route_dest}, Distance: {dest_distance}')

    @staticmethod
    def find_best(origin, dest, kdtree: KDTree):
        _, origin_idx = kdtree.query(origin)
        _, dest_idx = kdtree.query(dest)

        routes = RouteManger.__ROUTES
        origin_route = routes[origin_idx // len(routes)]
        dest_route = routes[dest_idx // len(routes)]

        print(f"Origin:: Route: {origin_route.route_name}, "
              f"Distance: {great_circle(origin, origin_route.points[origin_idx % len(routes)]).meters}")
        print(f'Dest:: Route: {dest_route.route_name}, '
              f'Distance: {great_circle(dest, dest_route.points[dest_idx % len(routes)]).meters}')
