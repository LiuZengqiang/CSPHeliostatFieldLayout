#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon, Point


def getConvexHull(points):
    '''
    Calculate the legal limits of the target heliostat field (the convex hull of 'points').
    
    points: point set

    '''
    # Calculate the convex hull
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    # Create a Shapely Polygon from the convex hull points
    polygon = Polygon(hull_points)
    return polygon


def isPointInPolygon(point, polygon):
    '''
    Determine whether the point is within the legal heliostat field range.
    
    point: test heliostat position point
    polygon: the legal limits of the target heliostat field (the convex hull of base field)
    '''
    return polygon.contains(point)


def heliostatCollisionConstrain(test_helio, exist_helio_x, exist_helio_y, min_dis):
    '''
    Collision constrain of adjacent heliostats.
    Check whether the distance between the newly added heliostat (test_helio) and the existing heliostats ([exist_helio_x,exist_helio_y]) is too small.

    test_helio: coordinate of tested heliostat, (x,y)
    exist_helio_x, exist_helio_y: coordinate of existed heliostats, [(x,y), (x,y)..]
    min_dis: minimum safe distance of two adjacent heliostats' centre
    '''

    test_helio_x = test_helio[0]
    test_helio_y = test_helio[1]

    for i in range(len(exist_helio_x)-1, -1, -1):
        temp_helio_x = exist_helio_x[i]
        temp_helio_y = exist_helio_y[i]

        delta_x = test_helio_x - temp_helio_x
        delta_y = test_helio_y - temp_helio_y
        delta_dis_2 = delta_x * delta_x + delta_y*delta_y
        if (np.abs(delta_dis_2) <= min_dis * min_dis):
            return True
    return False

def biomimetic_fun(lm, wm, min_dis, phi, a, b):
    '''
    Generate a biomimetic-PS-like heliostat field, ref. <Noone, 2012, Heliostat Field Optimization: A New Computationally Efficient Model and Biomimetic Layout> and <Fernández, 2004, PS10: a 11.0-MWe Solar Tower Power Plant with Saturated Steam Receiver>
    lm: heliostat height, m
    wm: heliostat width, m
    min_dis: minimum safe distance of two adjacent heliostats' centre
    phi: golden ratio phi of eq.(14) in the first reference paper
    a: the coefficient a of eq.(15) in the first reference paper
    b: the coefficient b of eq.(15) in the first reference paper
    '''
    # 1. Load PS-10 layout as the base field range.
    input_file = open("./layout_PS10_base.csv", "r")
    is_head = True
    x_base = []
    y_base = []
    for _ in input_file.readlines():
        if (is_head):
            is_head = False
            continue
        t = _.strip()
        t = t.split(',')

        x_base.append(float(t[1]))
        y_base.append(float(t[2]))
    input_file.close()

    points = []
    base_r = 0.0
    for i in range(len(x_base)):
        points.append((x_base[i], y_base[i]))
        base_r = np.max([base_r, np.sqrt(x_base[i]*x_base[i]+y_base[i]*y_base[i])])

    points = np.array(points)
    base_heliostat_convex = getConvexHull(points)

    # 2. Generate biomimetic heliostat layout in the PS-10 base field range.
    x = []
    y = []
    cnt = 0
    i = 0
    temp_r = 0.0
    while temp_r <= base_r:

        i += 1
        theta = 2.0 * np.pi * np.power(phi, -2) * i
        r = a * np.power(i, b)
        xi = r * np.cos(theta)
        yi = r * np.sin(theta)

        point = Point((xi, yi))

        if (isPointInPolygon(point, base_heliostat_convex) and heliostatCollisionConstrain([xi, yi], x, y, min_dis) == False):
            x.append(xi)
            y.append(yi)
            cnt += 1
        temp_r = np.max([temp_r, r])
    x_polygon, y_polygon = base_heliostat_convex.exterior.xy
    plt.plot(x_polygon, y_polygon)
    plt.scatter(x, y, color='blue', marker='.', label='Heliostat')
    plt.show()

    output_file = open("layout.csv", "w")
    output_file.write("id,x,y,z\n")
    for i in range(len(x)):
        id = i + 1
        output_file.write(str(id)+","+str(x[i])+","+str(y[i])+","+"0.0\n")

    output_file.close()


if __name__ == "__main__":

    lm = 4.0  # heliostat length, m
    wm = 3.2  # heliostat width, m
    phi = (1.0 + np.sqrt(5.0))/2.0  # golden ratio phi
    # the coefficient a of eq.(15) in <Noone2012, Heliostat Field Optimization: A New Computationally Efficient Model and Biomimetic Layout>
    a = 4.5
    # the coefficient b of eq.(15) in <Noone2012, Heliostat Field Optimization: A New Computationally Efficient Model and Biomimetic Layout>
    b = 0.65

    min_dis = np.sqrt(lm*lm+wm*wm) * 1.5  # the min distance between two adjacent heliostats
    biomimetic_fun(lm, wm, min_dis, phi, a, b)
