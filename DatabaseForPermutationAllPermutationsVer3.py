"""
                                        Unified 3D Orientation for Cubes
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

        SYMBOLS FOR CUBE's CORNERS:                                     COORDINATES DIRECTION:
          p1                     p2
            * * * * * * * * * *                                               Oz  ^
           *                 **                                                   *
          *                 * *                                                   *
      p4 *             p3  *  *                                                   *
        * * * * * * * * * *   *                                                   *
        *   X-----        *   *                                                   *
        *  |  p5          *  *  p6                                                *  *  *  *  *  * >  Oy
        * |               * *                                                    *
        *                 **                                                    *
        * * * * * * * * * *                                                    *
      p8                   p7                                                 *
                                                                             v
                                                                        Ox
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math
from copy import deepcopy
import json




# If DATA_SCALE from MarchingCubeVer2 != None, SIDE = 1
SIDE = 1
HALF_SIDE = SIDE/2


PERMUTATIONS = {

}


"""
ORIGINAL_CASE: For Cube side length = 2
Dictionary
keys = list of strings of given points inside object (remember that the name is in increasing order, i.e p1, p2, p3, p5, ..)
values = list of tuples as adjust for triangles, each with 3 tuples as 3 points to make a triangle, 
each has 3 elements as adjust for (x,y,z) coordinates of a point 
which are the update coordinates to get points on plane for drawing.

Example: given ('p3') for the case of normal cube (which is point (2,2,2), return [((-1,0,0),(0,-1,0),(0,0,-1))]
=> 
(2,2,2) + (-1,0,0) = (1,2,2) = first point on marching cube plane
(2,2,2) + (0,-1,0) = (2,1,2) = second point on marching cube plane
(2,2,2) + (0,0,-1) = (2,2,1) = third point on marching cube plane

Represent key of dict for multiple points: 'p1_p2_p3_p5',...

value of this dict represents adjustment to corresponding original point to get 3 points of triangle which lies
on  marching cube plane
"""
ORIGINAL_CASE = {
    "p5": [((-HALF_SIDE, -HALF_SIDE, 0), (0, -HALF_SIDE, -HALF_SIDE), (-HALF_SIDE, 0, -HALF_SIDE))],
    "p5_p6": [((-HALF_SIDE, -HALF_SIDE, 0),(0, -HALF_SIDE, -HALF_SIDE), (-HALF_SIDE, HALF_SIDE, 0)),
              ((-HALF_SIDE, HALF_SIDE, 0), (0, -HALF_SIDE, -HALF_SIDE), (0, HALF_SIDE, -HALF_SIDE))],
    "p2_p5": [((-HALF_SIDE, HALF_SIDE, 0), (0, HALF_SIDE, HALF_SIDE), (-HALF_SIDE, 0, HALF_SIDE)),
              ((-HALF_SIDE, -HALF_SIDE, 0), (0, -HALF_SIDE, -HALF_SIDE), (-HALF_SIDE, 0, -HALF_SIDE))],
    "p3_p5": [((-HALF_SIDE, -HALF_SIDE, 0), (0, -HALF_SIDE, -HALF_SIDE), (-HALF_SIDE, 0, -HALF_SIDE)),
              ((HALF_SIDE, HALF_SIDE, 0), (HALF_SIDE, 0, HALF_SIDE), (0, HALF_SIDE, HALF_SIDE))],
    "p5_p6_p7": [((-HALF_SIDE, -HALF_SIDE, 0), (0, -HALF_SIDE, -HALF_SIDE), (HALF_SIDE, HALF_SIDE, 0)),
                 ((HALF_SIDE, HALF_SIDE, 0), (0, -HALF_SIDE, -HALF_SIDE), (HALF_SIDE, 0, -HALF_SIDE)),
                 ((HALF_SIDE, HALF_SIDE, 0), (-HALF_SIDE, -HALF_SIDE, 0), (-HALF_SIDE, HALF_SIDE, 0))],
    "p2_p7_p8": [((0, -HALF_SIDE, -HALF_SIDE), (HALF_SIDE, -HALF_SIDE, 0), (0, HALF_SIDE, -HALF_SIDE)),
                 ((HALF_SIDE, HALF_SIDE, 0), (0, HALF_SIDE, -HALF_SIDE), (HALF_SIDE, -HALF_SIDE, 0)),
                 ((-HALF_SIDE, 0, HALF_SIDE), (-HALF_SIDE, HALF_SIDE, 0), (0, HALF_SIDE, HALF_SIDE))],
    "p2_p4_p7": [((0, HALF_SIDE, -HALF_SIDE), (HALF_SIDE, 0, -HALF_SIDE), (HALF_SIDE, HALF_SIDE, 0)),
                 ((HALF_SIDE, -HALF_SIDE, 0), (0, -HALF_SIDE, HALF_SIDE), (HALF_SIDE, 0, HALF_SIDE)),
                 ((-HALF_SIDE, 0, HALF_SIDE), (-HALF_SIDE, HALF_SIDE, 0), (0, HALF_SIDE, HALF_SIDE))],
    "p5_p6_p7_p8": [((-HALF_SIDE, -HALF_SIDE, 0), (HALF_SIDE, -HALF_SIDE, 0), (-HALF_SIDE, HALF_SIDE, 0)),
                    ((-HALF_SIDE, HALF_SIDE, 0), (HALF_SIDE, -HALF_SIDE, 0), (HALF_SIDE, HALF_SIDE, 0))],
    "p4_p5_p6_p7": [((-HALF_SIDE, -HALF_SIDE, 0), (0, -HALF_SIDE, -HALF_SIDE), (HALF_SIDE, HALF_SIDE, 0)),
                    ((HALF_SIDE, HALF_SIDE, 0), (0, -HALF_SIDE, -HALF_SIDE), (HALF_SIDE, 0, -HALF_SIDE)),
                    ((-HALF_SIDE, -HALF_SIDE, 0), (HALF_SIDE, HALF_SIDE, 0), (-HALF_SIDE, HALF_SIDE, 0)),
                    ((HALF_SIDE, -HALF_SIDE, 0), (0, -HALF_SIDE, HALF_SIDE), (HALF_SIDE, 0, HALF_SIDE))],
    "p1_p3_p6_p8": [((0, -HALF_SIDE, -HALF_SIDE), (HALF_SIDE, -HALF_SIDE, 0), (HALF_SIDE, 0, -HALF_SIDE)),
                    ((0, HALF_SIDE, -HALF_SIDE), (-HALF_SIDE, HALF_SIDE, 0), (-HALF_SIDE, 0, -HALF_SIDE)),
                    ((0, -HALF_SIDE, HALF_SIDE), (-HALF_SIDE, -HALF_SIDE, 0), (-HALF_SIDE, 0, HALF_SIDE)),
                    ((HALF_SIDE, HALF_SIDE, 0), (HALF_SIDE, 0, HALF_SIDE), (0, HALF_SIDE, HALF_SIDE))],
    "p1_p5_p6_p8": [((0, HALF_SIDE, -HALF_SIDE), (-HALF_SIDE, HALF_SIDE, 0), (HALF_SIDE, 0, -HALF_SIDE)),
                    ((HALF_SIDE, 0, -HALF_SIDE), (-HALF_SIDE, HALF_SIDE, 0), (-HALF_SIDE, 0, HALF_SIDE)),
                    ((HALF_SIDE, 0, -HALF_SIDE), (-HALF_SIDE, 0, HALF_SIDE), (HALF_SIDE, -HALF_SIDE, 0)),
                    ((HALF_SIDE, -HALF_SIDE, 0), (-HALF_SIDE, 0, HALF_SIDE), (0, -HALF_SIDE, HALF_SIDE))],
    "p1_p5_p6_p7": [((HALF_SIDE, HALF_SIDE, 0), (-HALF_SIDE, HALF_SIDE, 0), (HALF_SIDE, 0, -HALF_SIDE)),
                    ((HALF_SIDE, 0, -HALF_SIDE), (-HALF_SIDE, HALF_SIDE, 0), (0, -HALF_SIDE, HALF_SIDE)),
                    ((HALF_SIDE, 0, -HALF_SIDE), (0, -HALF_SIDE, HALF_SIDE), (0, -HALF_SIDE, -HALF_SIDE)),
                    ((-HALF_SIDE, HALF_SIDE, 0), (-HALF_SIDE, 0, HALF_SIDE), (0, -HALF_SIDE, HALF_SIDE))],
    "p2_p5_p6_p8": [((0, HALF_SIDE, -HALF_SIDE), (0, HALF_SIDE, HALF_SIDE), (HALF_SIDE, 0, -HALF_SIDE)),
                    ((HALF_SIDE, 0, -HALF_SIDE), (0, HALF_SIDE, HALF_SIDE), (-HALF_SIDE, -HALF_SIDE, 0)),
                    ((HALF_SIDE, 0, -HALF_SIDE), (-HALF_SIDE, -HALF_SIDE, 0), (HALF_SIDE, -HALF_SIDE, 0)),
                    ((-HALF_SIDE, -HALF_SIDE, 0), (0, HALF_SIDE, HALF_SIDE), (-HALF_SIDE, 0, HALF_SIDE))],
    "p2_p4_p6_p8": [((0, -HALF_SIDE, -HALF_SIDE), (0, -HALF_SIDE, HALF_SIDE), (HALF_SIDE, 0, -HALF_SIDE)),
                    ((HALF_SIDE, 0, HALF_SIDE), (HALF_SIDE, 0, -HALF_SIDE), (0, -HALF_SIDE, HALF_SIDE)),
                    ((0, HALF_SIDE, -HALF_SIDE), (0, HALF_SIDE, HALF_SIDE), (-HALF_SIDE, 0, HALF_SIDE)),
                    ((-HALF_SIDE, 0, HALF_SIDE), (-HALF_SIDE, 0, -HALF_SIDE), (0, HALF_SIDE, -HALF_SIDE))]

}

"""
Mapping basic cube coordinates to string. Basic cube has side-length = 2, and draw from origin (p5 = (0,0,0))
"""
MAPPING = {
    "p1" : (-1*HALF_SIDE, -1*HALF_SIDE, 1*HALF_SIDE),
    "p2" : (-1*HALF_SIDE, 1*HALF_SIDE, 1*HALF_SIDE),
    "p3" : (1*HALF_SIDE, 1*HALF_SIDE, 1*HALF_SIDE),
    "p4" : (1*HALF_SIDE, -1*HALF_SIDE, 1*HALF_SIDE),
    "p5" : (-1*HALF_SIDE, -1*HALF_SIDE, -1*HALF_SIDE),
    "p6" : (-1*HALF_SIDE, 1*HALF_SIDE, -1*HALF_SIDE),
    "p7" : (1*HALF_SIDE, 1*HALF_SIDE, -1*HALF_SIDE),
    "p8" : (1*HALF_SIDE, -1*HALF_SIDE, -1*HALF_SIDE),
    "mid" : (0, 0, 0)
}



REVERSE_MAPPING = {(-HALF_SIDE, -HALF_SIDE, HALF_SIDE): 'p1',
                   (-HALF_SIDE, HALF_SIDE, HALF_SIDE): 'p2',
                   (HALF_SIDE, HALF_SIDE, HALF_SIDE): 'p3',
                   (HALF_SIDE, -HALF_SIDE, HALF_SIDE): 'p4',
                   (-HALF_SIDE, -HALF_SIDE, -HALF_SIDE): 'p5',
                   (-HALF_SIDE, HALF_SIDE, -HALF_SIDE): 'p6',
                   (HALF_SIDE, HALF_SIDE, -HALF_SIDE): 'p7',
                   (HALF_SIDE, -HALF_SIDE, -HALF_SIDE): 'p8',
                   (0,0,0): 'mid'
}

def create_cube_from_midpoint(mid_point):
    """
    create p1 -> p8 from mid_point
    :param mid_point:
    :return:
    """
    lis = list(MAPPING.values())
    lis = [(i[0] + mid_point[0], i[1] + mid_point[1], i[2] + mid_point[2]) for i in lis]
    return lis



def draw_normal_cube(mid_point):
    """
    draw corners and edges of a basic cube (side = 2, p5 = Origin)

    :return:
    """

    lis = create_cube_from_midpoint(mid_point)
    # print(lis)
    # print("mid is: ",mid_point)
    # print("side is: ",SIDE)
    # print("half-side is: ",HALF_SIDE)
    lis_keys = list(MAPPING.keys())
    # scatter points
    fig = plt.figure(figsize=(15, 8))
    ax = fig.add_subplot(111, projection='3d')
    for point in range(len(lis)):
        ax.scatter(lis[point][0], lis[point][1], lis[point][2], c= "green")
        ax.text  (lis[point][0], lis[point][1], lis[point][2],
                f"{lis_keys[point]} {lis[point][0], lis[point][1], lis[point][2]}")

    # Set coordinates size so that it does not draw the rectangle
    ax.set_xlim(mid_point[0] - HALF_SIDE, mid_point[0] + HALF_SIDE)
    ax.set_ylim(mid_point[1] - HALF_SIDE, mid_point[1] + HALF_SIDE)
    ax.set_zlim(mid_point[2] - HALF_SIDE, mid_point[2] + HALF_SIDE)

    # draw lines:
    draw_lines_between(lis[0:4] + [lis[0]])
    draw_lines_between(lis[4:8] + [lis[4]])
    draw_lines_between([lis[0], lis[4]])
    draw_lines_between([lis[1], lis[5]])
    draw_lines_between([lis[2], lis[6]])
    draw_lines_between([lis[3], lis[7]])



def draw_lines_between(points):
    """
    Given a set of points, connect them with lines
    :param points:
    :return:
    """
    X = [point[0] for point in points]
    Y = [point[1] for point in points]
    Z = [point[2] for point in points]
    plt.plot(X, Y, Z, linestyle='solid', color='green')


def create_triangle(key, mid_point):
    """
    From a mid_point coordinates and the points inside (input of marching cube)
    We'll create triangles that cut the cubes

    :param mid_point: tuple 3 elements - coordinates of mid_point. Ex: (1, 1, 1)
    :param key: string - the points inside the cube. Ex: "p5_p6"

    :return: List of triangles

    Ex:
    adjust = ORIGINAL_CASE[key] = ORGINAL_CASE["p5_p6"]
    = [((HALF_SIDE, 0, 0), (0, SIDE, HALF_SIDE), (0, 0, HALF_SIDE)),
              ((HALF_SIDE, 0, 0), (HALF_SIDE, -1 * SIDE, 0), (0, 0, HALF_SIDE))]
    return = list of triangles = [((a,b,c), (a,b,c), (a,b,c)), ((a,b,c), (a,b,c), (a,b,c)), ((a,b,c), (a,b,c), (a,b,c))]
    """
    adjust = PERMUTATIONS[key]
    list_of_triangles = []
    for tri in adjust:
        temp = []
        for vertex in tri:
            temp.append((mid_point[0] + vertex[0], mid_point[1] + vertex[1], mid_point[2] + vertex[2]))
        list_of_triangles.append((temp[0], temp[1], temp[2]))
    return list_of_triangles


def get_coordinates_from_keys(look_up_key, mid_point):
    """
    Given look_up_keys, for ex "p5_p6", and mid_point coordinates, for ex (1, 1, 1),
    return the list of coordinates of look-up-keys.

    :param look_up_key: string
    :param mid_point: tuple 3 elements
    :return: list
            Ex: [(0, 0, 0), (0, 1, 0)]
    """
    list_of_keys = look_up_key.split("_")
    key_coordinates = []
    adjust = [MAPPING[key] for key in list_of_keys]

    for point in adjust:
        key_coordinates.append((mid_point[0] + point[0], mid_point[1] + point[1], mid_point[2] + point[2]))
    return key_coordinates


def draw_triangle_and_hightlight_point_inside(look_up_key, mid_point):
    """
    From given look up key, we get coordinates of triangles for marching cube from look up table,
    draw triangles and highlight point in side, then plot them

    :param look_up_key: string - key of look up table. Ex: "p5_p6"
    :param mid_point: tuple 3 elements as midpoint. Ex: (1, 1, 1)
    :return: plot
    """
    key_coordinates = get_coordinates_from_keys(look_up_key, mid_point)

    # create triangles
    lis_of_triangles = create_triangle(look_up_key, mid_point)
    draw_triangles(lis_of_triangles)
    # highlight original point inside:
    highlight_points_inside(key_coordinates)

def draw_triangles(lis_of_triangles):
    """

    :param lis_of_triangles:
    :return:
    """
    ax = plt.gca()
    tri_object = Poly3DCollection(lis_of_triangles)
    tri_object.set_edgecolor("orange")
    tri_object.set_facecolor("orange")
    ax.add_collection(tri_object)

def highlight_points_inside(list_of_points):
    ax = plt.gca()
    for point in list_of_points:
        ax.scatter(point[0], point[1], point[2], c="red")



def rotate_axis(vector, axis, degree):
    """
    Rotates the given vector around the given axis, in given degree

    This functions calls rotate_Ox(), rotate_Oy() and rotate_Oz()

    :param key:
    :param mid_point:
    :param axis:
    :param rotation_degree:
    :return:
    """

    if axis == "Ox":
        return rotate_Ox(vector, degree)
    elif axis == "Oy":
        return rotate_Oy(vector, degree)
    elif axis == "Oz":
        return rotate_Oz(vector, degree)



def rotate_Ox(vector, degree):
    """
    Rotate a vector around Ox axis (only works for 90*n (n = integer) degrees.

    :param vector: numpy array as vector
    :param degree: integer.
    :return:
    """
    rotate = np.matrix([[1, 0, 0],
                        [0, int(math.cos(np.radians(degree))), int(-math.sin(np.radians(degree)))],
                        [0, int(math.sin(np.radians(degree))), int(math.cos(np.radians(degree)))]])
    return np.array(rotate*vector)


def rotate_Oy(vector, degree):
    """
    Rotate a vector around Oy axis (only works for 90*n (n = integer) degrees.

    :param vector: numpy array as vector
    :param degree:
    :return:
    """
    rotate = np.matrix([[int(math.cos(np.radians(degree))), 0, int(math.sin(np.radians(degree)))],
                        [0, 1, 0],
                        [int(-math.sin(np.radians(degree))), 0, int(math.cos(np.radians(degree)))]])
    return np.array(rotate*vector)

def rotate_Oz(vector, degree):
    """
    Rotate a vector around Oz axis (only works for 90*n (n = integer) degrees.

    :param vector: numpy array as vector
    :param degree:
    :return:
    """
    rotate = np.matrix([[int(math.cos(np.radians(degree))), int(-math.sin(np.radians(degree))), 0],
                        [int(math.sin(np.radians(degree))), int(math.cos(np.radians(degree))), 0],
                        [0, 0, 1]])
    return np.array(rotate*vector)

def to_vector(point):
    """
    Turn point into a vector

    :param point: tuple - (1, 1, 1)
    :return: np array - [[ 1]
                        [1]
                        [1]]
    """
    return np.array([[point[0]], [point[1]], [point[2]]])

def to_point(vector):
    """
    turn vector into point

    :param vector: np array - [[1], [1], [1]]


    :return: point - (1, 1, 1)
    """
    return (vector[0][0], vector[1][0], vector[2][0])


def rotate_triangle(list_of_tri, axis, degree):
    """
    Rotate the list of triangles around given axis in given degree

    This function calls rotate_axis()

    :param list_of_tri:
    :return:
    """
    a = [None for i in range(len(list_of_tri))]
    for i in range(len(list_of_tri)):
        a[i] = (to_point(rotate_axis(to_vector(list_of_tri[i][0]), axis, degree)),
                to_point(rotate_axis(to_vector(list_of_tri[i][1]), axis, degree)),
                to_point(rotate_axis(to_vector(list_of_tri[i][2]), axis, degree)))
    return a

def rotate_point(list_of_point, axis, degree):
    """
    Rotate a list of points around axis in degree

    :param list_of_point:
    :param axis:
    :param degree:
    :return:
    """
    a = [None for i in range(len(list_of_point))]
    for i in range(len(list_of_point)):
        a[i] = to_point(rotate_axis(to_vector(list_of_point[i]), axis, degree))
        # list_of_tri[i] = (to_point(rotate_axis(to_vector(list_of_tri[i][0]), axis, degree)),
        #         to_point(rotate_axis(to_vector(list_of_tri[i][1]), axis, degree)),
        #         to_point(rotate_axis(to_vector(list_of_tri[i][2]), axis, degree)))
    return a

def mirror_xy(vector):
    """

    :param vector:
    :return:
    """
    mirror = np.matrix([[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, -1]])
    return np.array(mirror * vector)


def mirror_yz(vector):
    """

    :param vector:
    :return:
    """
    mirror = np.matrix([[-1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1]])
    return np.array(mirror * vector)


def mirror_xz(vector):
    """

    :param vector:
    :return:
    """
    mirror = np.matrix([[1, 0, 0],
                        [0, -1, 0],
                        [0, 0, 1]])
    return np.array(mirror * vector)


def mirror_plane(vector, plane):
    """

    :param vector:
    :param plane:
    :return:
    """

    if plane == "xy":
        return mirror_xy(vector)
    elif plane == "yz":
        return mirror_yz(vector)
    elif plane == "xz":
        return mirror_xz(vector)


def mirror_triangle(list_of_tri, plane):
    """
    Rotate the list of triangles around given axis in given degree

    This function calls rotate_axis()

    :param list_of_tri:
    :return:
    """
    a = [None for i in range(len(list_of_tri))]
    for i in range(len(list_of_tri)):
        a[i] = (to_point(mirror_plane(to_vector(list_of_tri[i][0]), plane)),
                to_point(mirror_plane(to_vector(list_of_tri[i][1]), plane)),
                to_point(mirror_plane(to_vector(list_of_tri[i][2]), plane)))
    return a

def mirror_point(list_of_point, plane):
    """
    Rotate the list of triangles around given axis in given degree

    This function calls rotate_axis()

    :param list_of_tri:
    :return:
    """
    a = [None for i in range(len(list_of_point))]
    for i in range(len(list_of_point)):
        a[i] = to_point(mirror_plane(to_vector(list_of_point[i]), plane))
        # list_of_tri[i] = (to_point(mirror_plane(to_vector(list_of_tri[i][0]), plane)),
        #         to_point(mirror_plane(to_vector(list_of_tri[i][1]), plane)),
        #         to_point(mirror_plane(to_vector(list_of_tri[i][2]), plane)))
    return a

def invert_original_case():
    """

    :return:
    """
    all = {"p1", "p2", "p3", "p4", "p5", "p6", "p7", "p8"}

    temp_dict = [(key,deepcopy(val)) for key,val in ORIGINAL_CASE.items()]
    # print(temp_dict)
    for i in temp_dict:
        key = i[0]
        val = i[1]
        new_key = "_".join(sorted(list(all.difference(set(key.split("_"))))))
        # print("current is: ",key)
        # print("new is: ",new_key)
        # print()
        ORIGINAL_CASE[new_key] = val

def marching_cubes_permutation_rot():
    """
    THIS FUNCTION CALCULATES ALL POSSIBLE PERMUTATIONS FOR MARCHING CUBES ALGO.

    Given a pair of keys_values in original case look-up table, return its permutations through mirroring and rotating


    :param key: 2 element tuple = pair of key and value from ORIGINAL_CASE
    :return: list of 2 element tuples = pairs of key and value for permutation of ORIGINAL CASE

    Example:
    input: "p5": [((1, 0, 0), (0, 1, 0), (0, 0, 1))]
    output:
    [
     "p1": [((a, b, c), (d, e, f), (g, h, k)),
     "p2": ((a, b, c), (d, e, f), (g, h, k)),
     "p3": ((a, b, c), (d, e, f), (g, h, k)),
     "p4": ((a, b, c), (d, e, f), (g, h, k)),
     "p5": ((1, 0, 0), (0, 1, 0), (0, 0, 1))
                                            ]
    """
    mirror_planes = ["xy", "yz", "xz"]
    all_rotation_axis = ["Ox", "Oy", "Oz"]
    all_rotation_angle = [90, 180, 270]

    invert_original_case()


    for key,val in ORIGINAL_CASE.items():
        if PERMUTATIONS.get(key) == None:
            PERMUTATIONS[key] = val


        # ["p5", "p6"]
        original_key_string_list = key.split("_")

        # Coordinates of p5 and p6: [(-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5)]
        original_key_coor_list = [MAPPING[i] for i in original_key_string_list]


        # ORIGINALCASE["p5_p6"] = val

        # print("original_key_string_list is:",original_key_string_list)
        # print()
        # print("original_key_coor_list is:", original_key_coor_list)
        # print()

        for rot_ax_before_mir in all_rotation_axis:
            for rot_ang_before_mir in all_rotation_angle:
                rot_keys_coor_before_mir = rotate_point(original_key_coor_list, rot_ax_before_mir, rot_ang_before_mir)
                rot_keys_string_list_before_mir = [REVERSE_MAPPING[i] for i in rot_keys_coor_before_mir]

                new_k = "_".join(sorted(rot_keys_string_list_before_mir))
                new_v = rotate_triangle(val, rot_ax_before_mir,rot_ang_before_mir)

                # print("new_k: ",new_k)
                if PERMUTATIONS.get(new_k) == None:
                    PERMUTATIONS[new_k] = new_v
        #         print("rot_key_list rotate around",rot_ax_before_mir,"in",rot_ang_before_mir,"is: ",rot_keys_string_list_before_mir)
        #         print("rot_key_coor rotate around", rot_ax_before_mir, "in", rot_ang_before_mir, "is: ", rot_keys_coor_before_mir)
        #         print()
        # print()
        if len(original_key_string_list) == 3 or len(original_key_string_list) == 5:
            all_rotation_axis_new = ["Ox", "Oy"]
            all_rotation_angle_new = [90, 180, 270]
            for ang in all_rotation_angle_new:
                rot_keys_coor_before_mir_new = rotate_point(original_key_coor_list, "Oz",
                                                        ang)
                rot_keys_string_list_before_mir_new = [REVERSE_MAPPING[j] for j in rot_keys_coor_before_mir_new]

                new_k_oz = "_".join(sorted(rot_keys_string_list_before_mir_new))
                new_v_oz = rotate_triangle(val, "Oz", ang)

                # print("new_k: ",new_k)
                if PERMUTATIONS.get(new_k_oz) == None:
                    PERMUTATIONS[new_k_oz] = new_v_oz

                for rot_ax_before_mir in all_rotation_axis_new:
                    for rot_ang_before_mir in all_rotation_angle_new:
                        rot_keys_coor_before_mir = rotate_point(rot_keys_coor_before_mir_new, rot_ax_before_mir,
                                                                rot_ang_before_mir)
                        rot_keys_string_list_before_mir = [REVERSE_MAPPING[m] for m in rot_keys_coor_before_mir]

                        new_k = "_".join(sorted(rot_keys_string_list_before_mir))
                        new_v = rotate_triangle(new_v_oz, rot_ax_before_mir, rot_ang_before_mir)

                        # print("new_k: ",new_k)
                        if PERMUTATIONS.get(new_k) == None:
                            PERMUTATIONS[new_k] = new_v


        for mir in mirror_planes:
            mir_key_coor = mirror_point(original_key_coor_list, mir)
            mir_key_string_list = [REVERSE_MAPPING[i] for i in mir_key_coor]
            # print("mir_key_string_list is: ",mir_key_string_list)
            mir_key_string = "_".join(sorted(mir_key_string_list))

            mir_val_coor = mirror_triangle(val, mir)
            # print("mir_val_coor: ",mir_val_coor)
            marching_cubes_permutation_mir_and_rot(mir_key_string, mir_val_coor)

        mir_key_coor2 = mirror_point(original_key_coor_list, "xy")
        mir_key_coor2 = mirror_point(mir_key_coor2, "yz")
        mir_key_coor2 = mirror_point(mir_key_coor2, "xz")

        mir_key_string_list2 = [REVERSE_MAPPING[i] for i in mir_key_coor2]
        # print("mir_key_string_list is: ",mir_key_string_list)
        mir_key_string2 = "_".join(sorted(mir_key_string_list2))

        mir_val_coor2 = mirror_triangle(val, "xy")
        mir_val_coor2 = mirror_triangle(mir_val_coor2, "yz")
        mir_val_coor2 = mirror_triangle(mir_val_coor2, "xz")
        # print("mir_val_coor: ",mir_val_coor)
        marching_cubes_permutation_mir_and_rot(mir_key_string2, mir_val_coor2)




    # check = 3
    # count = 0
    # bol = False
    # # for tem_key in PERMUTATIONS.keys():
    # #     if len(tem_key.split("_")) == check:
    # #         count += 1
    # # print("number of point = ",check,":",count)
    #
    #
    # for keyt,valt in PERMUTATIONS.items():
    #     if len(keyt.split("_")) == check:
    #         count += 1
    #         print("Count: ",count)
    #         print("Case ", keyt, " value is: ", valt)
    #         print()
    #         if keyt == "p3_p4_p8":
    #             bol = True
    # print(bol)
    # if not bol:
    #     print("Key p3_p4_p8 not found")


def marching_cubes_permutation_mir_and_rot(key, val):
    all_rotation_axis = ["Ox", "Oy", "Oz"]
    all_rotation_angle = [90, 180, 270]

    if PERMUTATIONS.get(key) == None:
        PERMUTATIONS[key] = val

    # ["p5", "p6"]
    original_key_string_list = key.split("_")

    # Coordinates of p5 and p6: [(-0.5, -0.5, -0.5), (-0.5, 0.5, -0.5)]
    original_key_coor_list = [MAPPING[i] for i in original_key_string_list]

    # ORIGINALCASE["p5_p6"] = val

    # print("original_key_string_list is:", original_key_string_list)
    # print()
    # print("original_key_coor_list is:", original_key_coor_list)
    # print()
    for rot_ax_before_mir in all_rotation_axis:
        for rot_ang_before_mir in all_rotation_angle:
            rot_keys_coor_before_mir = rotate_point(original_key_coor_list, rot_ax_before_mir, rot_ang_before_mir)
            rot_keys_string_list_before_mir = [REVERSE_MAPPING[i] for i in rot_keys_coor_before_mir]

            new_k = "_".join(sorted(rot_keys_string_list_before_mir))
            new_v = rotate_triangle(val, rot_ax_before_mir, rot_ang_before_mir)

            # print("new_k: ",new_k)
            if PERMUTATIONS.get(new_k) == None:
                PERMUTATIONS[new_k] = new_v
    #         print("rot_key_list rotate around", rot_ax_before_mir, "in", rot_ang_before_mir, "is: ",
    #               rot_keys_string_list_before_mir)
    #         print("rot_key_coor rotate around", rot_ax_before_mir, "in", rot_ang_before_mir, "is: ",
    #               rot_keys_coor_before_mir)
    #         print()
    # print()
        # for mir_plane in mirror_planes:
    # print(PERMUTATIONS)

def permutation_256():
    marching_cubes_permutation_rot()
    PERMUTATIONS[""] = []
    PERMUTATIONS["p1_p2_p3_p4_p5_p6_p7_p8"] = []

def count_permutation_cases():
    for k,v in PERMUTATIONS.items():
        print("Case ",k," value is: ", v)
    print()
    print("Number of permutation cases: ",len(PERMUTATIONS))


if __name__ == "__main__":

    """
    UPDATING PERMUTATIONS
    """
    # NOT INCLUDING 0 AND 8 CASES:
    # marching_cubes_permutation_rot()

    # INCLUDING 0 AND 8 CASES:
    permutation_256()

    # total cases:
    count_permutation_cases()
    
    with open('permutations.txt',"w") as f:
        f.write(json.dumps(PERMUTATIONS))
    # print(PERMUTATIONS)


    """
    Drawing and testing original cases here
    
    Uncomment all lines at once to start testing
    """
    # LOOK_UP_KEY = "p2_p4_p6_p8"
    # MID_POINT = (0, 0, 0)
    # draw_normal_cube(MID_POINT)
    # draw_triangle_and_hightlight_point_inside(LOOK_UP_KEY, MID_POINT)




    """
    Drawing and testing rotation here
    
    Uncomment all lines at once to start testing
    """
    # MID_POINT = (0, 0, 0)
    # LOOK_UP_KEY = "p5_p6"
    # draw_normal_cube(MID_POINT)
    #
    # AXIS = "Oz"
    # DEGREE = 90
    # test = ORIGINAL_CASE[LOOK_UP_KEY]
    #
    # # Comment/ Uncomment the following line to test BEFORE and AFTER the transformation
    # # test = rotate_triangle(test, AXIS, DEGREE)
    # # test = rotate_triangle(test, AXIS, DEGREE)
    # # test = rotate_triangle(test, AXIS, DEGREE)
    # # test = rotate_triangle(test, AXIS, DEGREE)
    #
    # # comment out the following line to try for other thing
    # draw_triangles(test)


    """
    Drawing and testing mirroring here
    
    Uncomment all lines at once to start testing
    """
    # MID_POINT = (0, 0, 0)
    # LOOK_UP_KEY = "p2_p4_p6_p8"
    # draw_normal_cube(MID_POINT)
    # PLANE = "xy"
    # test = ORIGINAL_CASE[LOOK_UP_KEY]
    #
    # # Comment/ Uncomment the following line to test BEFORE and AFTER the transformation
    # # test = mirror_triangle(test, PLANE)
    #
    # draw_triangles(test)






    """
    Uncomment this to start drawing
    """


    # plt.show()
    
    # print(list(MAPPING.keys())[:-1])
    # a = {"p1", "p2", "p3"}
    # b = {"p2"}
    # print(sorted(list(a.difference(b))))
    # invert_original_case()