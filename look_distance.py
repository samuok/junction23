import eye_directon as ed
import numpy as np


def map_on_spehere(x, y):
    r_squared = x ** 2 + y ** 2
    if r_squared > 1:
        return 1
    x1 = 2 * x / (1 + r_squared)
    y1 = 2 * y / (1 + r_squared)
    z1 = (r_squared - 1) / (1 + r_squared)
    return [x1, y1, z1]


def get_sphere_points(left_eye, right_eye):
    points = ed.get_eye_directions(left_eye, right_eye)
    l = map_on_spehere(points[0][0], points[0][1])
    r = map_on_spehere(points[1][0], points[1][1])
    l[2] = -l[2]
    r[2] = -r[2]
    return [l, r]


def closest_points_on_unit_vectors(vector1, vector2):
    normalized_vector1 = vector1 / np.linalg.norm(vector1)
    normalized_vector2 = vector2 / np.linalg.norm(vector2)
    dot_product = np.dot(normalized_vector1, normalized_vector2)
    point_on_vector1 = normalized_vector1 * dot_product
    point_on_vector2 = normalized_vector2 * dot_product
    return [point_on_vector1, point_on_vector2]


def get_look_distance_point(left_eye, right_eye):
    ret = get_sphere_points(left_eye, right_eye)
    closest_points = closest_points_on_unit_vectors(ret[0], ret[1])
    x = closest_points[0][0] + closest_points[1][0]
    y = closest_points[0][1] + closest_points[1][1]
    z = closest_points[0][2] + closest_points[1][2]
    x /= 2
    y /= 2
    z /= 2
    return [x, y, z]


def vec_magnitude(point1, point2):
    x = point2[0] - point1[0]
    y = point2[1] - point1[1]
    z = point2[2] - point1[2]
    mag = np.sqrt(x * x + y * y + z * z)
    return mag


def get_distance(total_mag):
    unit = 40 / 0.04316024849332165
    dist = unit * total_mag
    return dist


def get_look_distance(left_eye, right_eye):
    point = get_look_distance_point(left_eye, right_eye)
    ret = get_sphere_points(left_eye, right_eye)
    mag1 = vec_magnitude(ret[0], point)
    mag2 = vec_magnitude(ret[1], point)
    total = (mag1 + mag2) / 2
    return (get_distance(total))
