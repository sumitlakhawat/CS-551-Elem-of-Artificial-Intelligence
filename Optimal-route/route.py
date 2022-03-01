#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Rajdeep Singh Chauhan rajchauh, Shruti Padole spadole, Sumit Lakhawat slakhawa
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import copy
from math import tanh
from math import sin, cos, sqrt, atan2, radians
from queue import PriorityQueue


def get_response(route):
    route_taken = [
        (segment[1], segment[5] + " for " + segment[2] + " miles") for segment in route
    ]
    total_miles = 0
    total_hours = 0
    total_delivery_hours = 0

    for segment in route:
        total_miles += float(segment[2])
        total_hours += float(segment[4])
        total_delivery_hours += float(segment[4])
        if int(segment[3]) >= 50:
            total_delivery_hours += tanh(float(segment[2]) / 1000) * 2 * total_hours
    return {
        "total-segments": len(route_taken),
        "total-miles": total_miles,
        "total-hours": total_hours,
        "total-delivery-hours": total_delivery_hours,
        "route-taken": route_taken,
    }


def get_delivery_hours(length, speed, tot_time, node_time):
    return (
        (tanh(length / 1000) * 2 * tot_time) + node_time if speed >= 50 else node_time
    )


def get_route(start, end, cost):
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    (segments, max_speed) = load_all_segments()
    cities = load_all_cities()

    if cost == "segments":
        return get_response(
            get_route_by_segments(
                start, end, copy.deepcopy(segments), copy.deepcopy(cities)
            )
        )

    elif cost == "distance":
        return get_response(
            get_route_by_distance(
                start, end, copy.deepcopy(segments), copy.deepcopy(cities)
            )
        )

    elif cost == "time":
        return get_response(
            get_route_by_time(
                start, end, copy.deepcopy(segments), copy.deepcopy(cities), max_speed
            )
        )

    elif cost == "delivery":
        return get_response(
            get_route_by_delivery(
                start, end, copy.deepcopy(segments), copy.deepcopy(cities), max_speed
            )
        )


def load_all_cities():
    cities = {}
    with open("city-gps.txt", "r") as file:
        for line in file:
            [city, lat, lon] = line.split(" ")
            cities[city] = [lat, lon[:-1]]
    return cities


def load_all_segments():
    segments = {}
    max_speed = 1
    with open("road-segments.txt", "r") as file:
        for line in file:
            [source, destination, length, speed, name] = line.split(" ")
            max_speed = max_speed if max_speed >= int(speed) else int(speed)
            if source in segments:
                segments[source] += [
                    {
                        "destination": destination,
                        "value": [
                            source,
                            destination,
                            length,
                            speed,
                            int(length) / int(speed),
                            name[:-1],
                        ],
                    }
                ]
            else:
                segments[source] = [
                    {
                        "destination": destination,
                        "value": [
                            source,
                            destination,
                            length,
                            speed,
                            int(length) / int(speed),
                            name[:-1],
                        ],
                    }
                ]

            if destination in segments:
                segments[destination] += [
                    {
                        "destination": source,
                        "value": [
                            destination,
                            source,
                            length,
                            speed,
                            int(length) / int(speed),
                            name[:-1],
                        ],
                    }
                ]
            else:
                segments[destination] = [
                    {
                        "destination": source,
                        "value": [
                            destination,
                            source,
                            length,
                            speed,
                            int(length) / int(speed),
                            name[:-1],
                        ],
                    }
                ]

    return (segments, max_speed)


def get_route_by_segments(source, destination, segments, cities):
    q = PriorityQueue()
    visited_nodes = []
    for segment in segments[source]:
        h_cost = 0
        if segment["value"][1] in cities:
            h_cost = calculate_distance_between_coordinates(
                cities[segment["value"][1]], cities[destination]
            )
        else:
            h_cost = calculate_distance_between_coordinates(
                cities[segment["value"][0]], cities[destination]
            ) - float(segment["value"][2])

        q.put(
            (
                h_cost,
                (
                    float(segment["value"][2]),
                    segment["value"],
                    [segment["value"]],
                    h_cost,
                ),
            )
        )
    while not q.empty():
        h_s, (g_s, segment, value, h_cost) = q.get()
        visited_nodes += [segment[0] + segment[1] + segment[5]]
        if segment[1] == destination:
            return value
        for path in segments[segment[1]]:
            if (
                path["value"][0] + path["value"][1] + path["value"][5]
                not in visited_nodes
            ):
                if path["value"][1] in cities:
                    q.put(
                        (
                            g_s
                            + calculate_distance_between_coordinates(
                                cities[path["value"][1]], cities[destination]
                            ),
                            (
                                g_s + float(path["value"][2]),
                                path["value"],
                                value + [path["value"]],
                                calculate_distance_between_coordinates(
                                    cities[path["value"][1]], cities[destination]
                                ),
                            ),
                        )
                    )

                else:
                    q.put(
                        (
                            g_s + h_cost - float(path["value"][2]),
                            (
                                g_s + float(path["value"][2]),
                                path["value"],
                                value + [path["value"]],
                                h_cost - float(path["value"][2]),
                            ),
                        )
                    )


def get_route_by_distance(source, destination, segments, cities):
    q = PriorityQueue()
    visited_nodes = []
    for segment in segments[source]:
        h_cost = 0
        if segment["value"][1] in cities:
            h_cost = calculate_distance_between_coordinates(
                cities[segment["value"][1]], cities[destination]
            ) + float(segment["value"][2])
        else:
            h_cost = calculate_distance_between_coordinates(
                cities[segment["value"][0]], cities[destination]
            )

        q.put(
            (
                h_cost,
                (
                    float(segment["value"][2]),
                    segment["value"],
                    [segment["value"]],
                    h_cost - float(segment["value"][2]),
                ),
            )
        )

    while not q.empty():
        h_s, (g_s, segment, value, h_cost) = q.get()
        visited_nodes += [segment[0] + segment[1] + segment[5]]
        if segment[1] == destination:
            return value
        for path in segments[segment[1]]:
            if (
                path["value"][0] + path["value"][1] + path["value"][5]
                not in visited_nodes
            ):
                if path["value"][1] in cities:
                    q.put(
                        (
                            g_s
                            + calculate_distance_between_coordinates(
                                cities[path["value"][1]], cities[destination]
                            )
                            + float(path["value"][2]),
                            (
                                g_s + float(path["value"][2]),
                                path["value"],
                                value + [path["value"]],
                                calculate_distance_between_coordinates(
                                    cities[path["value"][1]], cities[destination]
                                ),
                            ),
                        ),
                    )

                else:
                    q.put(
                        (
                            g_s + h_cost,
                            (
                                g_s + float(path["value"][2]),
                                path["value"],
                                value + [path["value"]],
                                h_cost - float(path["value"][2]),
                            ),
                        )
                    )


def get_route_by_time(source, destination, segments, cities, max_speed):
    q = PriorityQueue()
    visited_nodes = []
    for segment in segments[source]:
        h_cost = 0
        if segment["value"][1] in cities:
            h_cost = (
                calculate_distance_between_coordinates(
                    cities[segment["value"][1]], cities[destination]
                )
                / max_speed
            ) + segment["value"][4]
        else:
            h_cost = (
                calculate_distance_between_coordinates(
                    cities[segment["value"][0]], cities[destination]
                )
                / max_speed
            )

        q.put(
            (
                h_cost,
                (
                    segment["value"][4],
                    segment["value"],
                    [segment["value"]],
                    h_cost - segment["value"][4],
                ),
            )
        )

    while not q.empty():
        h_s, (g_s, segment, value, h_cost) = q.get()
        visited_nodes += [segment[0] + segment[1] + segment[5]]
        if segment[1] == destination:
            return value
        for path in segments[segment[1]]:
            if (
                path["value"][0] + path["value"][1] + path["value"][5]
                not in visited_nodes
            ):
                if path["value"][1] in cities:
                    q.put(
                        (
                            g_s
                            + (
                                calculate_distance_between_coordinates(
                                    cities[path["value"][1]], cities[destination]
                                )
                                / max_speed
                            )
                            + path["value"][4],
                            (
                                g_s + path["value"][4],
                                path["value"],
                                value + [path["value"]],
                                calculate_distance_between_coordinates(
                                    cities[path["value"][1]], cities[destination]
                                )
                                / max_speed,
                            ),
                        ),
                    )

                else:
                    q.put(
                        (
                            g_s + h_cost,
                            (
                                g_s + path["value"][4],
                                path["value"],
                                value + [path["value"]],
                                h_cost - path["value"][4],
                            ),
                        )
                    )


def get_route_by_delivery(source, destination, segments, cities, max_speed):
    q = PriorityQueue()
    visited_nodes = []
    max_speed = 50
    for segment in segments[source]:
        h_cost = 0
        if segment["value"][1] in cities:
            h_distance_cost = calculate_distance_between_coordinates(
                cities[segment["value"][1]], cities[destination]
            )
            h_cost = get_delivery_hours(
                h_distance_cost,
                max_speed,
                get_delivery_hours(
                    float(segment["value"][2]),
                    int(segment["value"][3]),
                    segment["value"][4],
                    segment["value"][4],
                )
                + h_distance_cost / max_speed,
                h_distance_cost / max_speed,
            ) + get_delivery_hours(
                float(segment["value"][2]),
                int(segment["value"][3]),
                segment["value"][4],
                segment["value"][4],
            )
        else:
            h_distance_cost = calculate_distance_between_coordinates(
                cities[segment["value"][0]], cities[destination]
            )
            h_cost = get_delivery_hours(
                h_distance_cost,
                max_speed,
                h_distance_cost / max_speed,
                h_distance_cost / max_speed,
            )

        q.put(
            (
                h_cost,
                (
                    get_delivery_hours(
                        float(segment["value"][2]),
                        int(segment["value"][3]),
                        segment["value"][4],
                        segment["value"][4],
                    ),
                    segment["value"],
                    [segment["value"]],
                    h_cost
                    - get_delivery_hours(
                        float(segment["value"][2]),
                        int(segment["value"][3]),
                        segment["value"][4],
                        segment["value"][4],
                    ),
                ),
            )
        )
    while not q.empty():
        h_s, (g_s, segment, value, h_cost) = q.get()
        visited_nodes += [segment[0] + segment[1] + segment[5]]
        if segment[1] == destination:
            return value
        for path in segments[segment[1]]:
            if (
                path["value"][0] + path["value"][1] + path["value"][5]
                not in visited_nodes
            ):
                if path["value"][1] in cities:
                    delivery_distance = calculate_distance_between_coordinates(
                        cities[path["value"][1]], cities[destination]
                    )
                    h_delivery_time = get_delivery_hours(
                        delivery_distance,
                        max_speed,
                        g_s + (delivery_distance / max_speed) + get_delivery_hours(
                        float(path["value"][2]),
                        int(path["value"][3]),
                        g_s + float(path["value"][4]),
                        float(path["value"][4])),
                        delivery_distance / max_speed,
                    )
                    delivery_time = get_delivery_hours(
                        float(path["value"][2]),
                        int(path["value"][3]),
                        g_s + float(path["value"][4]),
                        float(path["value"][4]),
                    )
                    q.put(
                        (
                            g_s + h_delivery_time + delivery_time,
                            (
                                g_s + delivery_time,
                                path["value"],
                                value + [path["value"]],
                                h_delivery_time,
                            ),
                        ),
                    )

                else:
                    q.put(
                        (
                            g_s + h_cost,
                            (
                                g_s
                                + get_delivery_hours(
                                    float(path["value"][2]),
                                    int(path["value"][3]),
                                    g_s + float(path["value"][4]),
                                    float(path["value"][4]),
                                ),
                                path["value"],
                                value + [path["value"]],
                                h_cost
                                - get_delivery_hours(
                                    float(path["value"][2]),
                                    int(path["value"][3]),
                                    g_s + float(path["value"][4]),
                                    float(path["value"][4]),
                                ),
                            ),
                        )
                    )


# Referenced from https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def calculate_distance_between_coordinates(c1, c2):
    # approximate radius of earth in miles
    R = 3958.8

    lat1 = radians(float(c1[0]))
    lon1 = radians(float(c1[1]))
    lat2 = radians(float(c2[0]))
    lon2 = radians(float(c2[1]))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])


