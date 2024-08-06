#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt


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


def biomimetic_fun(target_num, lm, wm, min_dis, phi, a, b):
    '''
    Generate a biomimetic-surround heliostat field, ref. <Noone2012, Heliostat Field Optimization: A New Computationally Efficient Model and Biomimetic Layout>

    target_num: target number of heliostats in the generated heliostat layout
    lm: heliostat height, m
    wm: heliostat width, m
    min_dis: minimum safe distance of two adjacent heliostats' centre
    phi: golden ratio phi of eq.(14) in reference paper
    a: the coefficient a of eq.(15) in reference paper
    b: the coefficient b of eq.(15) in reference paper
    '''
    x = []
    y = []
    cnt = 0
    i = 0
    while cnt < target_num:
        i += 1
        theta = 2.0 * np.pi * np.power(phi, -2) * i
        r = a * np.power(i, b)
        xi = r * np.cos(theta)
        yi = r * np.sin(theta)

        if (heliostatCollisionConstrain([xi, yi], x, y, min_dis) == False):
            x.append(xi)
            y.append(yi)
            cnt += 1

    plt.scatter(x, y, color='blue', marker='.', label='Data Points')
    plt.show()

    output_file = open("layout.csv", "w")
    output_file.write("id,x,y,z\n")
    for i in range(len(x)):
        id = i + 1
        output_file.write(str(id)+","+str(x[i])+","+str(y[i])+","+"0.0\n")

    output_file.close()


if __name__ == "__main__":

    target_num = 1800  # target heliostat number
    lm = 4  # heliostat length, m
    wm = 3.2  # heliostat width, m
    phi = (1.0 + np.sqrt(5.0))/2.0  # golden ratio phi
    # the coefficient a of eq.(15) in <Noone2012, Heliostat Field Optimization: A New Computationally Efficient Model and Biomimetic Layout>
    a = 4.5
    b = 0.65
    # the coefficient b of eq.(15) in <Noone2012, Heliostat Field Optimization: A New Computationally Efficient Model and Biomimetic Layout>

    min_dis = np.sqrt(lm*lm+wm*wm) * 1.5  # the min distance between two adjacent heliostats
    biomimetic_fun(target_num, lm, wm, min_dis, phi, a, b)
