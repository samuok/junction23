from cmath import sqrt
import numpy as np
import math


# left_center = [19873, 6500, 10329, 15016, 16065, 16502]
# right_center = [25081, 6040, 8177, 13971, 14545, 8708]

def get_distance_unit_left(left_eye, index):
    left_units = [1 / 19873, 1 / 6500, 1 / 10329, 1 / 15016, 1 / 16065, 1 / 16502]
    ret = left_units[index] * left_eye[index]
    return ret


def get_distance_unit_right(right_eye, index):
    right_units = [1 / 25081, 1 / 6040, 1 / 8177, 1 / 13971, 1 / 14545, 1 / 8708]
    ret = right_units[index] * right_eye[index]
    return ret


def get_point_dist(point1, point2):
    x = point1[0] - point2[0]
    y = point1[1] - point2[1]
    mag = sqrt(x * x + y * y)
    return mag


def get_angle(a, b, c):
    if a + b > c and a + c > b and b + c > a:
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
        return angle
    return "false"


def get_the_direction_vector_left(point1, point2, angle):
    x = point2[0] - point1[0]
    y = point2[1] - point1[1]
    mag = sqrt(x * x + y * y)
    x /= mag
    y /= mag
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])
    rotated_vector = np.dot(rotation_matrix, [x, y])
    return np.real(rotated_vector)


def get_point_left(point1, point2, a, b):
    c = np.real(get_point_dist(point1, point2))
    angle = get_angle(a, b, c)
    if angle == "false":
        return 0, 0
    angle = -angle
    vec = get_the_direction_vector_left(point1, point2, angle)
    xDist = vec[0] * a
    yDist = vec[1] * a
    ret = [point1[0] + xDist, point1[1] + yDist]
    return ret


def get_point_right(point1, point2, a, b):
    c = np.real(get_point_dist(point1, point2))
    angle = get_angle(a, b, c)
    if angle == "false":
        return 0, 0
    vec = get_the_direction_vector_left(point1, point2, angle)
    xDist = vec[0] * a
    yDist = vec[1] * a
    ret = [point1[0] + xDist, point1[1] + yDist]
    return ret


def get_left_average(left_eye_coords):
    val1 = get_point_left([0.950433, 0.310754], [1, 0], left_eye_coords[0], left_eye_coords[1])
    val2 = get_point_left([0.950433, 0.310754], [0.950433, -0.310754], left_eye_coords[0], left_eye_coords[2])
    val3 = get_point_left([1, 0], [0.950433, -0.310754], left_eye_coords[1], left_eye_coords[2])
    val4 = get_point_right([-0.950433, 0.310754], [-1, 0], left_eye_coords[3], left_eye_coords[4])
    val5 = get_point_right([-0.950433, 0.310754], [-0.950433, -0.310754], left_eye_coords[3], left_eye_coords[5])
    val6 = get_point_right([-1, 0], [-0.950433, -0.310754], left_eye_coords[4], left_eye_coords[5])
    x = val1[0] + val2[0] + val3[0] + val4[0] + val5[0] + val6[0]
    y = val1[1] + val2[1] + val3[1] + val4[1] + val5[1] + val6[1]
    x /= 6
    y /= 6
    return x, y


def get_right_average(right_eye_coords):
    val1 = get_point_right([-0.950433, 0.310754], [-1, 0], right_eye_coords[0], right_eye_coords[1])
    val2 = get_point_right([-0.950433, 0.310754], [-0.950433, -0.310754], right_eye_coords[0], right_eye_coords[2])
    val3 = get_point_right([-1, 0], [-0.950433, -0.310754], right_eye_coords[1], right_eye_coords[2])
    val4 = get_point_left([0.950433, 0.310754], [1, 0], right_eye_coords[3], right_eye_coords[4])
    val5 = get_point_left([0.950433, 0.310754], [0.950433, -0.310754], right_eye_coords[3], right_eye_coords[5])
    val6 = get_point_left([1, 0], [0.950433, -0.310754], right_eye_coords[4], right_eye_coords[5])
    x = val1[0] + val2[0] + val3[0] + val4[0] + val5[0] + val6[0]
    y = val1[1] + val2[1] + val3[1] + val4[1] + val5[1] + val6[1]
    x /= 6
    y /= 6
    return x, y


def get_eye_directions(left_eye, right_eye):
    left_eye_coords = [get_distance_unit_left(left_eye, 0), get_distance_unit_left(left_eye, 1),
                       get_distance_unit_left(left_eye, 2), get_distance_unit_left(left_eye, 5),
                       get_distance_unit_left(left_eye, 4), get_distance_unit_left(left_eye, 3)]
    right_eye_coords = [get_distance_unit_right(right_eye, 0), get_distance_unit_right(right_eye, 1),
                        get_distance_unit_right(right_eye, 2), get_distance_unit_right(right_eye, 5),
                        get_distance_unit_right(right_eye, 4), get_distance_unit_right(right_eye, 3)]
    left_point = get_left_average(left_eye_coords)
    right_point = get_right_average(right_eye_coords)
    return left_point, right_point


def vector_angle(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    cosine_angle = dot_product / magnitude_product
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
    angle_radians = np.arccos(cosine_angle)
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees


def get_angles(left_eye, right_eye):
    ret = get_eye_directions(left_eye, right_eye)
    angle1 = vector_angle(ret[0], [0, 1])
    if ret[0][0] < 0:
        angle1 = -angle1
    angle2 = vector_angle(ret[1], [0, 1])
    if ret[1][0] < 0:
        angle2 = -angle2
    return (angle1, angle2)


def get_magnitudes(left_eye, right_eye):
    points = get_eye_directions(left_eye, right_eye)
    mag1 = sqrt(points[0][0] * points[0][0] + points[0][1] * points[0][1])
    mag2 = sqrt(points[1][0] * points[1][0] + points[1][1] * points[1][1])
    return (mag1, mag2)


def get_left_dir(left_eye, right_eye):
    ret = get_angles(left_eye, right_eye)
    angle = ret[0]
    if abs(angle) < 22.5:
        return "up"
    if angle >= 22.5 and angle < 67.5:
        return "up right"
    if angle >= 67.5 and angle < 112.5:
        return "right"
    if angle >= 112.5 and angle < 157.5:
        return "down right"
    if abs(angle) >= 157.5:
        return "down"
    if angle <= 22.5 and angle > -67.5:
        return "up left"
    if angle <= -67.5 and angle > 112.5:
        return "left"
    return "down left"


def get_right_dir(left_eye, right_eye):
    ret = get_angles(left_eye, right_eye)
    angle = ret[1]
    if abs(angle) < 22.5:
        return "up"
    if angle >= 22.5 and angle < 67.5:
        return "up right"
    if angle >= 67.5 and angle < 112.5:
        return "right"
    if angle >= 112.5 and angle < 157.5:
        return "down right"
    if abs(angle) >= 157.5:
        return "down"
    if angle <= 22.5 and angle > -67.5:
        return "up left"
    if angle <= -67.5 and angle > 112.5:
        return "left"
    return "down left"


def get_dir_strings(left_eye, right_eye):
    mags = get_magnitudes(left_eye, right_eye)
    mags = np.real(mags)
    leftSet = False
    rightSet = False
    ret = ["left", "left"]
    if mags[0] < 0.055:
        ret[0] = "straight"
        leftSet = True
    if mags[1] < 0.055:
        ret[0] = "straight"
        rightSet = True
    if rightSet and leftSet:
        return ret
    if not leftSet:
        ret[0] = get_left_dir(left_eye, right_eye)
    if not rightSet:
        ret[1] = get_right_dir(left_eye, right_eye)
    return ret
