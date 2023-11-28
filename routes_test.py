from models.route_manager import RouteManger
import time

origin = (-7.150614065902453, -78.50582393347317)
dest = (-7.16390451810081, -78.4648772070873)


def own_function():
    RouteManger.load_points()
    start_time = time.process_time()
    RouteManger.find_best_route(origin, dest)
    end_time = time.process_time()

    execution_time = end_time - start_time
    print("CPU time:", execution_time, "seconds")


def kdtree_usage():
    routes = RouteManger.load_points()
    print(f'Routes loaded: {len(routes)}')
    kdtree = RouteManger.build_kd_tree(routes)
    print(f'KDTree built')
    RouteManger.find_best(origin, dest, kdtree)


kdtree_usage()